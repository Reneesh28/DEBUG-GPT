"""
Configuration for DebugGPT LoRA Fine-Tuning Pipeline.

This file is the single source of truth for all training parameters.
It contains ONLY configuration values — no torch logic, no GPU detection,
no training code, no dataset formatting.

Hardware target: RTX 5050 Laptop GPU (8 GB VRAM, Blackwell, BF16-capable)
"""

from pathlib import Path


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "datasets" / "debuggpt_training_dataset.jsonl"
OUTPUT_DIR = PROJECT_ROOT / "models" / "debuggpt-lora"


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------

class ModelConfig:
    BASE_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

class TokenizerConfig:
    MAX_SEQ_LENGTH = 1024   # Optimised: P90=~490 tokens, P95=~510 tokens
    PADDING_SIDE = "right"  # Standard for causal language modeling
    TRUNCATION = True
    USE_FAST = True         # Use the fast Rust-based tokenizer


# ---------------------------------------------------------------------------
# QLoRA  (4-bit quantization via bitsandbytes)
# ---------------------------------------------------------------------------

class QLoraConfig:
    LOAD_IN_4BIT = True
    BNB_4BIT_QUANT_TYPE = "nf4"
    BNB_4BIT_COMPUTE_DTYPE = "bfloat16"   # Parsed into torch dtype in train.py
    BNB_4BIT_USE_DOUBLE_QUANT = True


# ---------------------------------------------------------------------------
# LoRA  (Low-Rank Adaptation via PEFT)
# ---------------------------------------------------------------------------

class LoraConfigParams:
    R = 16
    LORA_ALPHA = 32
    LORA_DROPOUT = 0.05
    TARGET_MODULES = [
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
    ]
    BIAS = "none"
    TASK_TYPE = "CAUSAL_LM"


# ---------------------------------------------------------------------------
# Training
#
# Memory budget breakdown  (RTX 5050, 8 GB VRAM, seq_len=1024):
#   Model (4-bit)        ~3.5 GB
#   LoRA adapters         ~0.2 GB
#   Optimizer (8-bit)     ~0.4 GB
#   Activations (bs=4)    ~2.8 GB  (with gradient checkpointing + packing)
#   Overhead / buffers    ~0.8 GB
#   ─────────────────────────────
#   Total estimate        ~7.7 GB
# ---------------------------------------------------------------------------

class TrainingConfig:
    PER_DEVICE_TRAIN_BATCH_SIZE = 2     # Batch=4 OOMs with torch.compile disabled
    GRADIENT_ACCUMULATION_STEPS = 4     # Effective batch = 2 × 4 = 8 (same)
    GRADIENT_CHECKPOINTING = True       # Trades ~20% speed for ~40% VRAM

    LEARNING_RATE = 2e-4
    NUM_TRAIN_EPOCHS = 3
    LR_SCHEDULER_TYPE = "cosine"
    WARMUP_RATIO = 0.03

    OPTIM = "paged_adamw_8bit"          # 8-bit optimizer saves ~1 GB

    FP16 = False
    BF16 = True                         # Native on RTX 5050 (Blackwell SM 12.8)

    SAVE_STRATEGY = "epoch"
    LOGGING_STEPS = 25
    EVAL_STRATEGY = "no"

    # Speed optimisations
    PACKING = True                      # Pack multiple samples per sequence (biggest win)
    DATALOADER_NUM_WORKERS = 4          # Parallel data loading
    DATALOADER_PIN_MEMORY = True        # Faster CPU→GPU transfer
    TORCH_COMPILE = False               # Incompatible with bnb 4-bit quantized models (OOM)
