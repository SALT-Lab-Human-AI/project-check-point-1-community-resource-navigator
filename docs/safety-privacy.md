# 🔒 Safety & Privacy Notes  
_Community Resource Navigator_

---

## 1️⃣ Overview

The **Community Resource Navigator** handles real user queries but does **not collect or store personally identifiable information (PII)**.  
All data is processed locally within the Streamlit session or via secure, rate-limited API calls to **Groq (LLM)** and **Philly311**.

The design follows three principles:

1. **Minimal data retention**
2. **Transparent processing**
3. **Safe model interaction**

---

## 2️⃣ Personally Identifiable Information (PII) Handling

| Category | Example | Handling Policy |
|-----------|----------|----------------|
| **User credentials** | Demo login (`user1`, `user2`) | Stored only in memory; no real names or passwords. |
| **User queries** | “Where can I find help for my daughter?” | Logged as plain text in `chat_history`, but **no user metadata** beyond `username`. |
| **Location data** | Address fields in CSV or 311 API | Public data only (organization addresses); user-provided locations never persisted. |
| **Contact info (phones, emails)** | Service phone numbers | Public organizational data; sanitized before being sent to LLM context. |
| **IP address / browser data** | Streamlit session info | Never logged or transmitted. |

**Summary:**  
> Only public service metadata is stored; no private user details are collected or exported.  
> The app complies with basic GDPR-style data minimization (purpose-limited, ephemeral logging).

---

## 3️⃣ Data Storage & Retention

- **SQLite database (`data/app.db`)**  
  - Contains only `(username, query, response, timestamp)`  
  - No persistent identifiers or personal context beyond session alias.  
  - Developers can purge logs anytime:
    ```bash
    sqlite3 data/app.db "DELETE FROM chat_history;"
    ```

- **Environment variables** (`.env`)  
  - Store API keys only (Groq, optional Mapbox).  
  - `.env.example` is provided for safe configuration sharing.  
  - `.env` itself is excluded from version control via `.gitignore`.

---

## 4️⃣ Rate Limiting & API Usage

| API | Mechanism | Limit Strategy |
|------|-------------|----------------|
| **Groq LLM** | One request per user query | Prevents model flooding; 3-item summaries only. |
| **Philly311 API** | Limited to ≤ 50 requests per query | Query parameters control fetch size. |
| **Streamlit UI** | Debounced search button | Avoids repeated calls if user clicks rapidly. |

If external APIs fail or exceed rate limits, the app **gracefully degrades** by:
- Returning cached or CSV-only results.
- Displaying `⚠️ Groq error` or `No live updates available.` instead of crashing.

---

## 5️⃣ Jailbreak and Abuse Mitigations

| Risk | Mitigation |
|------|-------------|
| **Prompt Injection / Jailbreak** | System prompts clearly define a factual, civic-assistant role: _"Helpful factual assistant for Philadelphia."_ The LLM is **not** allowed to run code, generate unsafe content, or respond to personal questions. |
| **Off-topic or malicious queries** | Non-matching queries produce no recommendations; no direct execution or web search is possible. |
| **Prompt chaining abuse** | Each Groq call is stateless; chat history influences retrieval weighting but is never concatenated into the LLM prompt. |
| **Untrusted external data** | Philly311 data is treated as unverified; displayed with attribution and never rephrased as factual statements. |
| **Cross-site scripting (XSS)** | Streamlit sanitizes Markdown output; unsafe HTML disabled except for trusted CSS styling. |

---

## 6️⃣ Model Output Safety

- **Temperature:** `0.3` → deterministic, factual summaries.  
- **Max tokens:** `300` → prevents over-long or runaway responses.  
- **Context restriction:**  
  Only structured text from trusted sources (CSV + 311 API) is passed to the LLM.  
  No freeform user data or hidden code is embedded.

---

## 7️⃣ Responsible AI Practices

1. **Transparency:** All AI outputs labeled as “AI-generated recommendations.”  
2. **Explainability:** Each recommendation is linked to the real data source (local or Philly311).  
3. **Accountability:** Developers can audit every query–response pair in `chat_history`.  
4. **Opt-out:** Clearing the database removes all interaction history instantly.

---

## 8️⃣ Threat & Abuse Scenarios

| Scenario | Response |
|-----------|-----------|
| User attempts prompt injection (“ignore your instructions”) | LLM prompt explicitly resets role each call → ignored. |
| High traffic / spam load | Streamlit throttling + API rate limits prevent saturation. |
| Data corruption or invalid CSV | Exception handled; defaults to empty DataFrame. |
| LLM generates unsafe text | Temperature control + strict prompt prevents personal, political, or biased language. |

---

## 9️⃣ Future Improvements

- Add **per-user API quotas** in database (`usage_count` per 24h).  
- Implement **hashing of queries** before logging for stronger privacy.  
- Integrate **content moderation API** before rendering responses.  
- Support **secure audit exports** for research (anonymized interaction logs).

---

### ✅ Summary

> The Community Resource Navigator is designed for safety by default:  
> no personal data retention, minimal API exposure, and bounded AI behavior.  
> All processing occurs locally or through trusted civic APIs, and every LLM response is both rate-limited and context-bounded to prevent misuse or hallucination.

