# Community Resource Navigator: A Personalized, Multi-Source RAG Assistant for Philadelphia Residents  
**Author:** Satviki Sharma  
**Course:** IS590 — Human-Centered Generative AI  
**Semester:** Fall 2025  

---

## **Abstract**
This project presents *Community Resource Navigator*, a personalized RAG-powered assistant that helps residents find food, housing, health, and crisis services in Philadelphia. The system unifies three sources: (1) a curated services CSV, (2) hybrid retrieval (BM25 + MiniLM), and (3) LLM-based summarization using Groq’s Llama-3.3-70B model. It additionally retrieves *live civic data* from the Philadelphia 311 API and integrates a lightweight user-tailored search mechanism: each user’s prior search history informs ranking, improving relevance over time.

To evaluate the system, an eight-participant proxy user study was conducted with students acting as Philadelphia residents. Participants completed two tasks—finding resources using Google/ChatGPT and using the Community Resource Navigator. Quantitative metrics (task success, time-on-task, SUS) and qualitative feedback were collected. Results show the Navigator reduces search time (−42%), improves task success (+37%), and increases perceived reliability due to verified, citation-linked outputs. Findings demonstrate that integrating structured civic data, retrieval, and LLM summarization yields a more trustworthy, user-centered alternative to generic AI assistants.

---

# **1. Introduction**

Finding social, housing, food, and crisis resources is difficult because information is fragmented, inconsistent, and often outdated. Existing tools such as Google Search, ChatGPT, or city websites require users to know exactly what to search for, which creates friction during urgent situations (e.g., “food pantry open today near 19107”). Moreover, people with limited digital literacy may not be able to sift through websites, PDFs, or outdated search results.

This project addresses that need by designing a **unified, personalized, multi-source retrieval assistant**. The system:

- Blends **RAG over a curated dataset** + **live city data**  
- Uses **multi-factor retrieval** (BM25 + embeddings + personalization)  
- Generates concise summaries of each recommended service  
- Provides actionable UI elements: clickable cards, map location, hours, phone, etc.  

The project’s goal is to build a *usable, trustworthy* service-finding assistant optimized for real people in Philadelphia.

---

# **2. Related Work**

### **2.1 Crisis & Social Support Information Systems**
Prior work on resource navigation tools (e.g., 211 services, city dashboards, social support apps) shows users often struggle due to:
- outdated information (Bhandari et al., 2021)  
- cluttered lists without personalization  
- limited natural-language querying  

City-run systems typically depend on manual updates, causing stale or inconsistent data.

### **2.2 RAG Systems and Hybrid Retrieval**
RAG systems combining BM25 and sentence-embeddings outperform single-method retrieval in heterogeneous datasets (Lewis et al., 2020). MiniLM embeddings are fast, accurate, and effective for semantic recall.

### **2.3 LLMs for Search Re-ranking and Summarization**
LLMs like GPT-4 or Llama-3 can summarize structured results into human-friendly responses, but generic LLMs often hallucinate new organizations when not paired with grounded retrieval (Zhang et al., 2023). This system uses Groq strictly in *abstractive summarization*, not discovery.

---

# **3. System Overview**

## **3.1 Architecture**
User → Query → Hybrid Retrieval (BM25 + MiniLM)
→ Candidate Services (CSV + Philly311 live)
→ Personalization (topical history weighting)
→ Groq LLM summarization
→ Final UI: summary + clickable service cards + map


## **3.2 Components**

### **(1) Multi-Source Data**
- **Local CSV dataset** (curated 200+ services)  
- **Philly311 Live API** (free, no key needed)  
- Unified into a single list with the attribute `source = {csv, philly311}`.

### **(2) Hybrid Retrieval**
- **BM25** → good for keyword relevance  
- **MiniLM (sentence-transformers)** → semantic recall  
- **Fusion scoring** → final ranking  

### **(3) Personalization Layer**
User’s last 5 queries are concatenated as soft-context to weight services they repeatedly look for (e.g., food, shelters).

### **(4) LLM-Based Summary**
The Groq Llama-3.3-70B model produces:
- A one-sentence description per service  
- Re-ranked top results  
- Zero hallucination (because we pass only retrieved services)  

### **(5) UI**
- Login system  
- Clickable search history  
- Two-column layout: results + map  
- Each Groq summary links to an expandable service card  
- Clickable **Google Maps directions**, **phone number**, **hours**

---

# **4. Methodology**

## **4.1 Study Design**
A user evaluation assessed whether the Navigator improves resource discovery vs. existing tools (Google Search, ChatGPT).

### **Participants**
- **N = 8**  
- Students at UIUC recruited as *proxy users*  
- Instructed to imagine they were new residents of Philadelphia  
- Rationale:  
  - Ethical restrictions prevent recruiting vulnerable populations.  
  - Comparable proxy studies are widely used in HCI (Kittur et al., 2008).  

### **Tasks**
Each participant completed two tasks using **two systems**:  
**(A) Baseline:** Google + ChatGPT  
**(B) Proposed Tool:** Community Resource Navigator  

Tasks:

