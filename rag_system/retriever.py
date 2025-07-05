import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

# Configure API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

# Initialize OpenAI embedding model (must be the same used for indexing)
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"))

def query_chroma_db(query: str, collection_name: str = "transcriptions_collection", k: int = 5):
    """
    Queries the ChromaDB database with a given string and returns the results.
    """
    try:
        db = Chroma(persist_directory="chroma_db", embedding_function=embeddings, collection_name=collection_name)
        results = db.similarity_search(query, k=k)
        return results
    except Exception as e:
        print(f"Error querying ChromaDB: {e}", file=sys.stderr)
        return []