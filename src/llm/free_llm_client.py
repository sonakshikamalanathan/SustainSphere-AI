"""
Free LLM Client using Hugging Face Inference API
Supports IBM Granite and other open-source models
"""
import os
import requests
import logging
from typing import Optional
import re

logger = logging.getLogger(__name__)


class FreeLLMClient:
    """
    Free LLM client using Hugging Face Inference API
    
    Supports:
    - IBM Granite models (via Hugging Face)
    - Other open-source models
    - Completely free, no credit card needed
    """
    
    def __init__(self, model_name: str = "ibm-granite/granite-3.0-8b-instruct"):
        """
        Initialize free LLM client
        
        Args:
            model_name: Hugging Face model ID
        """
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        if not self.api_token:
            raise ValueError("HUGGINGFACE_API_TOKEN not found in environment variables")
        
        logger.info(f"Initialized free LLM client with model: {model_name}")
    
    def generate(
        self,
        prompt: str,
        max_new_tokens: int = 512,
        temperature: float = 0.3,
        top_p: float = 0.9
    ) -> str:
        """
        Generate response using Hugging Face Inference API
        
        Args:
            prompt: Input prompt
            max_new_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Generated text
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "return_full_text": False
            }
        }
        
        try:
            logger.info(f"Generating response with {self.model_name}")
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                # Handle different response formats
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                elif isinstance(result, dict):
                    generated_text = result.get("generated_text", "")
                else:
                    generated_text = str(result)
                
                logger.info("Response generated successfully")
                return generated_text.strip()
            
            elif response.status_code == 503:
                # Model is loading
                return "The AI model is currently loading. Please try again in a moment."
            
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return f"Error generating response. Please try again."
        
        except Exception as e:
            logger.error(f"Error calling Hugging Face API: {str(e)}")
            # Use offline fallback that extracts info from context
            return self._generate_offline_response(prompt)
    
    def _generate_offline_response(self, prompt: str) -> str:
        """
        Generate response from context when API is unavailable
        Extracts key information from the retrieved documents
        """
        # Extract context from prompt
        context_match = re.search(r'Context from sustainability documents:\s*(.*?)\s*Question:', prompt, re.DOTALL)
        
        if context_match:
            context = context_match.group(1).strip()
            
            # Extract question
            question_match = re.search(r'Question:\s*(.*?)\s*Instructions:', prompt, re.DOTALL)
            question = question_match.group(1).strip() if question_match else ""
            
            # Create structured response from context
            response = self._format_context_response(context, question)
            return response
        
        # Fallback if no context found
        return """⚠️ **Network Connectivity Issue**

I'm unable to connect to the AI model, but I've retrieved relevant information from the sustainability documents.

**Please review the source documents shown above** - they contain detailed information to answer your question.

**What's Working:**
✅ Document search and retrieval
✅ Relevance scoring
✅ Source citations

**Troubleshooting:**
- Check your internet connection
- Try using a mobile hotspot
- Ensure Hugging Face API is accessible

The retrieved sources contain the information you need!"""
    
    def _format_context_response(self, context: str, question: str) -> str:
        """
        Format context into a readable response
        """
        # Split context into sections
        sections = context.split('\n\n')
        
        # Build response
        response_parts = []
        response_parts.append("📚 **Based on the retrieved sustainability documents:**\n")
        
        # Add key points from context
        for i, section in enumerate(sections[:3], 1):  # Limit to 3 sections
            if section.strip():
                # Clean up the section
                clean_section = section.strip()
                # Add bullet point
                response_parts.append(f"**{i}.** {clean_section}\n")
        
        # Add note about offline mode
        response_parts.append("\n---")
        response_parts.append("\n⚠️ *Note: AI model is currently offline due to network issues. The information above is directly from the retrieved sustainability documents.*")
        response_parts.append("\n\n💡 **Tip:** Review the full source documents below for more detailed information.")
        
        return "\n".join(response_parts)


class FastFreeLLMClient(FreeLLMClient):
    """Faster alternative using smaller models"""
    
    def __init__(self):
        # Use a smaller, faster model
        super().__init__(model_name="google/flan-t5-base")


def main():
    """Test the free LLM client"""
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test prompt
    prompt = """You are a sustainability advisor. Answer this question:

Question: How can I reduce plastic waste at home?

Answer:"""
    
    print("\n🧪 Testing Free LLM Client...")
    print(f"Prompt: {prompt}\n")
    
    try:
        # Try IBM Granite first
        print("Trying IBM Granite model...")
        client = FreeLLMClient()
        response = client.generate(prompt)
        print(f"\n✅ Response:\n{response}\n")
    
    except Exception as e:
        print(f"\n⚠️ Granite not available, trying alternative...")
        # Fallback to faster model
        client = FastFreeLLMClient()
        response = client.generate(prompt)
        print(f"\n✅ Response:\n{response}\n")


if __name__ == "__main__":
    main()

# Made with Bob
