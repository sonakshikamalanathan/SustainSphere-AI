"""
Build FAISS index from sustainability documents
"""
import logging
import sys
from pathlib import Path
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config.settings import RAW_DATA_DIR, VECTOR_STORE_DIR
from src.data_processing.document_loader import DocumentLoader
from src.data_processing.text_splitter import DocumentChunker
from src.embeddings.embedding_model import EmbeddingGenerator
from src.vector_store.faiss_manager import FAISSManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/indexing.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class IndexBuilder:
    """Build FAISS index from documents"""
    
    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = DocumentChunker()
        self.embedder = EmbeddingGenerator()
        self.faiss_manager = FAISSManager()
        
        logger.info("Index builder initialized")
    
    def build_index(self, data_dir: Path, save_path: Path = None):
        """
        Build complete index from documents
        
        Args:
            data_dir: Directory containing documents
            save_path: Path to save index
        """
        logger.info(f"Starting index build from: {data_dir}")
        start_time = datetime.now()
        
        # Step 1: Load documents
        logger.info("Step 1: Loading documents...")
        documents = self.loader.load_directory(data_dir, recursive=True)
        logger.info(f"Loaded {len(documents)} documents")
        
        if not documents:
            logger.error("No documents found!")
            return
        
        # Step 2: Chunk documents
        logger.info("Step 2: Chunking documents...")
        chunks = self.chunker.chunk_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        
        if not chunks:
            logger.error("No chunks created!")
            return
        
        # Get chunk statistics
        stats = self.chunker.get_chunk_stats(chunks)
        logger.info(f"Chunk stats: {stats}")
        
        # Step 3: Generate embeddings
        logger.info("Step 3: Generating embeddings...")
        chunk_texts = [chunk['content'] for chunk in chunks]
        embeddings = self.embedder.generate_embeddings(
            chunk_texts,
            batch_size=32,
            show_progress=True
        )
        logger.info(f"Generated embeddings with shape: {embeddings.shape}")
        
        # Step 4: Build FAISS index
        logger.info("Step 4: Building FAISS index...")
        self.faiss_manager.add_documents(embeddings, chunks)
        
        # Step 5: Save index
        logger.info("Step 5: Saving index...")
        if save_path:
            self.faiss_manager.save_index(save_path)
        else:
            self.faiss_manager.save_index()
        
        # Get final statistics
        index_stats = self.faiss_manager.get_stats()
        
        # Calculate time taken
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Save metadata
        metadata = {
            'build_date': end_time.isoformat(),
            'duration_seconds': duration,
            'num_documents': len(documents),
            'num_chunks': len(chunks),
            'chunk_stats': stats,
            'index_stats': index_stats,
            'data_directory': str(data_dir)
        }
        
        metadata_path = (save_path or VECTOR_STORE_DIR / 'faiss_index').with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"\n{'='*60}")
        logger.info("INDEX BUILD COMPLETE!")
        logger.info(f"{'='*60}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Documents: {len(documents)}")
        logger.info(f"Chunks: {len(chunks)}")
        logger.info(f"Embeddings: {embeddings.shape}")
        logger.info(f"Index saved to: {save_path or VECTOR_STORE_DIR / 'faiss_index'}")
        logger.info(f"Metadata saved to: {metadata_path}")
        logger.info(f"{'='*60}\n")
        
        return metadata


def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Build FAISS index from documents')
    parser.add_argument(
        '--data-dir',
        type=Path,
        default=RAW_DATA_DIR,
        help='Directory containing documents'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Output path for index'
    )
    
    args = parser.parse_args()
    
    # Create logs directory
    Path('logs').mkdir(exist_ok=True)
    
    # Build index
    builder = IndexBuilder()
    
    try:
        metadata = builder.build_index(args.data_dir, args.output)
        
        print("\n✅ Index built successfully!")
        print(f"\nQuick Stats:")
        print(f"  Documents: {metadata['num_documents']}")
        print(f"  Chunks: {metadata['num_chunks']}")
        print(f"  Duration: {metadata['duration_seconds']:.2f}s")
        print(f"\nYou can now use the index for queries!")
        
    except Exception as e:
        logger.error(f"Error building index: {str(e)}", exc_info=True)
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
