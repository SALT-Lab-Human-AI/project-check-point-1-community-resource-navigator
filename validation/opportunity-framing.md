# 💡 Opportunity Framing – Community Resource Navigator  
*(Checkpoint 2 Validation)*  

## 1️⃣ Purpose
The *Community Resource Navigator* addresses critical gaps uncovered in the prompt-based validation study with ChatGPT, Microsoft Copilot, and Perplexity AI.  
While existing generative tools can return general results, none provide **reliable, structured, localized**, or **safety-aware** guidance for community resource searches.  
This document defines the product requirements our tool will meet that others do not.

---

## 2️⃣ Core Product Vision
> “A lightweight, trustworthy AI assistant that instantly surfaces verified local services (food, shelter, clinics, etc.) in a simple, human-friendly format — without hallucinations, hidden costs, or confusion.”

---

## 3️⃣ Key Differentiating Requirements

| # | Requirement | Why Existing Tools Fail | How Community Resource Navigator Solves It |
|:--|:--|:--|:--|
| **1** | **Structured Output** (Name / Address / Hours / Eligibility / Phone) | ChatGPT and Copilot return paragraphs of text with missing or inconsistent fields. | Every record is stored and retrieved from a CSV schema with fixed columns, ensuring predictable and readable cards. |
| **2** | **Local Grounding via RAG** | Current LLMs rely on generic web search, often showing wrong cities. | Hybrid BM25 + SentenceTransformer retrieval over verified local data (e.g., Philadelphia services). |
| **3** | **Offline / Low-cost Deployment** | All commercial tools require API access and cloud connectivity. | Runs fully on open-source models (MiniLM + BM25) with local CSV files, usable on community laptops or kiosks. |
| **4** | **Transparency and Source Control** | None show data provenance; users can’t verify accuracy. | “See retrieved sources” panel lists exact records and metadata for each result. |
| **5** | **Safety & Sensitivity Handling** | No privacy cues for sensitive queries (e.g., domestic violence, homelessness). | Built-in safety text and hotline auto-insertion for flagged terms (“violence”, “abuse”). |
| **6** | **Multilingual Accessibility (Planned)** | Most current tools default to English. | Support multi-language datasets + translation layer (e.g., English/Spanish). |
| **7** | **Zip-aware & Time-aware Filters** | None correctly interpret “near 19107” or “after 5 PM”. | Incorporates zip filtering and basic time parsing to match open-hour data. |
| **8** | **Human-centered UI** | Large-text interfaces can overwhelm users under stress. | Minimal Streamlit UI with quick results, accessibility fonts, and clear action hierarchy. |

---

## 4️⃣ Design Priorities
1. **Speed:** Query → Answer in < 2 seconds using pre-encoded embeddings.  
2. **Clarity:** Always return compact cards, not prose.  
3. **Trust:** Never generate unverified data — all answers grounded in `services.csv`.  
4. **Accessibility:** Simple interface usable by non-technical users (e.g., volunteers, seniors).  
5. **Expandability:** Easy to plug in additional city datasets later.  

---

## 5️⃣ User Promise
> “Ask once, get a clear, verified answer.”  
No ads, no confusing chat threads — just structured community help, instantly.

---

## 6️⃣ Next Steps
- Implement zip-radius and open-hour filters.  
- Add optional GPT-4 summarization layer (for descriptive clarity).  
- Prepare usability walkthrough and feedback collection for Checkpoint 3.  

---

*Author:* **Satviki Sharma**  
📧 satviki2@illinois.edu  
*Date:* October 2025  
