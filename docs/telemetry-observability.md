# 🩺 Telemetry and Observability Plan
_Community Resource Navigator_

---

## 1️⃣ Purpose

Telemetry and observability ensure that the **Community Resource Navigator** runs reliably, and that errors, performance issues, or model misbehaviors can be quickly identified and corrected.  

The system logs essential events, metrics, and user interactions into a local SQLite database (`data/app.db`) and console output.  
This lightweight setup keeps the project privacy-safe and portable while supporting meaningful debugging during development and testing.

---

## 2️⃣ Logged Data & Database Schema

All telemetry data is stored in the `chat_history` table of `data/app.db`.

### **Schema**

| Column | Type | Description |
|---------|------|-------------|
| `id` | INTEGER (PK, auto increment) | Unique identifier for each entry |
| `username` | TEXT | Logged-in user performing the query |
| `query` | TEXT | Full user input |
| `response` | TEXT | Groq LLM-generated summary (3-item answer) |
| `timestamp` | TEXT (ISO 8601) | UTC time of completion |

### **Example Entry**
```json
{
  "id": 15,
  "username": "user1",
  "query": "free dinner near 19107",
  "response": "1. Chosen 300 Outreach Center — ...",
  "timestamp": "2025-11-06T23:18:42Z"
}
