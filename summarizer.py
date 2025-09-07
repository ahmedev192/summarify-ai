import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import logging
from typing import Optional
from config import MODEL_NAME, MAX_LENGTH, MIN_LENGTH

logger = logging.getLogger(__name__)

class TextSummarizer:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.tokenizer = None
        self.model = None
        self.summarizer_pipeline = None
        self.is_loaded = False
        self._load_model()
    
    def _load_model(self):
        """Load the LLaMA/OPT model and tokenizer"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Check if CUDA is available
            device = "cuda" if torch.cuda.is_available() else "cpu"
            logger.info(f"Using device: {device}")
            
            # Pick dtype depending on device
            dtype = torch.float16 if device == "cuda" else torch.float32
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                dtype=dtype,
                device_map="auto" if device == "cuda" else None
            )
            
            # Move model to CPU manually if needed
            if device == "cpu":
                self.model = self.model.to(device)
            
            # Create summarization pipeline
            self.summarizer_pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=0 if device == "cuda" else -1
            )
            
            self.is_loaded = True
            logger.info("Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.is_loaded = False
            raise e
    
    def summarize(self, text: str, max_length: Optional[int] = None, min_length: Optional[int] = None) -> str:
        """Summarize the input text using the loaded model"""
        if not self.is_loaded:
            raise RuntimeError("Model not loaded. Please check the model loading process.")
        
        if not text.strip():
            raise ValueError("Input text cannot be empty")
        
        try:
            # Set default values
            max_len = max_length or MAX_LENGTH
            min_len = min_length or MIN_LENGTH
            
            # Create a prompt for summarization
            prompt = f"Summarize the following text in a concise way:\n\n{text}\n\nSummary:"
            
            # Generate summary
            result = self.summarizer_pipeline(
                prompt,
                max_length=max_len,
                min_length=min_len,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                truncation=True
            )
            
            # Extract the generated text
            generated_text = result[0]['generated_text']
            
            # Extract only the summary part (after "Summary:")
            if "Summary:" in generated_text:
                summary = generated_text.split("Summary:")[-1].strip()
            else:
                # Fallback: take the last part of generated text
                summary = generated_text[len(prompt):].strip()
            
            # Clean up the summary
            summary = self._clean_summary(summary)
            
            return summary
            
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            raise e
    
    def _clean_summary(self, summary: str) -> str:
        """Clean and format the generated summary"""
        # Remove any remaining prompt text
        summary = summary.replace("Summarize the following text in a concise way:", "").strip()
        
        # Remove incomplete trailing sentence
        sentences = summary.split('.')
        if len(sentences) > 1 and not sentences[-1].strip():
            summary = '.'.join(sentences[:-1]) + '.'
        
        # Ensure the summary ends with proper punctuation
        if summary and not summary.endswith(('.', '!', '?')):
            summary += '.'
        
        return summary.strip()
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        return {
            "model_name": self.model_name,
            "is_loaded": self.is_loaded,
            "device": "cuda" if torch.cuda.is_available() else "cpu",
            "max_length": MAX_LENGTH,
            "min_length": MIN_LENGTH
        }
