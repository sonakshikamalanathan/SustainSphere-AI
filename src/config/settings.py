"""
Configuration settings for SustainSphere AI
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
VECTOR_STORE_DIR = DATA_DIR / "vector_store"

# Create directories if they don't exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)

# Embedding model settings
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Text splitting settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# FAISS settings
FAISS_INDEX_NAME = "sustainability_index"
FAISS_INDEX_TYPE = "Flat"  # Options: "Flat", "IVF", "HNSW"
FAISS_INDEX_PATH = VECTOR_STORE_DIR / f"{FAISS_INDEX_NAME}.faiss"
FAISS_METADATA_PATH = VECTOR_STORE_DIR / f"{FAISS_INDEX_NAME}_metadata.pkl"
TOP_K_DOCUMENTS = 3  # Number of documents to retrieve
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score

# LLM settings
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
LLM_MODEL_NAME = "ibm-granite/granite-3.0-8b-instruct"
LLM_MAX_TOKENS = 512
LLM_TEMPERATURE = 0.7

# RAG settings
TOP_K_RESULTS = 3
CONTEXT_WINDOW = 2000

# Streamlit settings
APP_TITLE = "SustainSphere AI"
APP_ICON = "🌍"
PAGE_LAYOUT = "wide"

# Supported file types
SUPPORTED_FILE_TYPES = [".txt", ".pdf", ".docx"]
SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".docx"]  # Alias for compatibility

# File size limits
MAX_FILE_SIZE_MB = 50

# Logging
LOG_LEVEL = "INFO"

# Made with Bob
