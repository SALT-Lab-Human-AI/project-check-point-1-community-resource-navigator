# 🧩 Gap Analysis – Community Resource Navigator  
*(Checkpoint 2 Validation)*  

## 1️⃣ Overview
This gap analysis evaluates how existing generative AI tools — **ChatGPT**, **Microsoft Copilot**, and **Perplexity AI** — handle local community resource queries.  
The goal was to understand their performance in **accuracy, reliability, latency, UX**, and **safety**, and identify unmet needs that justify building the *Community Resource Navigator*.

---

## 2️⃣ Methodology
Each tool was prompted with 4 identical real-world queries:

1. “Where can I get a free dinner near 19107 on Sunday evening in Philadelphia?”  
2. “I need an emergency shelter for women with children in Philadelphia.”  
3. “Where can I find a place with food and showers today in Philadelphia?”  
4. “Are there any clinics open after 5 PM in the 19130 area?”  

Prompts and transcripts are saved under `/validation/{ToolName}/`.

Each test assessed:
- **Accuracy:** Were responses factual and location-appropriate?  
- **Completeness:** Did they include hours, addresses, and contact info?  
- **Reliability:** Were links or organizations real and current?  
- **Latency:** How fast was the response?  
- **UX / Tone:** Was the format usable for a stressed user in need?  
- **Safety:** Any hallucinated or unsafe instructions?  

---

## 3️⃣ Findings Summary

| Category | ChatGPT | Microsoft Copilot | Perplexity AI |
|:--|:--|:--|:--|
| **Accuracy** | Often correct; some outdated info on smaller shelters | Correctly lists verified sources but misses hours | Most accurate and location-aware; verified entries |
| **Completeness** | Strong on descriptive context but sometimes lacks phone numbers | Includes addresses but omits eligibility | Includes addresses, hours, phones, and safety notes |
| **Reliability** | 8/10 results were real | 6/10 valid; others generic web results | 9/10 verified and current |
| **Latency** | ~5–6 seconds | ~4 seconds | ~3 seconds |
| **UX / Tone** | Conversational and supportive | Formal, slightly corporate | Structured lists with markdown clarity |
| **Safety / Bias** | Neutral tone, no unsafe recs | Generic disclaimers only | Adds hotline and safety disclaimers |

---

## 4️⃣ Key Gaps Identified

### 🧭 Accuracy and Localization  
- ChatGPT and Copilot sometimes **misplace results** (e.g., list New Orleans or Champaign locations instead of Philadelphia).  
- Perplexity handled geography better, but none filtered by **zip code or real-time open hours**.  

### ⚙️ Reliability and Verifiability  
- No tool provided **consistent sources** or citations for community-specific data.  
- Users must manually fact-check each location.

### 💬 User Experience and Structure  
- Responses vary in structure: walls of text or incomplete tables.  
- Users in crisis need **short, structured cards** (Name | Address | Hours | Phone).  

### 💰 Accessibility and Cost  
- All rely on cloud APIs; none work **offline or for free** at the community center level.  
- A lightweight, local CSV+embedding pipeline avoids recurring costs.  

### ⚠️ Safety & Ethical Gaps  
- No mention of **confidential intake procedures** for shelters.  
- Missing **privacy warnings** for sensitive searches (e.g., domestic violence).  

---

## 5️⃣ Insights from “Speed Dating” Discussions  
Although this was a solo project, informal peer discussions revealed:  
- Community volunteers want **simple, factual outputs**, not conversational fluff.  
- Caseworkers care about **source transparency** and **update frequency**.  
- Many prefer **offline or locally hosted models** for privacy.  

These insights helped shape the focus on *retrieval accuracy, grounding, and concise structured responses*.

---

## 6️⃣ Opportunity Framing

| Problem | Current Tool Limitation | Opportunity for This Project |
|:--|:--|:--|
| Location-based accuracy | Models confuse cities | Build structured geotagged dataset (lat/lon) |
| Consistent schema | Unstructured text | Unified data schema (Name, Category, Hours, Eligibility, Phone) |
| Trustworthiness | LLM hallucinations | Retrieval grounded in verified CSV sources |
| Accessibility | Requires Internet/API keys | Lightweight offline Streamlit app |
| Transparency | No data provenance | Expandable “sources” panel for audit trail |

---

## 7️⃣ Next Steps
- Integrate **LLM summarization module** only after retrieval accuracy >90%.  
- Add **zip code radius filter** (e.g., “within 3 miles of 19107”).  
- Implement **user feedback button** (“helpful / not helpful”).  
- Prepare **prototype demo video** for Checkpoint 3.

---

*Author:* **Satviki Sharma**  
📧 satviki2@illinois.edu  
*Date:* October 2025  
