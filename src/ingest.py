import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Configuration
KNOWLEDGE_BASE_DIR = "./data/knowledge_base"
VECTOR_DB_DIR = "./data/vector_db"
# Using a small embedding model ideal for mobile/local devices
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def ingest_data():
    print("🧠 Starting Data Ingestion Process...")

    if not os.path.exists(KNOWLEDGE_BASE_DIR) or not os.listdir(KNOWLEDGE_BASE_DIR):
        print(f"⚠️  No files found in {KNOWLEDGE_BASE_DIR}. Please add some files (.txt, .md, .py, .js) to ingest.")
        return

    # 1. Load documents
    print(f"📂 Loading documents from {KNOWLEDGE_BASE_DIR}...")
    # Using TextLoader for simplicity; can be expanded to PDFLoader, etc.
    loader = DirectoryLoader(KNOWLEDGE_BASE_DIR, glob="**/*.*", loader_cls=TextLoader, use_multithreading=True)
    documents = loader.load()
    print(f"📄 Loaded {len(documents)} documents.")

    # 2. Split text into chunks
    print("✂️  Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"🧩 Split into {len(chunks)} chunks.")

    # 3. Create Embeddings & Store in Vector DB
    print(f"🧮 Loading Embedding Model: {EMBEDDING_MODEL_NAME} (this might take a moment on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    print("💾 Saving to Chroma Vector Database...")
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_DIR
    )

    print("✅ Ingestion Complete! Data is safely stored in the Vector DB.")

if __name__ == "__main__":
    ingest_data()
