# Artifact Package

This artifact package documents all code, data, configuration, and deployment links needed to reproduce the Community Resource Navigator prototype and the evaluation in this report.

---

## 1. Deployed Application

- **Deployed Streamlit App:**  
  https://community-navigator-ss.streamlit.app/

The deployed app runs the same core logic as `prototype/app.py` in this repository, using the `services.csv` dataset and environment variables described below.

---

## 2. GitHub Repository (Source Code)

- **Repository URL:**  
  https://github.com/SALT-Lab-Human-AI/project-check-point-1-community-resource-navigator/tree/main

### 2.1. Key Directories & Files

- `prototype/app.py`  
  - Main Streamlit application implementing:
    - Hybrid retrieval (BM25 + MiniLM embeddings)
    - Groq LLM–based summarization on top of retrieved results
    - User login (demo accounts)
    - Per-user chat history stored in SQLite
    - Filters for category / people served
    - Interactive map (PyDeck) showing matching services

- `data/services.csv`  
  - Curated dataset of community services for Philadelphia (food, shelter, clinics, etc.).
  - Used as the primary knowledge base for the RAG pipeline.
  - Columns include (after normalization in `app.py`):  
    `id, category, name, address, zip, days, open, close, eligibility, description, phone, latlon, lat, lon, hours, retrieval_text`.

- `.env.example`  
  - Template for environment variables required to run the app locally.
  - Example fields:
    - `DATA_PATH=data/services.csv`
    - `EMB_MODEL=sentence-transformers/all-MiniLM-L6-v2`
    - `DB_PATH=data/app.db`
    - `GROQ_API_KEY=YOUR_GROQ_API_KEY_HERE`
  - **Note:** The actual `.env` with secrets is *not* checked into GitHub.

- `requirements.txt` (if present)  
  - Python dependencies needed to run the prototype (Streamlit, `rank_bm25`, `sentence-transformers`, `pydeck`, `requests`, etc.).
  - If not present, see “Local Setup” below for a suggested environment.

- `docs/`  
  - Contains design and documentation artifacts:
    - `DESIGN_SPEC.md` – user journeys, flows, and key screens.
    - `FINAL_REPORT.md` – full project report (CP4) with method, results, and discussion.
    - Any additional figures / screenshots referenced in the report.

- `validation/`  
  - Prompting study artifacts for Checkpoint 2:
    - Prompt protocols and scenarios.
    - Transcripts of interactions with existing tools (ChatGPT, Copilot, Perplexity, etc.).
    - Gap analysis notes and opportunity framing.

- `images/`  
  - Screenshots of the prototype UI used in the report and slides (e.g., `prototype.png`).

---

## 3. Data Artifacts

### 3.1. Primary Dataset

- **File:** `data/services.csv`  
- **Description:**  
  A hand-curated table of community resources in Philadelphia, including:
  - Organization name
  - Category (e.g., Food, Shelter, Health)
  - Address and ZIP
  - Hours / days open
  - People served (e.g., “Women with children”, “Families”)
  - Phone and short description
  - Lat/Lon for mapping

- **Usage in the System:**
  - Loaded in `app.py` via `load_services_csv(...)`.
  - Normalized and converted into a `retrieval_text` field used by:
    - BM25 keyword retrieval (`rank_bm25`),
    - SentenceTransformer embeddings (`MiniLM`) for semantic similarity.
  - Results are then ranked and passed to the Groq LLM for summarization.

### 3.2. Derived Data

- **SQLite DB:** `data/app.db` (created at runtime)
  - Created by `init_db()` in `app.py`.
  - Stores per-user chat history:
    - `username, query, response, timestamp`
  - Used for:
    - Displaying recent searches in the sidebar.
    - Basic personalization (e.g., re-using previous queries).

---

## 4. Configuration & Environment

### 4.1. Environment Variables

There is an .env.example file for your reference

## 5. How to Run the App Locally

Clone the repo:

git clone https://github.com/SALT-Lab-Human-AI/project-check-point-1-community-resource-navigator.git
cd project-check-point-1-community-resource-navigator


Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate     # macOS / Linux
# venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


or use the manual pip install command shown above.

Create .env from .env.example:

cp .env.example .env
# then edit .env to add your GROQ_API_KEY and adjust paths if needed


Run Streamlit:

streamlit run prototype/app.py


Open the app:

Local URL: http://localhost:8501

Use the demo credentials (e.g., user1 / password1) to log in.

## 6. Reproducing Evaluation & User Study (CP4)

To reproduce the evaluation described in FINAL_REPORT.md:

Prompting & Baseline Tools (Checkpoint 2):

Go to validation/.

Use the provided prompt files and transcripts to replicate:

Queries issued to ChatGPT / Copilot / Perplexity.

Gap analysis of failures, latency, and UX friction.

User Study Setup (Checkpoint 4):

Materials included in docs/ and/or validation/:

Task instructions for proxy users (students acting as Philadelphia residents).

Survey questions (SUS/UMUX-Lite style items, satisfaction, usefulness).

Script for “Google vs. Navigator” comparison.

Running the Study:

Deploy or run the app locally.

Ask participants to:

Complete the same tasks using Google / existing tools.

Then complete tasks using the Community Resource Navigator.

Record:

Task success, time-on-task, and errors.

Survey responses (SUS/UMUX-Lite, satisfaction, trust).

Qualitative feedback about clarity, usefulness, and frustrations.

Analysis Scripts (if applicable):

Any Python notebooks or scripts used to compute descriptive statistics and plots should be placed under analysis/ or notebooks/ (if you added them).

These can be run after exporting survey data to CSV.



## 8. Summary

This artifact package provides:

A deployed prototype (Streamlit app) accessible on the web.

A reproducible codebase, including the RAG pipeline (BM25 + MiniLM + Groq).

Cleaned local data (services.csv) and runtime DB (app.db).

Configuration templates (.env.example) and instructions to run locally.

Prompting study artifacts and user study materials to replicate evaluation.

Together, these artifacts demonstrate a complete, end-to-end community resource navigation system and the evaluation workflow used in Checkpoint 4.
