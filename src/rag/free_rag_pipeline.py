"""
Free RAG Pipeline using Hugging Face models
"""
import logging
from typing import Dict, List, Any

from src.embeddings.embedding_model import EmbeddingGenerator
from src.vector_store.faiss_manager import FAISSManager
from src.llm.free_llm_client import FreeLLMClient, FastFreeLLMClient

logger = logging.getLogger(__name__)


class FreeRAGPipeline:
    """
    Complete RAG pipeline using free components
    """
    
    def __init__(self, use_fast_model: bool = False):
        """
        Initialize RAG pipeline
        
        Args:
            use_fast_model: Use faster but smaller model
        """
        logger.info("Initializing Free RAG Pipeline...")
        
        # Initialize components
        self.embedder = EmbeddingGenerator()
        self.faiss = FAISSManager()
        
        # Choose LLM
        if use_fast_model:
            self.llm = FastFreeLLMClient()
            logger.info("Using fast model for quick responses")
        else:
            try:
                self.llm = FreeLLMClient()
                logger.info("Using IBM Granite model")
            except:
                logger.warning("Granite not available, using fast model")
                self.llm = FastFreeLLMClient()
        
        # Load FAISS index
        try:
            self.faiss.load_index()
            logger.info("FAISS index loaded successfully")
        except FileNotFoundError:
            logger.warning("FAISS index not found. Run build_index.py first!")
    
    def query(self, question: str, k: int = 3) -> Dict[str, Any]:
        """
        Process user query through RAG pipeline
        
        Args:
            question: User's question
            k: Number of documents to retrieve
            
        Returns:
            Dictionary with answer and sources
        """
        logger.info(f"Processing query: {question}")
        
        try:
            # Step 1: Generate query embedding
            logger.info("Generating query embedding...")
            query_embedding = self.embedder.generate_embedding(question)
            
            # Step 2: Search for similar documents
            logger.info(f"Searching for top-{k} similar documents...")
            results = self.faiss.search(query_embedding, k=k, threshold=0.5)
            
            if not results:
                return {
                    'answer': "I don't have enough information to answer that question. Please try rephrasing or ask about waste management, water conservation, or energy efficiency.",
                    'sources': [],
                    'question': question,
                    'confidence': 'low'
                }
            
            # Step 3: Build context from retrieved documents
            logger.info("Building context...")
            context_parts = []
            sources = []
            
            for doc, score in results:
                context_parts.append(doc['content'])
                sources.append({
                    'content': doc['content'][:200] + "...",
                    'metadata': doc['metadata'],
                    'relevance_score': float(score)
                })
            
            context = "\n\n".join(context_parts)
            
            # Step 4: Create prompt
            prompt = self._build_prompt(context, question)
            
            # Step 5: Generate response
            logger.info("Generating AI response...")
            answer = self.llm.generate(
                prompt,
                max_new_tokens=512,
                temperature=0.3
            )
            
            # Step 6: Format result
            result = {
                'answer': answer,
                'sources': sources,
                'question': question,
                'confidence': 'high' if len(results) >= 2 else 'medium',
                'num_sources': len(sources)
            }
            
            logger.info("Query processed successfully")
            return result
        
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                'answer': f"Sorry, I encountered an error: {str(e)}",
                'sources': [],
                'question': question,
                'confidence': 'error'
            }
    
    def _build_prompt(self, context: str, question: str) -> str:
        """Build RAG prompt"""
        prompt = f"""You are SustainSphere AI, a helpful sustainability advisor. Answer the question based ONLY on the provided context. Be specific and actionable.

Context from sustainability documents:
{context}

Question: {question}

Instructions:
- Provide clear, practical advice
- Include specific actions the user can take
- Be concise but comprehensive
- If the context doesn't fully answer the question, say so

Answer:"""
        
        return prompt


def main():
    """Test the RAG pipeline"""
    import sys
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create pipeline
    print("\n🚀 Initializing Free RAG Pipeline...")
    pipeline = FreeRAGPipeline(use_fast_model=False)
    
    # Test questions
    questions = [
        "How can I reduce plastic waste at home?",
        "What are the best ways to conserve water?",
        "How do I start composting?"
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")
        
        result = pipeline.query(question)
        
        print(f"\n📝 Answer:\n{result['answer']}")
        print(f"\n📚 Sources: {result['num_sources']}")
        print(f"🎯 Confidence: {result['confidence']}")
        
        if result['sources']:
            print("\nSource details:")
            for i, source in enumerate(result['sources'], 1):
                print(f"  {i}. {source['metadata'].get('filename', 'Unknown')}")
                print(f"     Relevance: {source['relevance_score']:.2f}")


if __name__ == "__main__":
    main()

# Made with Bob
