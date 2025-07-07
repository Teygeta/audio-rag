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

def verify_chroma_db(collection_name: str = "transcriptions_collection"):
    """
    Loads the ChromaDB database and prints some of the indexed documents.
    """
    print(f"\nLoading ChromaDB from collection: {collection_name}")

    try:
        # Connects to the existing DB
        db = Chroma(persist_directory="chroma_db", embedding_function=embeddings, collection_name=collection_name)

        # Count the number of documents in the collection
        count = db.get(include=[])['ids']
        print(f"Found {len(count)} documents in collection '{collection_name}'.")

        if len(count) > 0:
            print("Performing a generic similarity search to show some data:")
            # Performs a generic similarity search with a generic query
            # This will retrieve the most relevant documents for the query
            results = db.similarity_search("information", k=5) # Retrieve the first 5 results

            for i, doc in enumerate(results):
                indexed_at = doc.metadata.get('indexed_at', 'N/A')
                print(f"\n--- Document {i+1} ---")
                print(f"Content: {doc.page_content[:200]}...") # Show the first 200 characters
                print(f"Metadata: {doc.metadata}")
                print(f"Indexed At: {indexed_at}")
        else:
            print("The collection is empty. No documents to show.")

    except Exception as e:
        print(f"Error verifying ChromaDB: {e}", file=sys.stderr)

def main():
    verify_chroma_db()

if __name__ == "__main__":
    main()
