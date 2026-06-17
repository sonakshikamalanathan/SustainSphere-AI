"""
Document loader for various file formats
"""
import logging
from pathlib import Path
from typing import List, Dict, Any
import pypdf
from docx import Document

from src.config.settings import SUPPORTED_EXTENSIONS, MAX_FILE_SIZE_MB

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Load documents from various file formats"""
    
    def __init__(self):
        self.supported_extensions = SUPPORTED_EXTENSIONS
        self.max_file_size_mb = MAX_FILE_SIZE_MB
    
    def load_pdf(self, file_path: Path) -> Dict[str, Any]:
        """Load PDF document"""
        try:
            logger.info(f"Loading PDF: {file_path}")
            
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                # Extract text from all pages
                text_content = []
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text.strip():
                        text_content.append({'page': page_num, 'content': text})
                
                full_text = "\n\n".join([page['content'] for page in text_content])
                
                metadata = {
                    'source': str(file_path),
                    'filename': file_path.name,
                    'file_type': 'pdf',
                    'num_pages': len(pdf_reader.pages),
                    'file_size_mb': file_path.stat().st_size / (1024 * 1024)
                }
                
                if pdf_reader.metadata:
                    metadata.update({
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                    })
                
                return {'content': full_text, 'metadata': metadata, 'pages': text_content}
                
        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {str(e)}")
            raise
    
    def load_text(self, file_path: Path) -> Dict[str, Any]:
        """Load text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            metadata = {
                'source': str(file_path),
                'filename': file_path.name,
                'file_type': 'txt',
                'file_size_mb': file_path.stat().st_size / (1024 * 1024)
            }
            
            return {'content': content, 'metadata': metadata}
            
        except Exception as e:
            logger.error(f"Error loading text file {file_path}: {str(e)}")
            raise
    
    def load_document(self, file_path: Path) -> Dict[str, Any]:
        """Load document based on file extension"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.max_file_size_mb:
            raise ValueError(f"File size exceeds maximum")
        
        extension = file_path.suffix.lower()
        
        if extension == '.pdf':
            return self.load_pdf(file_path)
        elif extension in ['.txt', '.md']:
            return self.load_text(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {extension}")
    
    def load_directory(self, directory_path: Path, recursive: bool = True) -> List[Dict[str, Any]]:
        """Load all supported documents from a directory"""
        directory_path = Path(directory_path)
        
        if not directory_path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        documents = []
        files = directory_path.rglob('*') if recursive else directory_path.glob('*')
        
        supported_files = [
            f for f in files 
            if f.is_file() and f.suffix.lower() in self.supported_extensions
        ]
        
        logger.info(f"Found {len(supported_files)} supported files")
        
        for file_path in supported_files:
            try:
                doc = self.load_document(file_path)
                documents.append(doc)
            except Exception as e:
                logger.warning(f"Skipping {file_path}: {str(e)}")
                continue
        
        return documents

# Made with Bob
