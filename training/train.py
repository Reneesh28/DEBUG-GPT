"""
DebugGPT LoRA Fine-Tuning Pipeline.

A clean, single-responsibility training script for fine-tuning Mistral 7B
with QLoRA on a consumer GPU (RTX 5050 Laptop, 8 GB VRAM).

Pipeline:
    main()
     ├── setup_logging()
     ├── load_environment()
     ├── validate_gpu()
     ├── load_training_dataset()
     ├── create_tokenizer()
     ├── create_quantization_config()
     ├── load_base_model()
     ├── create_lora_config()
     ├── create_training_args()
     ├── create_trainer()
     ├── trainer.train()
     └── save_adapter()
"""

import logging
import os
import sys
from pathlib import Path

import torch
from datasets import load_dataset, Dataset
from dotenv import load_dotenv
from peft import LoraConfig, PeftModel
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    PreTrainedTokenizerBase,
)
from trl import SFTConfig, SFTTrainer

from config import (
    PROJECT_ROOT,
    DATASET_PATH,
    OUTPUT_DIR,
    ModelConfig,
    TokenizerConfig,
    QLoraConfig,
    LoraConfigParams,
    TrainingConfig,
)

# Logging

logger = logging.getLogger("debuggpt.train")


def setup_logging() -> None:
    """Configure structured logging for the training pipeline."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)-5s  %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    # Silence overly chatty libraries
    logging.getLogger("transformers").setLevel(logging.WARNING)
    logging.getLogger("datasets").setLevel(logging.WARNING)
    logging.getLogger("accelerate").setLevel(logging.WARNING)


# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------

def load_environment() -> None:
    """Load .env file and set the HF token if present."""
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)

    # Support both key names — the .env uses HUGGING_FACE_TOKEN
    hf_token = os.getenv("HF_TOKEN") or os.getenv("HUGGING_FACE_TOKEN")

    if hf_token:
        # Set as HF_TOKEN so huggingface_hub picks it up automatically
        os.environ["HF_TOKEN"] = hf_token
        logger.info("HF_TOKEN loaded from .env")
    else:
        logger.warning("HF_TOKEN not found — requests will be unauthenticated")


# ---------------------------------------------------------------------------
# GPU Validation
# ---------------------------------------------------------------------------

def validate_gpu() -> None:
    """Assert that a CUDA GPU is available and log its capabilities."""
    if not torch.cuda.is_available():
        raise RuntimeError(
            "CUDA GPU not detected. "
            "This pipeline requires an NVIDIA GPU with CUDA support."
        )

    device = torch.cuda.current_device()
    gpu_name = torch.cuda.get_device_name(device)
    vram_gb = torch.cuda.get_device_properties(device).total_memory / (1024 ** 3)
    cuda_version = torch.version.cuda or "unknown"
    bf16_supported = torch.cuda.is_bf16_supported()

    logger.info("-" * 45)
    logger.info("GPU  : %s", gpu_name)
    logger.info("VRAM : %.2f GB", vram_gb)
    logger.info("CUDA : %s", cuda_version)
    logger.info("BF16 : %s", "Supported" if bf16_supported else "Not supported")
    logger.info("-" * 45)

    # Safety check: warn if BF16 is configured but not supported
    if TrainingConfig.BF16 and not bf16_supported:
        logger.warning(
            "BF16 is enabled in config but not supported by this GPU. "
            "Falling back to FP16 may be necessary."
        )


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

def format_for_mistral(example: dict) -> str:
    """
    Apply the Mistral instruction template to a single dataset record.

    Template:
        <s>[INST] {instruction}

        {input} [/INST]
        {response}</s>
    """
    return (
        f"<s>[INST] {example['instruction']}\n\n"
        f"{example['input']} [/INST]\n"
        f"{example['response']}</s>"
    )


def load_training_dataset() -> Dataset:
    """Load the JSONL dataset and return a HuggingFace Dataset."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {DATASET_PATH}\n"
            f"Run  python training/prepare_dataset.py  first."
        )

    logger.info("Loading dataset from %s ...", DATASET_PATH.relative_to(PROJECT_ROOT))
    dataset = load_dataset("json", data_files=str(DATASET_PATH), split="train")
    logger.info("Loaded %s training samples", f"{len(dataset):,}")
    return dataset


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

