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

*   **`setup-project`**: Esegue il setup iniziale del progetto (creazione venv, installazione dipendenze, configurazione .env). Utile se hai bisogno di riconfigurare l'ambiente.

    ```bash
    setup-project
    ```

*   **`verify-setup`**: Verifica che l'ambiente di setup sia corretto (versione Python, dipendenze, FFmpeg, chiavi API, directory ChromaDB).

    ```bash
    verify-setup
    ```

*   **`run-app-query`**: Esegue la logica per interrogare il database indicizzato. L'uso specifico potrebbe dipendere dall'implementazione interna (es. richiede input da riga di comando o avvia un'interfaccia).

    ```bash
    run-app-query # Potrebbe richiedere argomenti, controlla l'implementazione di app_query.py
    ```

*   **`run-app-upload`**: Esegue la logica per l'upload e l'ingestione di nuovi file audio/video per la trascrizione e l'indicizzazione.

    ```bash
    run-app-upload # Potrebbe richiedere argomenti (es. percorso file), controlla l'implementazione di app_upload.py
    ```

*   **`show-db`**: Mostra il contenuto del database ChromaDB.

    ```bash
    show-db
    ```

*   **`manage-db`**: Permette di gestire il database ChromaDB. Supporta i seguenti sottocomandi:

    -   Listare documenti:

        ```bash
        manage-db list
        ```

    -   Cancellare documenti specifici per ID:

        ```bash
        manage-db delete <id1> <id2> ...
        ```

    -   Cancellare l'intero database:

        ```bash
        manage-db delete-all
        ```

