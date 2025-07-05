# MP4-RAG: Video/Audio Transcription, Indexing, and Retrieval

MP4-RAG is a Python-based application designed to process video and audio files, transcribe their content, index the transcriptions into a vector database, and allow users to query this knowledge base using Retrieval Augmented Generation (RAG). This system helps you extract valuable information from your multimedia content by making it searchable and queryable.

## Features

*   **Multimedia to Audio Conversion**: Converts various video and audio formats to MP3 using FFmpeg.
*   **AI-Powered Transcription**: Transcribes audio files using OpenAI's Whisper API.
*   **Smart Title Generation**: Generates concise and descriptive titles for transcriptions using Google's Gemini API.
*   **Vector Database Indexing**: Indexes transcribed content into a ChromaDB vector database for efficient semantic search.
*   **Retrieval Augmented Generation (RAG)**: Answers user queries by retrieving relevant information from the indexed transcriptions and generating responses using Google's Gemini API.
*   **Database Management**: Tools to list, delete specific, or clear the entire ChromaDB.
*   **Developer Mode**: Option to limit audio processing to the first 30 seconds for faster testing.

## Requirements

Before you begin, ensure you have the following installed on your system:

*   **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
*   **FFmpeg**: A powerful tool for multimedia processing.
    *   **macOS**: `brew install ffmpeg` (using Homebrew)
    *   **Linux**: `sudo apt update && sudo apt install ffmpeg`
    *   **Windows**: Follow instructions on the [FFmpeg website](https://ffmpeg.org/download.html)
*   **Git**: For cloning the repository.
    *   [Download Git](https://git-scm.com/downloads)

## Quick Start

To get started with MP4-RAG, follow these simple steps:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/mp4-rag.git # Replace with your actual repo URL
    cd mp4-rag
    ```

2.  **Run the setup**:
    ```bash
    make setup
    ```
    This command will set up a Python virtual environment, install all necessary dependencies, and guide you through configuring your environment variables.

3.  **Configure API Keys**:
    After running `make setup`, you will be prompted to create a `.env` file. Ensure you add your OpenAI and Google API keys to this file:
    ```dotenv
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    GOOGLE_API_KEY="YOUR_GOOGLE_API_KEY"
    ```
    **Note**: Obtain your API keys from [OpenAI](https://platform.openai.com/account/api-keys) and [Google AI Studio](https://aistudio.google.com/app/apikey).

## Usage

### 1. Upload and Transcribe a File

To process a video or audio file and add its transcription to the database, use the `upload` command:

```bash
make upload
```
This will open a file selection dialog, transcribe the selected file, generate a title, and index the transcription into the ChromaDB.

### 2. Query the Knowledge Base

To ask questions about your indexed transcriptions, use the `ask` command with your query:

```bash
make ask QUERY="What did the speaker say about their experience abroad?"
```
The system will retrieve relevant information and generate an answer using AI.

## Database Management

The `rag_system/cleaner.py` script provides utilities to manage your ChromaDB.

*   **Interactive Deletion (macOS/Linux only)** (`make clean-db`):
    Running `make clean-db` will launch an interactive interface, allowing you to select and delete documents from the database. This feature is available only on macOS and Linux.
    ```bash
    make clean-db
    ```

*   **List all indexed documents** (`make show-db`):
    ```bash
    make show-db
    ```

*   **Delete specific documents by ID**:
    (First, use `make show-db` to find the IDs)
    ```bash
    python3 rag_system/cleaner.py delete <document_id_1> <document_id_2> ...
    # Example: python3 rag_system/cleaner.py delete 1a2b3c4d5e6f 7g8h9i0j1k2l
    ```
    **Note**: On Windows, the interactive mode is not supported. You must use the `list` and `delete <id>` commands directly.

*   **Delete the entire database** (`make clean-full-db`):
    ```bash
    make clean-full-db
    ```
    **Warning**: This action is irreversible and will remove all indexed transcriptions.

## Development Mode

If you set `DEV_MODE="true"` in your `.env` file, the audio conversion process will be limited to the first 30 seconds of the input file. This is useful for quickly testing the transcription and indexing pipeline without processing large files entirely.

## Project Structure

```
.
├── app_query.py              # Handles querying the RAG system
├── app_upload.py             # Handles file upload and transcription flow
├── main.py                   # Main entry point for the application
├── Makefile                  # Convenience commands (e.g., `make upload`)
├── requirements.txt          # Python dependencies
├── setup.sh                  # Script for initial setup (e.g., installing pnpm)
├── verify_setup.py           # Script to verify environment setup
├── .env.example              # Example .env file
├── .gitignore                # Git ignore rules
├── logs/                     # Log files (ignored by Git)
├── chroma_db/                # Local ChromaDB storage (ignored by Git)
├── transcriptions/           # Stores final transcription text files (ignored by Git)
├── temp/                     # Temporary files during processing (ignored by Git)
├── rag_system/
│   ├── cleaner.py            # Tools for managing the ChromaDB
│   ├── indexer.py            # Handles indexing transcriptions into ChromaDB
│   ├── retriever.py          # Handles retrieving relevant documents from ChromaDB
│   └── verifier.py           # Verifies ChromaDB integrity
└── transcription_pipeline/
    ├── logger.py             # Logs API usage
    ├── transcriber.py        # Core transcription and title generation logic
    └── utils.py              # Utility functions (e.g., audio duration)
```