def create_tokenizer() -> PreTrainedTokenizerBase:
    """Initialise the tokenizer with correct padding configuration."""
    logger.info("Initializing tokenizer (%s) ...", ModelConfig.BASE_MODEL_NAME)

    tokenizer = AutoTokenizer.from_pretrained(
        ModelConfig.BASE_MODEL_NAME,
        use_fast=TokenizerConfig.USE_FAST,
    )
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = TokenizerConfig.PADDING_SIDE

    return tokenizer


# ---------------------------------------------------------------------------
# Quantization
# ---------------------------------------------------------------------------

def create_quantization_config() -> BitsAndBytesConfig:
    """Create the 4-bit QLoRA quantization configuration."""
    compute_dtype = getattr(torch, QLoraConfig.BNB_4BIT_COMPUTE_DTYPE)

    logger.info(
        "Configuring 4-bit QLoRA (NF4, double quant, compute=%s) ...",
        QLoraConfig.BNB_4BIT_COMPUTE_DTYPE,
    )

    return BitsAndBytesConfig(
        load_in_4bit=QLoraConfig.LOAD_IN_4BIT,
        bnb_4bit_quant_type=QLoraConfig.BNB_4BIT_QUANT_TYPE,
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=QLoraConfig.BNB_4BIT_USE_DOUBLE_QUANT,
    )


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

def load_base_model(bnb_config: BitsAndBytesConfig) -> AutoModelForCausalLM:
    """Load the base model with quantization and optimised attention."""
    logger.info("Loading base model (this may take a few minutes) ...")

    model = AutoModelForCausalLM.from_pretrained(
        ModelConfig.BASE_MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        attn_implementation="sdpa",  # Fused attention kernels (2-3x faster)
    )
    model.config.use_cache = False  # Required for gradient checkpointing

    return model


# ---------------------------------------------------------------------------
# LoRA
# ---------------------------------------------------------------------------

def create_lora_config() -> LoraConfig:
    """Create the PEFT LoRA configuration."""
    logger.info(
        "Configuring LoRA (r=%d, alpha=%d, %d target modules) ...",
        LoraConfigParams.R,
        LoraConfigParams.LORA_ALPHA,
        len(LoraConfigParams.TARGET_MODULES),
    )

    return LoraConfig(
        r=LoraConfigParams.R,
        lora_alpha=LoraConfigParams.LORA_ALPHA,
        lora_dropout=LoraConfigParams.LORA_DROPOUT,
        target_modules=LoraConfigParams.TARGET_MODULES,
        bias=LoraConfigParams.BIAS,
        task_type=LoraConfigParams.TASK_TYPE,
    )


# ---------------------------------------------------------------------------
# Training Arguments
# ---------------------------------------------------------------------------

def create_training_args() -> SFTConfig:
    """Create the SFT training configuration."""
    effective_batch = (
        TrainingConfig.PER_DEVICE_TRAIN_BATCH_SIZE
        * TrainingConfig.GRADIENT_ACCUMULATION_STEPS
    )

    logger.info(
        "Training config: %d epochs, effective batch=%d, lr=%s, optim=%s, packing=%s",
        TrainingConfig.NUM_TRAIN_EPOCHS,
        effective_batch,
        TrainingConfig.LEARNING_RATE,
        TrainingConfig.OPTIM,
        TrainingConfig.PACKING,
    )

    return SFTConfig(
        output_dir=str(OUTPUT_DIR),
        per_device_train_batch_size=TrainingConfig.PER_DEVICE_TRAIN_BATCH_SIZE,
        gradient_accumulation_steps=TrainingConfig.GRADIENT_ACCUMULATION_STEPS,
        gradient_checkpointing=TrainingConfig.GRADIENT_CHECKPOINTING,
        learning_rate=TrainingConfig.LEARNING_RATE,
        num_train_epochs=TrainingConfig.NUM_TRAIN_EPOCHS,
        lr_scheduler_type=TrainingConfig.LR_SCHEDULER_TYPE,
        warmup_ratio=TrainingConfig.WARMUP_RATIO,
        optim=TrainingConfig.OPTIM,
        fp16=TrainingConfig.FP16,
        bf16=TrainingConfig.BF16,
        save_strategy=TrainingConfig.SAVE_STRATEGY,
        logging_steps=TrainingConfig.LOGGING_STEPS,
        eval_strategy=TrainingConfig.EVAL_STRATEGY,
        max_length=TokenizerConfig.MAX_SEQ_LENGTH,
        packing=TrainingConfig.PACKING,
        # Speed optimisations
        dataloader_num_workers=TrainingConfig.DATALOADER_NUM_WORKERS,
        dataloader_pin_memory=TrainingConfig.DATALOADER_PIN_MEMORY,
        torch_compile=TrainingConfig.TORCH_COMPILE,
    )


