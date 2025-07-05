import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

load_dotenv()

# Configure API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

# Initialize OpenAI embedding model
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))

def index_transcription(transcription_path: str, collection_name: str = "transcriptions_collection"):
    """
    Indexes a single transcription into the ChromaDB vector database.
    The collection name is 'transcriptions_collection' by default.
    """
    print(f"\nStarting transcription indexing: {transcription_path}")

    # Load transcription content
    with open(transcription_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Chunk size
        chunk_overlap=200 # Overlap between chunks to maintain context
    )
    chunks = text_splitter.create_documents([text])

    # Add metadata to chunks (e.g., original file name and indexed timestamp)
    from datetime import datetime
    indexed_at = datetime.now().isoformat()
    for chunk in chunks:
        chunk.metadata = {"source": os.path.basename(transcription_path), "indexed_at": indexed_at}

    # Initialize ChromaDB (creates or connects to the local DB)
    # The DB will be saved in the 'chroma_db' folder in the project root
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="chroma_db",
        collection_name=collection_name
    )

    print(f"Indexing completed for {transcription_path}. {len(chunks)} chunks added.")

if __name__ == "__main__":
    # Example usage (to test the indexer directly)
    # Make sure you have a transcription file in the 'transcriptions/' folder
    # and that your API keys are set in .env
    
    # Find the latest created transcription file
    transcriptions_dir = os.path.join(os.getcwd(), "transcriptions")
    if os.path.exists(transcriptions_dir):
        transcription_files = [os.path.join(transcriptions_dir, f) for f in os.listdir(transcriptions_dir) if f.endswith('.txt')]
        if transcription_files:
            # Sort by modification date (most recent)
            transcription_files.sort(key=os.path.getmtime, reverse=True)
            latest_transcription = transcription_files[0]
            index_transcription(latest_transcription)
        else:
            print("No transcription file found in the 'transcriptions/' folder.")
    else:
        print("The 'transcriptions/' folder does not exist.")