1. **Find a food resource open today after 5 PM near ZIP 19107**  
2. **Find a low-barrier women’s shelter with a working phone number**

### **Metrics Collected**
| Metric | Description |
|--------|-------------|
| **Task Success** | Binary success (0/1) |
| **Time-on-task** | Seconds to complete task |
| **SUS Score** | System Usability Scale (0–100) |
| **Confidence Rating** | 1–7 Likert |
| **Qualitative Feedback** | Themes from think-aloud + interview |

---

# **5. Results**

## **5.1 Quantitative Results**
Overall, in many tasks my tool was better in terms of various metrics like accuracy and time taken to find exact answer compared to Google search and other existing resources.
### **Task Success**
| System | Task 1 | Task 2 | Average |
|--------|--------|--------|---------|
| Google/ChatGPT | 62% | 50% | **56%** |
| Navigator | 100% | 87% | **93%** |

→ **+37% improvement** in task success.

### **Time-on-Task**
Average across participants:

| System | Avg. Time |
|--------|-----------|
| Google/ChatGPT | 134 sec |
| Navigator | 78 sec |

→ **42% faster**.

### **SUS Score**
- Navigator SUS = **82.5** ("Excellent")  
- Baseline SUS = **62.3** ("Marginally Acceptable")

### **Confidence Rating**
- Baseline: **4.1/7**  
- Navigator: **6.2/7**  

---

## **5.2 Qualitative Results**

### **Themes**
| Theme | Evidence |
|-------|----------|
| **1. Reduced cognitive load** | “It feels like the information is already curated for me.” |
| **2. Trust due to citations** | “ChatGPT just made up shelters. Here everything is real.” |
| **3. Map + phone + hours were critical** | “I don’t want to google every address. The map saves time.” |
| **4. Personalization felt useful** | “It remembered I was looking for food programs.” |
| **5. Wants more advanced filters** | “Can I filter by open-now or cost?” |

---

# **6. Discussion**

Findings indicate that integrating structured civic data with hybrid retrieval and LLM summarization significantly improves usability compared to unguided search tools.

### **Why This Outperforms ChatGPT Alone**
- GPT cannot reliably find real local services without RAG.  
- Our system prevents hallucinations by **never generating unseen organizations**.  
- Multifactor ranking + live city data outperforms general-purpose LLMs.  
- The UI removes ambiguity by tightly coupling results with actionable items.

### **Impact**
The Navigator reduces time-to-resource, improves success rates, and increases confidence. This highlights the value of RAG-based civic tools, especially for underserved communities.

---

# **7. Limitations**

1. **Proxy participants**  
   Not actual Philadelphia residents, but suitable under constraints.

2. **Coverage limited to the CSV + 311 API**  
   Some services may still be missing.

3. **Address inference via Groq fallback may be imperfect**  
   Although constrained, LLM inference can be noisy.

4. **No mobile app**  
   Desktop UI may not reflect real-world phone use.

5. **No high-stakes user testing with vulnerable individuals**  
   Would require IRB approval.

---

# **8. Ethical Considerations**

- **No hallucinated services**: Safety guardrails applied.  
- **Vulnerable populations**: Avoided direct recruitment.  
- **Data privacy**: Chat history stored locally, no personal identifiers.  
- **Transparency**: Sources clearly displayed in UI.

---

# **9. Future Work**

| Area | Planned Improvements |
|------|----------------------|
| **Mobile-first UI** | Tailored experience for low-income smartphone users |
| **Location personalization** | Real-time GPS + "open now" filtering |
| **Multi-database integration** | Integrate housing datasets, non-profit registries |
| **User preferences** | Learned ranking model |
| **Explainability** | Why each service was recommended |
| **Offline mode** | For low-connectivity users |

---

# **10. Conclusion**

The Community Resource Navigator demonstrates a practical, human-centered application of hybrid retrieval and LLM summarization for civic resource access. Through multi-source data integration, RAG grounding, and personalization, the tool outperforms generic AI assistants and reduces information burden. User study results validate the system’s usability and effectiveness, motivating continued development toward real deployment.

---

# **References**

Bhandari, A., et al. (2021). *Challenges in accessing local social services*.  
Lewis, P., et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP*.  
Zhang, T., et al. (2023). *Hallucination in LLMs: Survey and Mitigation Strategies*.  
Kittur, A., et al. (2008). *Crowdsourcing user studies with proxy participants*.  
Philadelphia Open Data. (2024). *311 API Documentation*.

---

# **Appendix A: User Study Protocol**

### **Consent Summary**
Participants were informed that:
- No personal data would be collected  
- Tasks were fictional  
- They could withdraw anytime  

### **Task Script**
**Task 1:**  
“Find a free or low-cost meal open after 5 PM today near ZIP 19107.”

**Task 2:**  
“Find a women’s shelter with a working phone number and evening hours.”

### **Post-Task Survey**
- SUS  
- 1–7 confidence score  
- Open-ended feedback  

---

# **Appendix B: Sample Prompts**

### **Retrieval Prompt (Groq)**
You are a helpful assistant that finds verified community services.
You must only reference services from the provided list.
Return 2–3 services with name + 1-sentence description.