# ---------------------------------------------------------------------------
# Trainer
# ---------------------------------------------------------------------------

def create_trainer(
    model: AutoModelForCausalLM,
    dataset: Dataset,
    tokenizer: PreTrainedTokenizerBase,
    peft_config: LoraConfig,
    training_args: SFTConfig,
) -> SFTTrainer:
    """Assemble the SFTTrainer with all components."""
    logger.info("Initializing SFTTrainer (packing=%s) ...", TrainingConfig.PACKING)

    if TrainingConfig.PACKING:
        # Pre-format each sample into a "text" column for packing.
        # SFTTrainer will bin multiple samples into full 1024-token
        # sequences — zero padding waste.
        dataset = dataset.map(lambda ex: {"text": format_for_mistral(ex)})
        return SFTTrainer(
            model=model,
            train_dataset=dataset,
            processing_class=tokenizer,
            peft_config=peft_config,
            args=training_args,
        )

    return SFTTrainer(
        model=model,
        train_dataset=dataset,
        processing_class=tokenizer,
        peft_config=peft_config,
        args=training_args,
        formatting_func=format_for_mistral,
    )


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save_adapter(trainer: SFTTrainer, tokenizer: PreTrainedTokenizerBase) -> None:
    """Save the fine-tuned LoRA adapter and tokenizer."""
    output_path = str(OUTPUT_DIR)
    logger.info("Saving LoRA adapter to %s ...", OUTPUT_DIR.relative_to(PROJECT_ROOT))

    trainer.save_model(output_path)
    tokenizer.save_pretrained(output_path)

    logger.info("Adapter and tokenizer saved successfully.")


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    """Execute the full DebugGPT fine-tuning pipeline."""
    # 1. Logging
    setup_logging()
    logger.info("DebugGPT Training Pipeline v1.0")
    logger.info("=" * 45)

    # 2. Environment
    load_environment()

    # 3. GPU validation
    validate_gpu()

    # 4. Dataset
    dataset = load_training_dataset()

    # 5. Tokenizer
    tokenizer = create_tokenizer()

    # 6. Quantization
    bnb_config = create_quantization_config()

    # 7. Base model
    model = load_base_model(bnb_config)

    # 8. Check if a previously trained adapter exists.
    #    If so, load it and train for 1 more epoch (continuation mode).
    #    Otherwise, create a fresh LoRA adapter and train from scratch.
    adapter_path = OUTPUT_DIR / "adapter_config.json"
    if adapter_path.exists():
        logger.info("Found trained adapter at %s — loading for continuation...", OUTPUT_DIR)
        model = PeftModel.from_pretrained(model, str(OUTPUT_DIR), is_trainable=True)
        peft_config = None  # Adapter already attached
        continuation = True
    else:
        peft_config = create_lora_config()
        continuation = False

    # 9. Training arguments
    training_args = create_training_args()

    # In continuation mode, train for exactly 1 epoch from the loaded adapter.
    if continuation:
        training_args.num_train_epochs = 1
        logger.info("Continuation mode: training 1 additional epoch.")

    # 10. Trainer
    trainer = create_trainer(model, dataset, tokenizer, peft_config, training_args)

    # 11. Train
    if not continuation:
        # Fresh training: check for checkpoints to resume from
        checkpoint_exists = False
        if OUTPUT_DIR.exists():
            for d in OUTPUT_DIR.iterdir():
                if d.is_dir() and d.name.startswith("checkpoint-"):
                    checkpoint_exists = True
                    break

        if checkpoint_exists:
            logger.info("Resuming training from latest checkpoint...")
            trainer.train(resume_from_checkpoint=True)
        else:
            logger.info("Starting fresh training...")
            trainer.train()
    else:
        # Continuation: train fresh 1 epoch with the loaded adapter
        logger.info("Starting epoch 3 training...")
        trainer.train()

    # 12. Save
    save_adapter(trainer, tokenizer)

    logger.info("=" * 45)
    logger.info("Training complete.")


if __name__ == "__main__":
    main()
