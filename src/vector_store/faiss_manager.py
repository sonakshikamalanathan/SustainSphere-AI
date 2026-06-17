"""
FAISS vector store manager for similarity search
"""
import logging
import pickle
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
import faiss

from src.config.settings import (
    FAISS_INDEX_PATH,
    FAISS_INDEX_TYPE,
    EMBEDDING_DIMENSION,
    TOP_K_DOCUMENTS,
    SIMILARITY_THRESHOLD
)

logger = logging.getLogger(__name__)


class FAISSManager:
    """Manage FAISS vector store for document retrieval"""
    
    def __init__(
        self,
        embedding_dimension: int = EMBEDDING_DIMENSION,
        index_type: str = FAISS_INDEX_TYPE
    ):
        """
        Initialize FAISS manager
        
        Args:
            embedding_dimension: Dimension of embeddings
            index_type: Type of FAISS index ('Flat' or 'IVF')
        """
        self.embedding_dimension = embedding_dimension
        self.index_type = index_type
        self.index: Optional[faiss.Index] = None
        self.documents: List[Dict[str, Any]] = []
        self.index_path = Path(FAISS_INDEX_PATH)
        
        logger.info(f"FAISS manager initialized: dim={embedding_dimension}, type={index_type}")
    
    def create_index(self):
        """Create a new FAISS index"""
        logger.info(f"Creating {self.index_type} FAISS index")
        
        if self.index_type == "Flat":
            # Flat index for exact search (good for small datasets)
            self.index = faiss.IndexFlatL2(self.embedding_dimension)
        elif self.index_type == "IVF":
            # IVF index for faster approximate search
            quantizer = faiss.IndexFlatL2(self.embedding_dimension)
            self.index = faiss.IndexIVFFlat(
                quantizer,
                self.embedding_dimension,
                100  # number of clusters
            )
        else:
            raise ValueError(f"Unsupported index type: {self.index_type}")
        
        logger.info("FAISS index created successfully")
    
    def add_documents(
        self,
        embeddings: np.ndarray,
        documents: List[Dict[str, Any]]
    ):
        """
        Add documents and their embeddings to the index
        
        Args:
            embeddings: Numpy array of embeddings (n_docs, embedding_dim)
            documents: List of document dictionaries with metadata
        """
        if self.index is None:
            self.create_index()
        
        # Ensure embeddings are float32
        embeddings = embeddings.astype('float32')
        
        # Train index if needed (for IVF)
        if self.index_type == "IVF" and not self.index.is_trained:
            logger.info("Training IVF index...")
            self.index.train(embeddings)
        
        # Add vectors to index
        self.index.add(embeddings)
        
        # Store documents
        self.documents.extend(documents)
        
        logger.info(f"Added {len(documents)} documents to index. Total: {len(self.documents)}")
    
    def search(
        self,
        query_embedding: np.ndarray,
        k: int = TOP_K_DOCUMENTS,
        threshold: float = SIMILARITY_THRESHOLD
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Search for similar documents
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            List of (document, similarity_score) tuples
        """
        if self.index is None or len(self.documents) == 0:
            logger.warning("Index is empty or not created")
            return []
        
        # Ensure query is 2D and float32
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        query_embedding = query_embedding.astype('float32')
        
        # Search
        distances, indices = self.index.search(query_embedding, k)
        
        # Convert distances to similarity scores (cosine similarity)
        # For L2 distance, similarity = 1 / (1 + distance)
        similarities = 1 / (1 + distances[0])
        
        # Filter by threshold and prepare results
        results = []
        for idx, similarity in zip(indices[0], similarities):
            if idx < len(self.documents) and similarity >= threshold:
                results.append((self.documents[idx], float(similarity)))
        
        logger.info(f"Found {len(results)} documents above threshold {threshold}")
        return results
    
    def save_index(self, path: Optional[Path] = None):
        """
        Save FAISS index and documents to disk
        
        Args:
            path: Path to save index (uses default if None)
        """
        if self.index is None:
            logger.warning("No index to save")
            return
        
        save_path = path or self.index_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save FAISS index
        index_file = save_path.with_suffix('.index')
        faiss.write_index(self.index, str(index_file))
        logger.info(f"Saved FAISS index to {index_file}")
        
        # Save documents
        docs_file = save_path.with_suffix('.pkl')
        with open(docs_file, 'wb') as f:
            pickle.dump(self.documents, f)
        logger.info(f"Saved documents to {docs_file}")
    
    def load_index(self, path: Optional[Path] = None):
        """
        Load FAISS index and documents from disk
        
        Args:
            path: Path to load index from (uses default if None)
        """
        load_path = path or self.index_path
        
        # Load FAISS index
        index_file = load_path.with_suffix('.index')
        if not index_file.exists():
            raise FileNotFoundError(f"Index file not found: {index_file}")
        
        self.index = faiss.read_index(str(index_file))
        logger.info(f"Loaded FAISS index from {index_file}")
        
        # Load documents
        docs_file = load_path.with_suffix('.pkl')
        if not docs_file.exists():
            raise FileNotFoundError(f"Documents file not found: {docs_file}")
        
        with open(docs_file, 'rb') as f:
            self.documents = pickle.load(f)
        logger.info(f"Loaded {len(self.documents)} documents from {docs_file}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the index"""
        if self.index is None:
            return {
                'total_documents': 0,
                'index_type': self.index_type,
                'embedding_dimension': self.embedding_dimension,
                'is_trained': False
            }
        
        return {
            'total_documents': len(self.documents),
            'index_type': self.index_type,
            'embedding_dimension': self.embedding_dimension,
            'is_trained': self.index.is_trained if hasattr(self.index, 'is_trained') else True,
            'total_vectors': self.index.ntotal
        }
    
    def clear(self):
        """Clear the index and documents"""
        self.index = None
        self.documents = []
        logger.info("Index and documents cleared")


def main():
    """Test FAISS manager"""
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create manager
    manager = FAISSManager(embedding_dimension=384)
    
    # Create dummy embeddings and documents
    n_docs = 10
    embeddings = np.random.rand(n_docs, 384).astype('float32')
    documents = [
        {
            'content': f'Document {i} about sustainability',
            'metadata': {'id': i, 'source': f'doc_{i}.pdf'}
        }
        for i in range(n_docs)
    ]
    
    print("\nAdding documents to index...")
    manager.add_documents(embeddings, documents)
    
    # Get stats
    stats = manager.get_stats()
    print(f"\nIndex Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Test search
    query_embedding = np.random.rand(384).astype('float32')
    print(f"\nSearching for similar documents...")
    results = manager.search(query_embedding, k=3, threshold=0.0)
    
    print(f"\nFound {len(results)} results:")
    for doc, score in results:
        print(f"  - {doc['metadata']['source']}: {score:.4f}")
    
    # Test save/load
    if len(sys.argv) > 1 and sys.argv[1] == '--save':
        print("\nSaving index...")
        manager.save_index()
        
        print("Loading index...")
        manager2 = FAISSManager(embedding_dimension=384)
        manager2.load_index()
        
        stats2 = manager2.get_stats()
        print(f"\nLoaded index statistics:")
        for key, value in stats2.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    main()

# Made with Bob
