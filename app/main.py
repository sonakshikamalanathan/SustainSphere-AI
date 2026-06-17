"""
SustainSphere AI - Free Streamlit Application
"""
import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.rag.free_rag_pipeline import FreeRAGPipeline

# Page config
st.set_page_config(
    page_title="SustainSphere AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize RAG pipeline
@st.cache_resource
def load_pipeline():
    """Load RAG pipeline (cached)"""
    return FreeRAGPipeline(use_fast_model=False)

# Header
st.markdown('<h1 class="main-header">🌍 SustainSphere AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Free AI-Powered Sustainability Advisor</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("ℹ️ About")
    st.write("""
    **SustainSphere AI** uses Retrieval-Augmented Generation (RAG) with IBM Granite to provide evidence-based sustainability advice.
    
    **Features:**
    - 🤖 AI-powered responses
    - 📚 Evidence-based answers
    - 🎯 SDG-aligned advice
    - 🆓 Completely free!
    """)
    
    st.header("🎯 SDG Focus")
    st.write("""
    - **SDG 12**: Responsible Consumption
    - **SDG 11**: Sustainable Cities
    - **SDG 13**: Climate Action
    """)
    
    st.header("💡 Example Questions")
    example_questions = [
        "How can I reduce plastic waste?",
        "What are ways to conserve water?",
        "How do I start composting?",
        "What is a circular economy?",
        "How can I save energy at home?"
    ]
    
    for q in example_questions:
        if st.button(q, key=q):
            st.session_state.example_question = q

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pipeline" not in st.session_state:
    with st.spinner("🔄 Loading AI model..."):
        try:
            st.session_state.pipeline = load_pipeline()
            st.success("✅ AI model loaded!")
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            st.info("💡 Make sure you've run `python scripts/build_index.py` first!")
            st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
        # Show sources for assistant messages
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 View Sources"):
                for i, source in enumerate(message["sources"], 1):
                    st.markdown(f"""
                    <div class="source-box">
                        <strong>Source {i}:</strong> {source['metadata'].get('filename', 'Unknown')}<br>
                        <strong>Relevance:</strong> {source['relevance_score']:.0%}<br>
                        <em>{source['content']}</em>
                    </div>
                    """, unsafe_allow_html=True)

# Handle example question from sidebar
if "example_question" in st.session_state:
    prompt = st.session_state.example_question
    del st.session_state.example_question
else:
    # Chat input
    prompt = st.chat_input("Ask a sustainability question...")

if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                result = st.session_state.pipeline.query(prompt)
                
                # Display answer
                st.write(result['answer'])
                
                # Display sources
                if result['sources']:
                    with st.expander("📚 View Sources"):
                        for i, source in enumerate(result['sources'], 1):
                            st.markdown(f"""
                            <div class="source-box">
                                <strong>Source {i}:</strong> {source['metadata'].get('filename', 'Unknown')}<br>
                                <strong>Relevance:</strong> {source['relevance_score']:.0%}<br>
                                <em>{source['content']}</em>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Add assistant message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result['answer'],
                    "sources": result['sources']
                })
            
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Try rephrasing your question or check if the index is built.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🌍 Built for the 1M1B AI for Sustainability Internship</p>
    <p>Powered by IBM Granite • RAG • Hugging Face • FAISS</p>
</div>
""", unsafe_allow_html=True)

# Made with Bob
