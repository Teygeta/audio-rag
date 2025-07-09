# Audio-RAG Project

This project implements a Retrieval Augmented Generation (RAG) system for audio/video content. It allows you to transcribe multimedia files, index the resulting text into a vector database (ChromaDB), and query the database to find relevant information.

## Setup

Follow these steps to set up the project on your system:

1.  **Clone the repository:**

    ```bash
    git clone <repository URL>
    cd audio-rag # or the project directory name
    ```

2.  **Run the cross-platform setup script:**

    ```bash
    python -m setup_project
    ```

    This script will create a virtual environment (`.venv`), install necessary dependencies, and guide you through configuring API keys in the `.env` file.

3.  **Activate the virtual environment:**

    -   On Linux/macOS:

        ```bash
        source .venv/bin/activate
        ```

    -   On Windows:

        ```bash
        .venv\Scripts\activate
        ```

    Ensure the virtual environment is active whenever you work on the project (you will see `(.venv)` at the beginning of your terminal prompt).

## Usage

Once the setup is complete and the virtual environment is activated, you can use the following scripts:

*   **`setup_project.py`**: Performs the initial project setup (venv creation, dependency installation, .env configuration). Useful if you need to reconfigure the environment.

    ```bash
    python setup_project.py
    ```

*   **`verify_setup.py`**: Verifies that the setup environment is correct (Python version, dependencies, FFmpeg, API keys, ChromaDB directory).

    ```bash
    python verify_setup.py
    ```

*   **`app_query.py`**: Executes the logic for querying the indexed database.

    ```bash
    python app_query.py "Your query here"
    ```

*   **`app_upload.py`**: Executes the logic for uploading and ingesting new audio/video files for transcription and indexing.

    ```bash
    python app_upload.py <path_to_audio/video_file>
    ```

*   **`rag_system/verifier.py`**: Displays the content of the ChromaDB database.

    ```bash
    python rag_system/verifier.py
    ```

*   **`rag_system/cleaner.py`**: Allows managing the ChromaDB database. Supports the following subcommands:

    -   List documents:

        ```bash
        python rag_system/cleaner.py list
        ```

    -   Delete specific documents by ID:

        ```bash
        python rag_system/cleaner.py delete <id1> <id2> ...
        ```

    -   Delete the entire database:

        ```bash
        python rag_system/cleaner.py delete-all
        ```

## Language Model Configuration

This project supports using either the Google Gemini model or a local model via Ollama.

To configure which model to use, set the `LLM_TYPE` environment variable in your `.env` file. It can be either `gemini` (default) or `ollama`.

### Using Google Gemini

Set `LLM_TYPE=gemini` in your `.env` file and ensure your `GOOGLE_API_KEY` is set.

### Using Ollama

1.  Install Ollama from [https://ollama.com/](https://ollama.com/).
2.  Pull the desired model (e.g., `ollama pull llama2`).
3.  Set `LLM_TYPE=ollama` in your `.env` file.
4.  Optionally, set `OLLAMA_MODEL` in your `.env` file to specify the model name (defaults to `llama2`).
5.  Ensure you have installed the necessary dependencies by running `python setup_project.py` (this will install `langchain-community`).

