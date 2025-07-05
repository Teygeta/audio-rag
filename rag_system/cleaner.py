import os
import sys
import curses
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

def get_all_documents(collection_name: str = "transcriptions_collection"):
    """
    Retrieves all documents (ID, content, metadata) from a ChromaDB collection.
    """
    try:
        db = Chroma(persist_directory="chroma_db", embedding_function=embeddings, collection_name=collection_name)
        all_ids = db.get(include=[])['ids']
        
        if not all_ids:
            return []

        all_docs_data = db.get(ids=all_ids, include=['documents', 'metadatas'])
        documents = []
        for i in range(len(all_docs_data['ids'])):
            documents.append({
                'id': all_docs_data['ids'][i],
                'content': all_docs_data['documents'][i],
                'metadata': all_docs_data['metadatas'][i]
            })
        return documents

    except Exception as e:
        # This error can occur if the DB is empty or not initialized correctly
        print(f"Error retrieving documents from ChromaDB: {e}", file=sys.stderr)
        return []

def display_documents_cli(documents):
    """
    Prints documents in a readable format for CLI mode.
    """
    if not documents:
        print("No documents to display.")
        return {}

    print(f"Found {len(documents)} documents in the collection.")
    print("\n--- Documents in the database ---")

    indexed_docs = {}
    for i, doc_data in enumerate(documents):
        doc_id = doc_data['id']
        content_snippet = doc_data['content'][:100].replace("\n", " ") + "..." if doc_data['content'] else ""
        source = doc_data['metadata'].get('source', 'N/A')
        indexed_at = doc_data['metadata'].get('indexed_at', 'N/A')
        print(f'{i+1}. ID: {doc_id}, Source: {source}, Indexed At: {indexed_at}, Content: "{content_snippet}"')
        indexed_docs[str(i+1)] = doc_id
    return indexed_docs

def delete_documents(ids_to_delete: list, collection_name: str = "transcriptions_collection"):
    """
    Deletes specified documents from the ChromaDB database.
    """
    if not ids_to_delete:
        print("No IDs provided for deletion.")
        return

    try:
        db = Chroma(persist_directory="chroma_db", embedding_function=embeddings, collection_name=collection_name)
        print(f"\nDeleting {len(ids_to_delete)} documents...")
        db.delete(ids=ids_to_delete)
        print("Documents deleted successfully.")

    except Exception as e:
        print(f"Error deleting documents from ChromaDB: {e}", file=sys.stderr)

def interactive_main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True) # Don't block waiting for input
    stdscr.clear()
    stdscr.refresh()

    documents = get_all_documents()
    if not documents:
        stdscr.addstr(0, 0, "No documents found in the database.")
        stdscr.addstr(1, 0, "Press any key to exit.")
        stdscr.getch()
        return

    current_row = 0
    selected_docs = set() # Set of selected document IDs for deletion

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        title = "--- ChromaDB Document Management (Press 'q' to quit, Space to select/deselect, Enter to delete) ---"
        stdscr.addstr(0, 0, title)

        start_row = 2
        for idx, doc_data in enumerate(documents):
            doc_id = doc_data['id']
            content_snippet = doc_data['content'][:w-20].replace("\n", " ") + "..." if doc_data['content'] else ""
            source = doc_data['metadata'].get('source', 'N/A')
            indexed_at = doc_data['metadata'].get('indexed_at', 'N/A')

            display_string = f"[{'X' if doc_id in selected_docs else ' '}] {idx+1}. Source: {source}, Indexed At: {indexed_at}, Content: \"{content_snippet}\" ".encode('utf-8', 'ignore').decode('utf-8')
            
            # Truncate the string if it's longer than the terminal width
            if len(display_string) >= w:
                display_string = display_string[:w-1]

            if idx == current_row:
                stdscr.attron(curses.A_REVERSE)
                stdscr.addstr(start_row + idx, 0, display_string)
                stdscr.attroff(curses.A_REVERSE)
            else:
                stdscr.addstr(start_row + idx, 0, display_string)
        
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP:
            current_row = max(0, current_row - 1)
        elif key == curses.KEY_DOWN:
            current_row = min(len(documents) - 1, current_row + 1)
        elif key == ord(' '): # Spacebar
            doc_id_to_toggle = documents[current_row]['id']
            if doc_id_to_toggle in selected_docs:
                selected_docs.remove(doc_id_to_toggle)
            else:
                selected_docs.add(doc_id_to_toggle)
        elif key == curses.KEY_ENTER or key == 10: # Enter
            if selected_docs:
                # Ask for confirmation before deleting
                stdscr.addstr(h-2, 0, f"Confirm deletion of {len(selected_docs)} documents? (y/n)")
                stdscr.refresh()
                confirm_key = stdscr.getch()
                while confirm_key not in [ord('y'), ord('n')]:
                    confirm_key = stdscr.getch()
                
                if confirm_key == ord('y'):
                    delete_documents(list(selected_docs))
                    # Reload documents after deletion
                    documents = get_all_documents()
                    selected_docs.clear()
                    current_row = 0 # Reset selection
                    stdscr.addstr(h-1, 0, "Documents deleted. Press any key to continue.")
                    stdscr.getch()
                else:
                    stdscr.addstr(h-1, 0, "Deletion cancelled. Press any key to continue.")
                    stdscr.getch()
                stdscr.clear() # Clear confirmation message
                stdscr.refresh()


import shutil

def delete_full_db():
    """
    Deletes the entire ChromaDB directory.
    Asks for user confirmation unless DEV_MODE is set to 'true'.
    """
    chroma_db_path = "chroma_db"
    if not os.path.exists(chroma_db_path):
        print(f"ChromaDB directory '{chroma_db_path}' does not exist. Nothing to delete.")
        return

    confirm = input(f"Are you sure you want to delete the entire ChromaDB directory ('{chroma_db_path}')? This action cannot be undone. (yes/no): ").lower()
    if confirm == "yes":
        print(f"Deleting '{chroma_db_path}'...")
        shutil.rmtree(chroma_db_path)
        print(f"ChromaDB directory '{chroma_db_path}' deleted.")
    else:
        print("Deletion cancelled.")

if __name__ == "__main__":
    # If command line arguments are provided, use CLI mode
    if len(sys.argv) >= 2:
        command = sys.argv[1]
        if command == "list":
            documents = get_all_documents()
            display_documents_cli(documents)
        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Specify document IDs to delete.", file=sys.stderr)
                sys.exit(1)
            ids_to_delete = sys.argv[2:]
            delete_documents(ids_to_delete)
        elif command == "delete-all":
            delete_full_db()
        else:
            print(f"Unrecognized command: {command}", file=sys.stderr)
            sys.exit(1)
    else: # No arguments, try interactive mode with curses
        if sys.platform == "win32":
            print("Interactive mode is not supported on Windows. Use: python cleaner.py [list | delete <id1> ... | delete-all]", file=sys.stderr)
            sys.exit(1)
        try:
            curses.wrapper(interactive_main)
        except curses.error as e:
            print(f"Error initializing curses: {e}", file=sys.stderr)
            print("Interactive mode requires a curses-compatible terminal. Use: python cleaner.py [list | delete <id1> ... | delete-all]", file=sys.stderr)
            sys.exit(1)