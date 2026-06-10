# Agentic Desktop Knowledge Engine Tasks

## Phase 1: Local AI & Watchdog Setup (The Engine)
- [x] Initialize Python environment and `requirements.txt` (`fastapi`, `watchdog`, `chromadb`, `sentence-transformers`, `ollama`)
- [ ] Install Ollama locally and pull models (e.g., `llama3` for text, `nomic-embed-text` for embeddings)
- [ ] Implement `app/core/llm.py` to communicate with the local Ollama API (Zero cloud dependency)
- [ ] Implement VectorDB wrapper (`app/rag/vector_db.py`) using ChromaDB
- [ ] Build the Directory Watcher (`app/memory/watchdog.py`) to monitor a chosen root folder
- [ ] Implement auto-ingestion: When a new file is detected by Watchdog, parse, chunk, and embed it into ChromaDB

## Phase 2: Local Agent Pipeline (The Brain)
- [ ] Create `app/agents/base.py` interface
- [ ] Implement `agents/planner.py` (Prompt tuned for local Llama-3)
- [ ] Implement `agents/writer.py` (Prompt to generate answers strictly from local chunks)
- [ ] Implement `agents/critic.py` (Prompt to fact-check the Writer using local LLM)
- [ ] Build `agents/orchestrator.py` to chain them together (Planner -> RAG -> Writer -> Critic -> Output)

## Phase 3: The API Bridge
- [ ] Define API schemas in `app/schemas/models.py`
- [ ] Implement `/status` endpoint (Show indexing progress/stats)
- [ ] Implement `/config` endpoint (Change the watched folder path)
- [ ] Implement `/ask` endpoint (Trigger the orchestrator pipeline)
- [ ] Setup FastAPI `main.py` to run both the web server and the Watchdog daemon thread concurrently

## Phase 4: UI & Packaging (Monetization Phase)
- [ ] Scaffold a React or Next.js frontend
- [ ] Build a sleek Spotlight-style Search / Chat UI
- [ ] Setup Tauri or Electron to wrap the React app and the Python FastAPI server
- [ ] Integrate a licensing system (e.g., Lemon Squeezy local key validation) for monetization
- [ ] Compile into a native `.app` or `.dmg` installer using `PyInstaller` and Tauri builder
