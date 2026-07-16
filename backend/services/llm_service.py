"""
backend/services/llm_service.py

Service for interacting with the LoRA fine-tuned Mistral model.
Loads the model into VRAM once and serves inference requests.
"""

import logging
import re
import torch
from pathlib import Path
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from backend.config import BASE_MODEL_NAME, LORA_ADAPTER_PATH

logger = logging.getLogger(__name__)

class LLMService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.tokenizer = None
        return cls._instance

    def load_model(self):
        """Loads the base model and LoRA adapter into VRAM."""
        if self.model is not None:
            return  # Already loaded

        if not Path(LORA_ADAPTER_PATH).exists():
            logger.warning(f"LoRA adapter not found at {LORA_ADAPTER_PATH}. Running in mock mode.")
            return

        logger.info("Initializing Tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            str(LORA_ADAPTER_PATH),
            use_fast=True
        )

        logger.info("Initializing 4-bit Quantization Config...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )

        logger.info(f"Loading Base Model ({BASE_MODEL_NAME})...")
        base_model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL_NAME,
            quantization_config=bnb_config,
            device_map="auto",
            attn_implementation="sdpa",
        )

        logger.info("Applying LoRA Adapter...")
        self.model = PeftModel.from_pretrained(base_model, str(LORA_ADAPTER_PATH))
        self.model.eval()
        
        logger.info("LLM Service successfully initialized.")

    def format_prompt(self, instruction: str, input_text: str) -> str:
        """Format the prompt using Mistral Instruct template."""
        return f"<s>[INST] {instruction}\n\n{input_text} [/INST]\n"

    def generate(self, instruction: str, input_text: str, max_new_tokens: int = 400) -> str:
        """Generate response from the model."""
        if self.model is None or self.tokenizer is None:
            self.load_model()
            
        if self.model is None: # Still none (meaning mock mode)
            return "**Technical Explanation**:\nModel is not loaded."

        prompt = self.format_prompt(instruction, input_text)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=0.2,
                top_p=0.95,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        generated_ids = outputs[0][inputs.input_ids.shape[-1]:]
        return self.tokenizer.decode(generated_ids, skip_special_tokens=True).strip()

    def parse_output(self, raw_text: str) -> dict:
        """
        Parses the structured markdown output into a dictionary.
        Extracts sections like **Technical Explanation**, **Beginner Explanation**, etc.
        """
        parsed = {
            "technical": "",
            "beginner": "",
            "analogy": "",
            "solution": "",
            "optimized_code": "",
            "prevention": "",
            "complexity_before": "",
            "complexity_after": ""
        }
        
        # Simple regex to extract blocks between bold headers
        sections = re.split(r'\*\*([^*]+)\*\*:', raw_text)
        
        if len(sections) > 1:
            for i in range(1, len(sections), 2):
                header = sections[i].strip().lower()
                content = sections[i+1].strip() if i+1 < len(sections) else ""
                
                if "technical" in header:
                    parsed["technical"] = content
                elif "beginner" in header:
                    parsed["beginner"] = content
                elif "analogy" in header:
                    parsed["analogy"] = content
                elif "solution" in header:
                    parsed["solution"] = content
                elif "optimized" in header:
                    # Strip markdown code blocks from optimized code if present
                    content = re.sub(r'^```[a-z]*\n|```$', '', content, flags=re.MULTILINE).strip()
                    parsed["optimized_code"] = content
                elif "prevention" in header:
                    parsed["prevention"] = content
                elif "complexity" in header:
                    # Extract Before and After if they exist
                    if "Before:" in content:
                        before_match = re.search(r'Before:\s*(O\([^)]+\))', content)
                        if before_match:
                            parsed["complexity_before"] = before_match.group(1)
                    if "After:" in content:
                        after_match = re.search(r'After:\s*(O\([^)]+\))', content)
                        if after_match:
                            parsed["complexity_after"] = after_match.group(1)
                            
        return parsed

# Global singleton instance
llm_service = LLMService()
