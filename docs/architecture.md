# 🧭 Community Resource Navigator – System Architecture

---

## 1️⃣ Overview

The **Community Resource Navigator** is an AI-powered Streamlit application that helps users in **Philadelphia** discover local community resources such as food pantries, shelters, health clinics, and city maintenance services.  

The system integrates **multiple heterogeneous data sources** — a curated CSV, a live city API (Philly311), and a local SQLite database — and uses **hybrid information retrieval** (BM25 + SentenceTransformer embeddings) enhanced with a **Generative AI reasoning layer** (Groq LLM) to provide human-like, context-aware recommendations.

---

## 2️⃣ Data Sources and Their Roles

| Source | Type | Description | Usage |
|---------|------|-------------|-------|
| **`data/services.csv`** | Local CSV | Curated community service records (organizations, eligibility, hours, contact info, lat/lon). | Main structured dataset. |
| **Philly311 API** | REST API | Live feed of service requests from the City of Philadelphia (sanitation, safety, streetlight issues, etc.). | Adds real-time context and active public reports. |
| **SQLite DB (`data/app.db`)** | Local database | Stores query–response history for personalization and auditing. | Enables adaptive recommendations and user context. |
| **Groq API (LLM)** | External service | Large Language Model (Llama 3.3 via Groq) for reasoning and summarization. | Synthesizes the top results into natural-language recommendations. |

Each query combines **local**, **live**, and **AI reasoning** layers to form a semantically enriched, actionable response.

---

## 3️⃣ System Architecture Overview

            ┌──────────────────────────────────────────────┐
            │              Streamlit Frontend              │
            │  (User login, query, filters, visualization) │
            └───────────────────┬──────────────────────────┘
                                │
                                ▼
 ┌────────────────────────────────────────────────────────────┐
 │                Data Integration Layer                      │
 │   - Load CSV via `load_services_csv()`                     │
 │   - Fetch live 311 data via `load_philly311_data()`        │
 │   - Merge → unified DataFrame with common schema           │
 └───────────────────┬────────────────────────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────────────────────────┐
 │                 Hybrid Retrieval Engine                    │
 │  BM25 (lexical) + SentenceTransformer (semantic) fusion     │
 │  + personalization boost from chat history                 │
 │  → top-K ranked service candidates                         │
 └───────────────────┬────────────────────────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────────────────────────┐
 │           Generative Summarization (Groq LLM)              │
 │   Context: top results → concise 3-item recommendation     │
 │   Natural language synthesis with factual grounding        │
 └───────────────────┬────────────────────────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────────────────────────┐
 │                Presentation & Visualization                │
 │  Streamlit cards + expanders + PyDeck map (geo layer)      │
 │  Fused color coding: local (blue), Philly311 (orange)      │
 └───────────────────┬────────────────────────────────────────┘
                     │
                     ▼
 ┌────────────────────────────────────────────────────────────┐
 │           Telemetry, Logging & Personalization             │
 │  SQLite (`chat_history`): stores queries & responses       │
 │  Used for keyword boosting and adaptive filtering          │
 └────────────────────────────────────────────────────────────┘
