# 🌍 SustainSphere AI

**A RAG-Powered Sustainability Advisor using IBM Granite**

An AI-powered web application that provides evidence-based sustainability advice by combining Retrieval-Augmented Generation (RAG) with IBM Granite LLM, helping students, households, and communities make informed decisions about waste management, water conservation, energy efficiency, and climate action.

---

## 📋 Project Overview

**Internship**: 1M1B AI for Sustainability Virtual Internship  
**Primary SDG**: SDG 12 - Responsible Consumption and Production  
**Secondary SDGs**: SDG 11 (Sustainable Cities), SDG 13 (Climate Action)

### Problem Statement

Many students, households, and communities struggle to find reliable and actionable sustainability information. Existing resources are scattered, technical, or not personalized to their specific context.

### Solution

SustainSphere AI uses Retrieval-Augmented Generation (RAG) to answer sustainability questions by:
1. Retrieving relevant information from curated sustainability documents
2. Using IBM Granite LLM to generate accurate, contextual responses
3. Providing source citations for transparency and trust

---

## ✨ Features

- 🤖 **AI-Powered Q&A**: Ask any sustainability question in natural language
- 📚 **Evidence-Based**: Answers backed by trusted sustainability documents
- 🎯 **SDG-Focused**: Organized by UN Sustainable Development Goals
- 🔍 **Source Citations**: See exactly where information comes from
- 💬 **Interactive Chat**: User-friendly Streamlit interface
- ⚡ **Fast Responses**: Optimized RAG pipeline for quick answers
- 🌱 **Actionable Advice**: Practical recommendations you can implement

---

## 🏗️ Architecture

```
User Query → Embedding → FAISS Search → Context Retrieval → IBM Granite → Response
                ↓                              ↓
         Vector Database              Sustainability Documents
```

### Technology Stack

- **LLM**: IBM Granite (via watsonx.ai API)
- **Framework**: LangChain for RAG orchestration
- **Vector Store**: FAISS for similarity search
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Frontend**: Streamlit
- **Language**: Python 3.9+

---

## 📁 Project Structure

```
SustainSphere-AI/
├── src/
│   ├── config/              # Configuration settings
│   ├── data_processing/     # Document loading and chunking
│   ├── embeddings/          # Embedding generation
│   ├── vector_store/        # FAISS operations
│   ├── llm/                 # IBM Granite integration
│   └── rag/                 # RAG pipeline
├── app/                     # Streamlit application
├── data/
│   ├── raw/                 # Original documents
│   ├── processed/           # Chunked documents
│   └── vector_store/        # FAISS index
├── scripts/                 # Utility scripts
├── tests/                   # Test suite
└── docs/                    # Documentation
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- 8GB RAM minimum
- Internet connection (for API access)
- IBM Cloud account (free tier available)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/SustainSphere-AI.git
cd SustainSphere-AI
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy example env file
copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

# Edit .env and add your IBM credentials:
# IBM_API_KEY=your_api_key_here
# IBM_PROJECT_ID=your_project_id_here
```

### Get IBM watsonx.ai Credentials

1. Sign up for IBM Cloud: https://cloud.ibm.com/registration
2. Create a watsonx.ai project
3. Get your API key from IBM Cloud dashboard
4. Get your project ID from watsonx.ai project settings

---

## 📚 Usage

### Step 1: Prepare Documents

Place your sustainability documents in the `data/raw/` directory:

```
data/raw/
├── sdg_11_sustainable_cities/
│   └── urban_planning.pdf
├── sdg_12_responsible_consumption/
│   ├── waste_management.pdf
│   └── circular_economy.pdf
└── sdg_13_climate_action/
    └── carbon_footprint.pdf
```

### Step 2: Build the Index

```bash
python scripts/build_index.py
```

This will:
- Load all documents from `data/raw/`
- Split them into chunks
- Generate embeddings
- Create FAISS index
- Save to `data/vector_store/`

Expected output:
```
✅ Index built successfully!

Quick Stats:
  Documents: 10
  Chunks: 245
  Duration: 45.23s
```

### Step 3: Run the Application

```bash
streamlit run app/main.py
```

The app will open in your browser at `http://localhost:8501`

### Step 4: Ask Questions!

Try these example questions:
- "How can I reduce plastic waste at home?"
- "What are the best ways to conserve water?"
- "How do I start composting?"
- "What is a circular economy?"

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/unit/test_document_loader.py
```

### Test Individual Components

```bash
# Test document loader
python src/data_processing/document_loader.py data/raw/sample.pdf

