# Audio-RAG Project

Questo progetto implementa un sistema di Retrieval Augmented Generation (RAG) per contenuti audio/video. Permette di trascrivere file multimediali, indicizzare il testo risultante in un database vettoriale (ChromaDB) e interrogare il database per trovare informazioni pertinenti.

## Setup

Segui questi passaggi per configurare il progetto sul tuo sistema:

1.  **Clona il repository:**

    ```bash
    git clone <URL del repository>
    cd audio-rag # o il nome della directory del progetto
    ```

2.  **Esegui lo script di setup cross-platform:**

    ```bash
    python -m setup_project
    ```

    Questo script creerà un ambiente virtuale (`.venv`), installerà le dipendenze necessarie e ti guiderà nella configurazione delle chiavi API nel file `.env`.

3.  **Attiva l'ambiente virtuale:**

    -   Su Linux/macOS:

        ```bash
        source .venv/bin/activate
        ```

    -   Su Windows:

        ```bash
        .venv\Scripts\activate
        ```

    Assicurati che l'ambiente virtuale sia attivo ogni volta che lavori al progetto (vedrai `(.venv)` all'inizio del prompt del tuo terminale).

## Utilizzo

Una volta completato il setup e attivato l'ambiente virtuale, puoi utilizzare i seguenti script:

*   **`setup_project.py`**: Esegue il setup iniziale del progetto (creazione venv, installazione dipendenze, configurazione .env). Utile se hai bisogno di riconfigurare l'ambiente.

    ```bash
    python setup_project.py
    ```

*   **`verify_setup.py`**: Verifica che l'ambiente di setup sia corretto (versione Python, dipendenze, FFmpeg, chiavi API, directory ChromaDB).

    ```bash
    python verify_setup.py
    ```

*   **`app_query.py`**: Esegue la logica per interrogare il database indicizzato.

    ```bash
    python app_query.py "La tua domanda qui"
    ```

*   **`app_upload.py`**: Esegue la logica per l'upload e l'ingestione di nuovi file audio/video per la trascrizione e l'indicizzazione.

    ```bash
    python app_upload.py <percorso_del_file_audio/video>
    ```

*   **`rag_system/verifier.py`**: Mostra il contenuto del database ChromaDB.

    ```bash
    python rag_system/verifier.py
    ```

*   **`rag_system/cleaner.py`**: Permette di gestire il database ChromaDB. Supporta i seguenti sottocomandi:

    -   Listare documenti:

        ```bash
        python rag_system/cleaner.py list
        ```

    -   Cancellare documenti specifici per ID:

        ```bash
        python rag_system/cleaner.py delete <id1> <id2> ...
        ```

    -   Cancellare l'intero database:

        ```bash
        python rag_system/cleaner.py delete-all
        ```

