"""
Embedding model for generating vector representations of text
"""
import logging
from typing import List, Optional
import numpy as np
from sentence_transformers import SentenceTransformer

from src.config.settings import EMBEDDING_MODEL_NAME, EMBEDDING_DIMENSION

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generate embeddings for text using sentence transformers"""
    
    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        """
        Initialize embedding generator
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self.embedding_dimension = EMBEDDING_DIMENSION
        
        logger.info(f"Embedding generator initialized with model: {model_name}")
    
    def load_model(self):
        """Load the embedding model"""
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            try:
                self.model = SentenceTransformer(self.model_name)
                logger.info("Embedding model loaded successfully")
            except Exception as e:
                logger.error(f"Error loading embedding model: {str(e)}")
                raise
    
    def generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for a single text
        
        Args:
            text: Input text
            
        Returns:
            Numpy array of embeddings
        """
        if self.model is None:
            self.load_model()
        
        try:
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise
    
    def generate_embeddings(
        self,
        texts: List[str],
        batch_size: int = 32,
        show_progress: bool = True
    ) -> np.ndarray:
        """
        Generate embeddings for multiple texts
        
        Args:
            texts: List of input texts
            batch_size: Batch size for processing
            show_progress: Whether to show progress bar
            
        Returns:
            Numpy array of embeddings
        """
        if self.model is None:
            self.load_model()
        
        if not texts:
            logger.warning("Empty text list provided")
            return np.array([])
        
        try:
            logger.info(f"Generating embeddings for {len(texts)} texts")
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True
            )
            logger.info(f"Generated embeddings with shape: {embeddings.shape}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings"""
        return self.embedding_dimension


class EmbeddingCache:
    """Simple cache for embeddings"""
    
    def __init__(self):
        self.cache = {}
        logger.info("Embedding cache initialized")
    
    def get(self, text: str) -> Optional[np.ndarray]:
        """Get cached embedding"""
        return self.cache.get(text)
    
    def set(self, text: str, embedding: np.ndarray):
        """Cache an embedding"""
        self.cache[text] = embedding
    
    def clear(self):
        """Clear the cache"""
        self.cache.clear()
        logger.info("Embedding cache cleared")
    
    def size(self) -> int:
        """Get cache size"""
        return len(self.cache)


def main():
    """Test embedding generator"""
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create generator
    generator = EmbeddingGenerator()
    
    # Test texts
    if len(sys.argv) > 1:
        texts = sys.argv[1:]
    else:
        texts = [
            "Reduce plastic waste by using reusable bags",
            "Conserve water by fixing leaky faucets",
            "Save energy by using LED bulbs"
        ]
    
    print(f"\nGenerating embeddings for {len(texts)} texts...")
    
    # Generate embeddings
    embeddings = generator.generate_embeddings(texts)
    
    print(f"\nEmbedding shape: {embeddings.shape}")
    print(f"Embedding dimension: {generator.get_embedding_dimension()}")
    
    # Show first embedding preview
    print(f"\nFirst embedding preview (first 10 values):")
    print(embeddings[0][:10])
    
    # Test cache
    cache = EmbeddingCache()
    cache.set(texts[0], embeddings[0])
    cached = cache.get(texts[0])
    print(f"\nCache test: {'Passed' if cached is not None else 'Failed'}")
    print(f"Cache size: {cache.size()}")


if __name__ == "__main__":
    main()

# Made with Bob