# Test text splitter
python src/data_processing/text_splitter.py data/raw/sample.pdf

# Test embeddings
python src/embeddings/embedding_model.py "test query"

# Test FAISS manager
python src/vector_store/faiss_manager.py
```

---

## 📖 Documentation

Comprehensive documentation is available:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Complete system architecture and design
- **[INTERNSHIP_SUBMISSION.md](INTERNSHIP_SUBMISSION.md)** - Full project documentation for 1M1B internship

---

## 🎯 Development Roadmap

### Week 1: Core Implementation ✅
- [x] Project architecture design
- [x] Document processing pipeline
- [x] Embedding generation
- [x] FAISS vector store
- [x] Index building script

### Week 2: RAG & LLM Integration
- [ ] IBM Granite client
- [ ] Prompt engineering
- [ ] RAG query pipeline
- [ ] Response formatting

### Week 3: Frontend Development
- [ ] Streamlit UI
- [ ] Chat interface
- [ ] Source display
- [ ] SDG filtering

### Week 4: Testing & Polish
- [ ] Unit tests
- [ ] Integration tests
- [ ] Documentation
- [ ] Demo preparation

---

## 🔧 Configuration

### Key Settings (src/config/settings.py)

```python
# Embedding Model
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# Text Chunking
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval
TOP_K_DOCUMENTS = 3
SIMILARITY_THRESHOLD = 0.7

# IBM Granite
GRANITE_MODEL_ID = "ibm/granite-13b-chat-v2"
GENERATION_CONFIG = {
    "temperature": 0.3,
    "max_new_tokens": 512,
    "top_p": 0.9,
}
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: Import errors when running scripts
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**Issue**: FAISS installation fails
```bash
# Solution: Install via conda
conda install -c conda-forge faiss-cpu
```

**Issue**: Out of memory during indexing
```bash
# Solution: Reduce batch size in settings.py
# Or process documents in smaller batches
```

**Issue**: IBM API authentication fails
```bash
# Solution: Check your .env file
# Ensure IBM_API_KEY and IBM_PROJECT_ID are correct
```

---

## 📊 Performance

### Expected Performance (8GB RAM System)

- **Index Building**: ~1-2 minutes for 10 documents
- **Query Response Time**: 2-3 seconds
- **Memory Usage**: ~2-3 GB
- **Concurrent Users**: 5-10 (local deployment)

### Optimization Tips

1. **Use API approach** for IBM Granite (recommended for 8GB RAM)
2. **Batch process** documents during indexing
3. **Cache embeddings** for frequently asked questions
4. **Limit context window** to reduce LLM processing time

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **1M1B Foundation** for the AI for Sustainability Internship opportunity
- **IBM** for providing Granite LLM and watsonx.ai platform
- **LangChain** for the excellent RAG framework
- **Hugging Face** for sentence transformers
- **Streamlit** for the amazing web framework

---

## 📞 Contact

**Project Maintainer**: [Your Name]  
**Email**: your.email@example.com  
**LinkedIn**: [Your LinkedIn Profile]  
**GitHub**: [Your GitHub Profile]

---

## 🌟 Star History

If you find this project helpful, please consider giving it a star ⭐

---

## 📈 Project Status

**Current Version**: 1.0.0  
**Status**: Active Development  
**Last Updated**: June 2024

### Completed Features
✅ Document processing pipeline  
✅ Embedding generation  
✅ FAISS vector store  
✅ Index building  
✅ Comprehensive documentation  

### In Progress
🔄 IBM Granite integration  
🔄 RAG query pipeline  
🔄 Streamlit UI  

### Planned Features
📋 Conversation history  
📋 User feedback system  
📋 Multi-language support  
📋 Mobile-responsive design  

---

## 🎓 Learning Resources

### RAG & LLMs
- [LangChain Documentation](https://python.langchain.com/)
- [IBM Granite Models](https://www.ibm.com/products/watsonx-ai)
- [RAG Explained](https://www.pinecone.io/learn/retrieval-augmented-generation/)

### Sustainability
- [UN SDGs](https://sdgs.un.org/)
- [EPA Sustainability Resources](https://www.epa.gov/sustainability)
- [Circular Economy Principles](https://ellenmacarthurfoundation.org/)

---

<div align="center">

**Built with ❤️ for a sustainable future 🌍**

[Report Bug](https://github.com/yourusername/SustainSphere-AI/issues) · [Request Feature](https://github.com/yourusername/SustainSphere-AI/issues) · [Documentation](docs/)

</div>