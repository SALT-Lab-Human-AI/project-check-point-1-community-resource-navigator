# Proposal: Community Resource Navigator

---

## 📝 Problem & Importance
Residents often struggle to find reliable, up-to-date information on community resources such as food pantries, free clinics, ESL classes, housing support, and job training. The current landscape of directories, hotlines, and flyers creates barriers for those who need these services most—new immigrants, elderly residents, and low-income families.  

This lack of accessible information leads to **underutilization of available programs**, duplicated effort across organizations, and added stress for individuals in already vulnerable situations. A streamlined, AI-powered platform could dramatically improve equity of access by providing **plain-language, conversational search** across community resources.  

---

## 📚 Prior Systems & Gaps
Several systems exist today:

- **211 Hotlines**: Widely known but limited to phone access, with wait times, language barriers, and inconsistent availability.  
- **Community Websites & Directories**: Typically static, often outdated, and difficult to navigate for users with low digital literacy.  
- **Mobile Apps by NGOs**: Fragmented, require heavy manual updates, and limited adoption.  

**Gaps Identified (via literature):**
- *Sezgin et al. (2024)* show that chatbots like DAPHNE improve access but struggle with dataset freshness and empathy in tone.  
- *Mekni & Haynes (2020)* highlight scalability issues in recommendation platforms.  
- *Rahmani et al. (2021)* demonstrate that hybrid semantic + lexical search outperforms keyword-only retrieval, but this is rarely used in social service platforms.  
- *Perron et al. (2024)* caution that embedding models risk bias if not domain-adapted.  

Taken together, prior systems lack **robust retrieval**, **multilingual inclusivity**, and **ease of deployment** for community-scale use.

---

## 💡 Proposed Approach
The **Community Resource Navigator** will be a lightweight, AI-driven prototype designed for solo development. Key features:

1. **Retrieval-Augmented Chatbot**:  
   - User inputs plain-language questions (*“Where is the nearest free clinic?”*).  
   - System searches a small structured dataset (CSV/SQLite) using **Sentence-Transformer embeddings (MiniLM)** combined with **BM25 lexical search**.  

2. **Concise Summaries**:  
   - Service cards with name, address, hours, and eligibility, inspired by DAPHNE’s structured outputs.  

3. **Multilingual Support**:  
   - Leverage Hugging Face translation pipelines to handle Spanish/English queries.  

4. **Simple Interface**:  
   - Built in **Streamlit**, making it easy to deploy and test.  

5. **Scalable Foundations**:  
   - Schema design influenced by Mattingly et al. (2016), so the dataset can be extended or reused later.  

**Why This Improves on Prior Art:**
- More lightweight and maintainable than large NGO platforms.  
- Hybrid search addresses retrieval accuracy gaps highlighted by Rahmani et al. (2021).  
- Designed with empathy and inclusivity (multilingual, plain-language responses) based on insights from Sezgin et al. (2024).  
- Feasible for a single developer, but extensible for future class or community contributions.  

---

## ✅ Plan for Checkpoint 2 Validation (Prompt-Based)
To validate the concept, I will conduct a **prompting study across ≥3 existing tools** (e.g., ChatGPT, Perplexity, Copilot, NotebookLM).  

**Protocol:**  
- Prepare a set of scenarios:  
  - *Typical Case*: “Where is the nearest food pantry in Champaign?”  
  - *Edge Case*: “What if I need free childcare and housing help at the same time?”  
  - *Failure Case*: “Find me services open past 10pm” (rarely exists).  
- Compare responses across tools for **accuracy, reliability, UX friction, latency, and safety**.  
- Record transcripts, sanitize outputs, and categorize gaps.  

**Expected Outcome:**  
Identify **specific product requirements** (structured outputs, dataset freshness, multilingual UX) that current tools fail to meet, forming the foundation of the Navigator.  

---

## ⚠️ Initial Risks & Mitigation
1. **Privacy & Safety**  
   - Risk: Users may share sensitive personal info in queries.  
   - Mitigation: Prototype explicitly disclaims data storage; no logging of inputs beyond testing.  

2. **Bias in Models**  
   - Risk: Pretrained embeddings may reflect stereotypes.  
   - Mitigation: Test prompts for fairness; document observed biases; use neutral, factual responses.  

3. **Reliability of Dataset**  
   - Risk: Community data becomes outdated quickly.  
   - Mitigation: Start with synthetic/mock data; design schema to allow easy updating later.  

4. **Overpromising**  
   - Risk: Users may assume chatbot is authoritative.  
   - Mitigation: Include disclaimers; frame as **prototype** only.  

---

## 🛠️ Open Issues & Milestones
Since I am working solo, I will own all deliverables.  

**Milestones**  
- **Week 1–2:** Create dataset schema and mock service CSV.  
- **Week 3–4:** Build baseline chatbot with hybrid search.  
- **Week 5–6:** Add multilingual support + structured summaries.  
- **Week 7–8:** Prototype Streamlit dashboard; conduct prompting study.  
- **Week 9:** Document results; refine based on feedback.  

**Open Issues**  
- How to best handle **multilingual evaluation**.  
- Whether to integrate a **translation model** or curate bilingual datasets.  
- Balancing **simplicity (solo dev)** with **research ambition (checkpoints, validation)**.  
