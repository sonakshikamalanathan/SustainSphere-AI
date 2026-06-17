"""
Text splitting utilities for chunking documents
"""
import logging
from typing import List, Dict, Any, Optional
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config.settings import CHUNK_SIZE, CHUNK_OVERLAP

logger = logging.getLogger(__name__)


class DocumentChunker:
    """Split documents into chunks for embedding"""
    
    # Default separators for text splitting
    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]
    
    def __init__(
        self,
        chunk_size: int = CHUNK_SIZE,
        chunk_overlap: int = CHUNK_OVERLAP,
        separators: Optional[List[str]] = None
    ):
        """
        Initialize document chunker
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Overlap between chunks
            separators: List of separators for splitting
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators if separators is not None else self.DEFAULT_SEPARATORS
        
        # Initialize LangChain text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=self.separators,
            length_function=len,
        )
        
        logger.info(f"Initialized chunker: size={chunk_size}, overlap={chunk_overlap}")
    
    def chunk_document(self, document: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split a document into chunks
        
        Args:
            document: Document dictionary with 'content' and 'metadata'
            
        Returns:
            List of chunk dictionaries
        """
        content = document.get('content', '')
        metadata = document.get('metadata', {})
        
        if not content:
            logger.warning(f"Empty content for document: {metadata.get('filename', 'unknown')}")
            return []
        
        # Split text into chunks
        text_chunks = self.text_splitter.split_text(content)
        
        # Create chunk dictionaries with metadata
        chunks = []
        for i, chunk_text in enumerate(text_chunks):
            chunk = {
                'content': chunk_text,
                'metadata': {
                    **metadata,
                    'chunk_id': i,
                    'total_chunks': len(text_chunks),
                    'chunk_size': len(chunk_text)
                }
            }
            chunks.append(chunk)
        
        logger.info(f"Split document into {len(chunks)} chunks")
        return chunks
    
    def chunk_documents(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Split multiple documents into chunks
        
        Args:
            documents: List of document dictionaries
            
        Returns:
            List of all chunks from all documents
        """
        all_chunks = []
        
        for doc in documents:
            try:
                chunks = self.chunk_document(doc)
                all_chunks.extend(chunks)
            except Exception as e:
                logger.error(f"Error chunking document: {str(e)}")
                continue
        
        logger.info(f"Total chunks created: {len(all_chunks)}")
        return all_chunks
    
    def get_chunk_stats(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about chunks
        
        Args:
            chunks: List of chunk dictionaries
            
        Returns:
            Dictionary with chunk statistics
        """
        if not chunks:
            return {
                'total_chunks': 0,
                'avg_chunk_size': 0,
                'min_chunk_size': 0,
                'max_chunk_size': 0
            }
        
        chunk_sizes = [len(chunk['content']) for chunk in chunks]
        
        stats = {
            'total_chunks': len(chunks),
            'avg_chunk_size': sum(chunk_sizes) / len(chunk_sizes),
            'min_chunk_size': min(chunk_sizes),
            'max_chunk_size': max(chunk_sizes),
            'total_characters': sum(chunk_sizes)
        }
        
        return stats


def main():
    """Test text splitter"""
    import sys
    from pathlib import Path
    from src.data_processing.document_loader import DocumentLoader
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) > 1:
        # Load document
        loader = DocumentLoader()
        doc = loader.load_document(Path(sys.argv[1]))
        
        # Chunk document
        chunker = DocumentChunker()
        chunks = chunker.chunk_document(doc)
        
        # Print stats
        stats = chunker.get_chunk_stats(chunks)
        print(f"\nChunk Statistics:")
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"Average size: {stats['avg_chunk_size']:.0f} characters")
        print(f"Min size: {stats['min_chunk_size']} characters")
        print(f"Max size: {stats['max_chunk_size']} characters")
        
        # Print first chunk
        if chunks:
            print(f"\nFirst chunk preview:")
            print(chunks[0]['content'][:200] + "...")
    else:
        print("Usage: python text_splitter.py <document_path>")


if __name__ == "__main__":
    main()

# Made with Bob
