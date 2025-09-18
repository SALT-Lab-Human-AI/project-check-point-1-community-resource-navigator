[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/lHqtj83j)

# Community Resource Navigator

---

## 📝 Problem Statement and Why It Matters
Finding community resources such as food pantries, free clinics, ESL classes, job training, and housing support is often difficult. Many residents—especially new immigrants, seniors, or low-income families—face barriers like outdated websites, overwhelming directories, or language challenges.  

This project aims to simplify the process by creating a **lightweight AI-powered tool** where users can ask questions in plain language and quickly receive relevant, easy-to-read answers.

---

## 🎯 Target Users and Core Tasks
**Target Users**
- Local residents seeking essential services.  
- Volunteers and case workers supporting community members.  

**Core Tasks**
1. **Ask Simple Questions:** *“Where is the nearest free clinic?”*  
2. **Retrieve Structured Information:** Return service name, location, hours, and contact info.  
3. **Basic Summarization:** Provide concise, easy-to-read service details.  

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
- Designed as a **prototype** that could later expand into a full system.  

---

## 🛠️ Tools and Technologies
- **Backend/Logic:** Python (FastAPI or Flask).  
- **Data Storage:** CSV or SQLite (small dataset of community services).  
- **AI/NLP:**  
  - **Sentence-Transformers (MiniLM)** for semantic search.  
  - Optionally a lightweight open-source LLM like **Mistral-7B-Instruct** or **Falcon-7B-Instruct** (via Hugging Face).  
- **Frontend:** Streamlit (for a simple prototype interface).  
- **Version Control:** Git/GitHub.  

---

## 📅 Milestones (Solo Project)
1. **Week 1:** Collect a small dataset of 20–30 local community services.  
2. **Week 2:** Implement simple semantic search (using Sentence-Transformers).  
3. **Week 3:** Build chatbot interface in Streamlit.  
4. **Week 4:** Add summarization feature (using Hugging Face model).  
5. **Week 5:** Testing, documentation, and cleanup.  

---

## 📬 Contact
Maintained by:  
📧 **[satviki2@illinois.edu]**
