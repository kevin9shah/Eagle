# Agentic Desktop Knowledge Engine (Privacy-First)

## 1. 🧠 Architecture Pivot: OS-Level Integration

Instead of a user manually uploading PDFs to a web server, the product will now act as a background daemon on the user's PC.

### New Core Components:
1. **Directory Watcher (The "Eyes")**: Uses Python's `watchdog` library. The user selects a root folder (e.g., `~/Documents` or a specific `~/AI_Brain` folder). The watcher constantly monitors for new, modified, or deleted files and automatically syncs them to the Vector DB.
2. **100% Local AI Stack (Absolute Privacy)**: 
   * **LLM**: Instead of OpenAI/Gemini (which sends data to the cloud), we integrate **Ollama**. The app will run models like `Llama-3-8B` or `Phi-3` directly on the MacBook M1 chip. Data *never* leaves the machine.
   * **Embeddings**: Run locally using `sentence-transformers` (HuggingFace) instead of paid APIs.
3. **Multi-Agent Orchestrator**: The same Planner -> Writer -> Critic pipeline, but interacting with the local OS files.
4. **Desktop UI**: A minimal, spotlight-like search bar or a sleek Chat UI built with **Tauri** or **Electron**.

---

## 2. 🛡️ Privacy Guarantee Design

To market this product effectively, **"Zero-Data-Leak"** is your biggest selling point.
* **No Telemetry**: The app does not ping external servers.
* **Air-Gapped Capable**: The app must function entirely without an internet connection once the local LLM weights are downloaded.
* **Local Vector DB**: ChromaDB runs entirely in the user's local AppData directory.

---

## 3. 💰 Monetization Strategy

How to make money from a local Python backend:

### Packaging the App
You cannot easily sell a Python script. You must package it into a standalone executable.
* **Frontend**: Build a sleek UI using React/Next.js.
* **Desktop Wrapper**: Use **Tauri** (lighter, faster) or **Electron** to package the web UI and run the Python FastAPI server as a hidden background process.
* **Bundler**: Use `PyInstaller` to compile the Python backend into a `.app` (Mac) or `.exe` (Windows) so the user doesn't need to install Python.

### Business Models
1. **One-Time Purchase (Recommended)**: "Pay $49 once, own your private AI forever." Sell it on Gumroad or Lemon Squeezy. This model is highly popular for local-first productivity tools.
2. **Freemium**: The app is free for indexing up to 100 documents. A premium license key (validated locally via RSA signatures or a lightweight API check) unlocks unlimited indexing and advanced agent workflows (like the Critic agent).
3. **"Bring Your Own Key" (BYOK) Cloud Tier**: While the default is local Ollama, offer a setting where power users can put in their own OpenAI API key if they want GPT-4o-level reasoning, at their own privacy risk.

---

## 4. 📋 Updated Implementation Roadmap

**Phase 1: Local AI & Watchdog Setup**
- Install Ollama on your Mac and pull `llama3`.
- Build the `watchdog` script that listens to a specific folder and automatically chunks/embeds new files into local ChromaDB.

**Phase 2: Local Agent Pipeline**
- Connect the Planner, Writer, and Critic agents to use the local Ollama API instead of Gemini.
- Ensure the Critic agent can fact-check efficiently using local models.

**Phase 3: The API & Desktop Bridge**
- Wrap the FastAPI server to handle requests from a local UI.
- Add endpoints like `/status` (indexing progress) and `/config` (setting the watched folder path).

**Phase 4: UI & Packaging (Monetization Phase)**
- Build a React frontend.
- Package the React frontend and Python backend into a single double-clickable Desktop App using Tauri/Electron.
- Integrate Lemon Squeezy for license key validation.

---

## 5. 🗄️ ChromaDB Integration Plan

To fulfill the zero-data-leak and privacy-first guarantee, we will implement ChromaDB entirely locally using `chromadb.PersistentClient`.

### Component Details
#### `app/core/vector_db.py` (New File)
We will create a `VectorDBClient` wrapper class.
- **Storage Path**: Data will be saved locally to `data/chromadb/` using `chromadb.PersistentClient(path="./data/chromadb")`.
- **Embeddings**: We will use Chroma's built-in `SentenceTransformerEmbeddingFunction` with a local model like `nomic-embed-text` or `all-MiniLM-L6-v2`. This ensures text chunk embeddings are generated locally on the user's machine.
- **Methods**:
  - `add_chunks(collection_name, chunks, metadatas, ids)`: For the watchdog to insert new document chunks.
  - `query(collection_name, query_text, n_results)`: For the retrieval agent to search relevant chunks.

### User Review Required
> [!IMPORTANT]
> - Do you prefer putting the `VectorDBClient` in `app/core/vector_db.py` or `app/retrieval/vector_db.py`? (The task list mentioned `app/rag/vector_db.py`, but that directory doesn't exist. I recommend `app/core/` for the shared client and `app/retrieval/` for the actual RAG search logic).
> - Would you like me to go ahead and implement the `vector_db.py` wrapper now?

---

## 6. 🏗️ Auto-Ingestion Architecture Fix

To resolve the architectural flaws in the auto-ingestion pipeline (preventing duplicates and ensuring an initial scan), we will implement the following two fixes:

### 1. Initial Boot Scan (`app/memory/file_watcher.py`)
Before the watchdog observer starts listening for real-time events, the `watch()` function will iterate through the provided directory using `os.walk` and call `ingest_file()` on every `.pdf` it finds. This guarantees the database is fully up-to-date before live watching begins.

### 2. Duplicate Prevention via Metadata Purging (`app/ingestion/vector_db.py`)
Currently, modifying a file appends new chunks, leading to duplicates. Because `PyPDFLoader` automatically adds a `{"source": "absolute/path/to/file.pdf"}` tag to every chunk's metadata, we can perform a clean overwrite.
Inside `ingest_file()`, before we embed and add the new documents, we will fetch the raw Chroma collection and delete any existing chunks associated with that file:
```python
# Purge old chunks for this file
collection = chroma_client.get_or_create_collection(collection_name)
collection.delete(where={"source": file_path})
```
This ensures that if a file is modified (or re-scanned on boot), its old embeddings are completely wiped out before the fresh ones are inserted, guaranteeing zero duplicates.

### User Review Required
> [!IMPORTANT]
> Since you have been implementing the code yourself recently, would you like me to go ahead and apply these architecture fixes directly to your `vector_db.py` and `file_watcher.py` files, or would you prefer me to just give you the step-by-step code snippets again?
