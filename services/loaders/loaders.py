from services.loaders.ics_loader import ICSLoader
from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    CSVLoader,
    JSONLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    UnstructuredEmailLoader,
)

# Map file extensions to LangChain loader classes
EXTENSION_LOADER_MAP = {
    ".txt": TextLoader,
    ".md": TextLoader,
    ".pdf": PyPDFLoader,
    ".docx": UnstructuredWordDocumentLoader,
    ".csv": CSVLoader,
    ".json": JSONLoader,
    ".pptx": UnstructuredPowerPointLoader,
    ".xlsx": UnstructuredExcelLoader,
    ".eml": UnstructuredEmailLoader,
    ".ics": ICSLoader,
    # Extend this mapping for other formats (e.g., .pptx, .ipynb).
}
