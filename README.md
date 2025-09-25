# Community Resource Navigator

---

## 📝 Problem Statement and Why It Matters
Finding community resources such as food pantries, free clinics, ESL classes, job training, and housing support is often difficult. Many residents—especially new immigrants, seniors, or low-income families—face barriers like outdated websites, overwhelming directories, or language challenges.  

This project aims to simplify the process by creating a **lightweight AI-powered tool** where users can ask questions in plain language and quickly receive relevant, easy-to-read answers.  

> Example queries:  
> - “Where is the nearest free clinic open after 5pm?”  
> - “Shelters for women with children in 19107.”  
> - “Which centers offer showers and laundry?”

---

## 🎯 Target Users and Core Tasks
**Target Users**
- Local residents seeking essential services.  
- Volunteers and case workers supporting community members.  

**Core Tasks**
1. **Ask Simple Questions:** *“Where is the nearest free clinic?”*  
2. **Retrieve Structured Information:** Return service name, location, hours, and contact info.  
3. **Basic Summarization:** Provide concise, easy-to-read service details.  
4. **Transparency:** Expandable “sources” view shows the original dataset row(s).  

---

## 🏆 Competitive Landscape
**Existing Tools**
- **211 Hotlines** – useful but slow and limited to phone access.  
- **Community Websites/Directories** – often outdated or hard to navigate.  

**Shortcomings**
- Hard for users with low digital literacy.  
- Not conversational or multilingual.  
- Limited personalization.  

---

## 💡 Initial Concept and Value Proposition
The **Community Resource Navigator** will be a **simple chatbot prototype** that:  
- Uses **open-source NLP models** for natural language search.  
- Stores information in a **structured dataset (CSV/JSON)**.  
- Returns **concise answers** with relevant service details.  
- Provides a **basic web interface** for testing queries.  

**Value Proposition**
- Quick and accessible way to find community services.  
- Easy to maintain with simple datasets.  
- Designed as a **prototype** that could later expand into a full system (multilingual, geospatial, volunteer-facing dashboards).  

---

## 📊 Dataset
The current dataset (`data/services.csv`) contains **~100 entries** of Philadelphia-based resources with fields like:

| Column | Purpose |
|--------|---------|
| `Category` | Type of service (e.g., Food, Shelter, Medical, Legal, Housing) |
| `Organization Name` | Service provider |
| `Address` / `Zip Code` | Location info |
| `Days`, `Time: Open`, `Time: Close` | Hours of operation |
| `People Served` | Eligibility (Men, Women, Families, Children) |
| `Description` | Details of services |
| `Phone Number` | Contact |
| `LatLon` | Geographic coordinates (for future “near me” queries) |

---

## 🛠️ Tools and Technologies
- **Backend/Logic:** Python (FastAPI or Flask).  
- **Data Storage:** CSV or SQLite (community services).  
- **AI/NLP:**  
  - **Sentence-Transformers (MiniLM)** for semantic search.  
  - Optionally a lightweight open-source LLM like **Mistral-7B-Instruct** or **Falcon-7B-Instruct** (via Hugging Face).  
- **Frontend:** Streamlit (for a simple prototype interface).  
- **Version Control:** Git/GitHub.  

---

## 🧪 Prototype (Screenshots)
_These are placeholders — replace with actual screenshots once the Streamlit UI runs._

- **Search Interface**  
  ![Search](docs/screens/01_search.png)  

- **Generated Service Cards**  
  ![Results](docs/screens/02_cards.png)  

- **Expandable Sources Panel**  
  ![Sources](docs/screens/03_sources.png)  

---

## 🔄 Process
1. **Load & Normalize Data**  
   - Read CSV, unify columns (name, address, hours, eligibility, description).  
   - Create `retrieval_text` for embeddings + BM25.  

2. **Hybrid Retrieval**  
   - BM25 keyword search.  
   - MiniLM embeddings for semantic similarity.  
   - Fuse results → top-k rows.  

3. **Answer Generation**  
   - Option A: **Offline fallback** (template-based cards).  
   - Option B: **LLM (OpenAI/HF)** → grounded summarization prompt.  

4. **Display in Streamlit**  
   - Main: conversational answer + service cards.  
   - Sidebar: dataset info / settings.  
   - Expander: raw retrieved rows for transparency.  

---

## 📅 Milestones (Solo Project)
1. **Week 1:** Collect a small dataset of 20–30 local community services.  
2. **Week 2:** Implement simple semantic search (using Sentence-Transformers).  
3. **Week 3:** Build chatbot interface in Streamlit.  
4. **Week 4:** Add summarization feature (using Hugging Face model).  
5. **Week 5:** Testing, documentation, and cleanup.  

---

## 🔐 Privacy, Safety, Attribution
- **Privacy:** No personal data stored; queries are not logged.  
- **Safety:** Model grounded in dataset only; fallback policy = “I don’t know.”  
- **Attribution:** Dataset source documented; model cards acknowledged (e.g., Hugging Face, OpenAI).  

---

## 📬 Contact
Maintained by:  
📧 **satviki2@illinois.edu**

---
