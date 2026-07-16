"""
evaluate.py

Evaluates the trained LoRA adapter against the base Mistral model.
Tests inference on standard debugging scenarios: Compiler Errors, Runtime Errors,
Logical Bugs, and Optimizations.
"""
import logging
import sys
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from config import OUTPUT_DIR, ModelConfig, TokenizerConfig

# Logging setup
logging.basicConfig(level=logging.INFO, format="%(levelname)-5s %(message)s", handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger("evaluate")
logging.getLogger("transformers").setLevel(logging.WARNING)

# Test samples covering all debugging categories
TEST_SAMPLES = [
    {
        "category": "Compiler Error Explanation",
        "instruction": "Explain this compiler error and provide a fix.",
        "input": "Error: 'vector' was not declared in this scope\nCode:\nint main() {\n  vector<int> v;\n  return 0;\n}"
    },
    {
        "category": "Runtime Error Explanation",
        "instruction": "Diagnose this runtime error and provide a fix.",
        "input": "IndexError: list index out of range\nCode:\narr = [1, 2, 3]\nprint(arr[3])"
    },
    {
        "category": "Logical Bug Explanation",
        "instruction": "Find and fix the logical bug in this code.",
        "input": "Code:\ndef is_even(n):\n    return n % 2 == 1"
    },
    {
        "category": "Optimization Suggestion",
        "instruction": "Suggest performance optimizations for this code.",
        "input": "Code:\ndef get_unique(items):\n    unique_items = []\n    for item in items:\n        if item not in unique_items:\n            unique_items.append(item)\n    return unique_items"
    }
]

def format_prompt(instruction: str, input_text: str) -> str:
    """Format prompt using the Mistral Instruct template."""
    return f"<s>[INST] {instruction}\n\n{input_text} [/INST]\n"

def generate_response(model, tokenizer, prompt: str) -> str:
    """Generate a response from the model."""
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            temperature=0.2,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode the newly generated tokens (ignoring the prompt)
    generated_ids = outputs[0][inputs.input_ids.shape[-1]:]
    return tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

def main():
    logger.info("DebugGPT Model Evaluation v1.0")
    logger.info("=" * 45)
    
    if not OUTPUT_DIR.exists():
        logger.error(f"LoRA adapter not found at {OUTPUT_DIR}. Train the model first.")
        return
        
    logger.info("Loading Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(OUTPUT_DIR, use_fast=TokenizerConfig.USE_FAST)
    
    logger.info("Configuring 4-bit quantization...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16,
        bnb_4bit_use_double_quant=True,
    )
    
    logger.info("Loading Base Model...")
    base_model = AutoModelForCausalLM.from_pretrained(
        ModelConfig.BASE_MODEL_NAME,
        quantization_config=bnb_config,
        device_map="auto",
        attn_implementation="sdpa",
    )
    
    logger.info("Loading LoRA Adapter...")
    model = PeftModel.from_pretrained(base_model, str(OUTPUT_DIR))
    model.eval()
    
    logger.info("Starting Evaluation...\n")
    
    for idx, sample in enumerate(TEST_SAMPLES, 1):
        logger.info(f"--- Test {idx}: {sample['category']} ---")
        prompt = format_prompt(sample["instruction"], sample["input"])
        
        # 1. Base Model Output
        logger.info("Generating with Base Model...")
        with model.disable_adapter():
            base_output = generate_response(model, tokenizer, prompt)
            
        # 2. Fine-Tuned Model Output
        logger.info("Generating with Fine-Tuned Model...")
        finetuned_output = generate_response(model, tokenizer, prompt)
        
        print(f"\n[Base Model Output - {sample['category']}]")
        print(base_output)
        print("-" * 40)
        print(f"[Fine-Tuned Model Output - {sample['category']}]")
        print(finetuned_output)
        print("=" * 60 + "\n")
        
    logger.info("Evaluation Complete.")

if __name__ == "__main__":
    main()
