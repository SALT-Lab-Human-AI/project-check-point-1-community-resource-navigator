# 🧭 Community Resource Navigator – Telemetry & Observability Plan

_Last updated: Checkpoint #3_

---

## 1️⃣ Overview
This document explains what data the **Community Resource Navigator** app collects, how it is stored, and how developers use it for debugging, personalization, and performance monitoring.  
Our goal is to maintain **minimal, privacy-respecting observability** while ensuring that we can effectively troubleshoot and improve the system.

---

## 2️⃣ Logged Data

| Data Type | Source | Purpose | Retention | Privacy Notes |
|------------|---------|----------|------------|----------------|
| **User Account Info** | SQLite `users` table | Authentication (stores name, email, and bcrypt-hashed password). | Persistent | Passwords are hashed; no plaintext credentials are stored. |
| **User Query History** | SQLite `chat_history` table | Track queries and generated responses to improve relevance and personalization. | Rolling window (e.g., 10 recent queries per user). | Queries contain no PII beyond the local username. |
| **App Runtime Logs** | Streamlit console / local logs | Debugging failed logins, API errors, and Groq failures. | Temporary (session-based). | No sensitive data (emails, passwords, or tokens) is ever written to logs. |

---

## 3️⃣ Logging Goals

- Support local debugging for:
  - Failed API or database operations  
  - Groq timeout or summarization errors  
  - Query/retrieval mismatches  
- Allow limited, anonymized analysis of user behavior (query categories, frequency).  
- Avoid any external telemetry or analytics collection.

---

## 4️⃣ Debugging & Observability

- **Console Logging:**  
  Exceptions and warnings are printed to the Streamlit runtime console.  
- **Error Tracking:**  
  Each Groq or API failure is logged with timestamp + internal user ID (no emails).  
- **Performance Monitoring:**  
  Developers can monitor query latency and Groq response times through local print/log statements.  

All debugging information remains local and is never transmitted externally.

---

## 5️⃣ Privacy & Security

- All **passwords hashed** with `bcrypt` before storage.  
- **No plaintext credentials**, API keys, or secrets appear in logs.  
- API keys are securely stored in `.env` files or **Streamlit Secrets**, never in GitHub.  
- `.env` and `.db` files are explicitly included in `.gitignore`.  
- Only authorized developers can access the local database for debugging.  

---

## ✅ TL;DR

> The system logs only what is essential for functionality and debugging.  
> No personally identifiable information (PII) is exposed, all credentials are securely hashed, and all telemetry stays on-device.  
> Observability focuses on reliability and ethical data practices.

---

**Maintainer:** Satviki Sharma  
**Team:** Community Resource Navigator — Fall 2025  
**Repo:** [GitHub Link](https://github.com/your-org/community-navigator)
