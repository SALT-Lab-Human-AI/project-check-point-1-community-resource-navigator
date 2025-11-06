# 🧪 Community Resource Navigator – Use Cases and Test Scenarios

This document illustrates the core **end-to-end use cases** for the Community Resource Navigator and the **minimal test coverage** used to validate each critical path.  
Each use case demonstrates the combined behavior of the **retrieval engine** (BM25 + embeddings), **multi-source data integration** (CSV + Philly311), and the **Groq LLM summarization layer**.

---

## 1️⃣ Use Case 1 – Food Assistance (“Free dinner near 19107”)

**User goal:** Find free meal services available in Center City, Philadelphia.

**User input:**
> "free dinner near 19107"

**Data sources involved:**
- `services.csv` → Food pantries and outreach programs  
- Philly311 API → Recent service reports related to shelters or food access  
- SQLite `chat_history` → Boosts for previous food-related searches  

**System behavior:**
1. Load structured services from the CSV.  
2. Fetch live Philly311 data for food or shelter mentions.  
3. Merge both into a unified dataset.  
4. Perform hybrid retrieval (BM25 + embeddings).  
5. Pass top results to Groq LLM for summarization.  
6. Display 3 concise, human-readable recommendations.

**Expected answer (LLM-generated):**
1. **Chosen 300 Outreach Center** — Offers free hot dinners daily at 6pm near Spring Garden St.  
2. **Our Brother’s Place** — Provides meals and shelter for men near 19107.  
3. **St. Mark’s Food Cupboard** — Central food pantry open evenings on Locust St.

**Test coverage:**  
✅ `test_end_to_end.py` ensures retrieval → summarization flow executes successfully.

---

## 2️⃣ Use Case 2 – Shelter Assistance (“Homeless shelter open tonight”)

**User goal:** Locate open shelters offering emergency accommodation.

**User input:**
> "homeless shelter open tonight"

**Data sources involved:**
- `services.csv` → Shelter and housing programs  
- Philly311 API → Live requests tagged under “Homeless Encampment” or “Public Welfare”  

**System behavior:**
1. Filter CSV by category “Shelter.”  
2. Pull live 311 data for recent shelter-related reports.  
3. Rank combined data by textual relevance and semantic proximity.  
4. Summarize results into top 3 service recommendations.

**Expected answer:**
1. **Our Brother’s Place** — Provides overnight shelter and meals for men.  
2. **Women Against Abuse Safe Haven** — Emergency housing for women escaping domestic violence.  
3. **Philly311 Update** — Temporary warming center open tonight near Broad & Spring Garden.

**Test coverage:**  
✅ `test_retrieval.py` confirms hybrid search correctly ranks relevant shelter entries.

---

## 3️⃣ Use Case 3 – Health and Wellness (“Free medical clinic for uninsured people”)

**User goal:** Access low-cost or free medical services for uninsured residents.

**User input:**
> "free medical clinic for uninsured people"

**Data sources involved:**
- `services.csv` → Health centers and nonprofit clinics  
- Philly311 API → Reports mentioning “medical,” “clinic,” or “public health”  

**System behavior:**
- Hybrid retrieval detects semantic similarity (e.g., “clinic” ≈ “healthcare”).  
- Groq LLM rewrites dense text into natural, user-facing summaries.

**Expected answer:**
1. **Philadelphia FIGHT Clinic** — Offers free HIV and general health care for uninsured patients.  
2. **Community Health Center of West Philly** — Provides checkups and testing services.  
3. **Philly311 Report** — Recent pop-up vaccination event near Market Street.

**Test coverage:**  
✅ `test_data_loading.py` ensures CSV parsing and text preprocessing (retrieval_text) work properly.

---

## 4️⃣ Use Case 4 – City Services (“Trash collection complaints near 19148”)

**User goal:** View active public service requests for sanitation issues in South Philly.

**User input:**
> "trash collection complaints near 19148"

**Data sources involved:**
- Philly311 API (primary) → Live city service requests  
- `services.csv` → Local recycling or cleanup programs for context  

**System behavior:**
1. Query Philly311 endpoint for recent sanitation-related service requests.  
2. Merge with local CSV to surface long-term waste assistance programs.  
3. Display both:
   - Orange pins: active 311 complaints  
   - Blue pins: permanent local waste support services  
4. Summarize with LLM.

**Expected answer:**
1. **Philly311 Report** — Recent trash pickup delay reported near Passyunk Ave.  
2. **South Philly Clean Streets Program** — Local waste management initiative.  
3. **Philly311 Report** — Overflow bins request near Broad & Oregon.

**Test coverage:**  
✅ Live API fetch validated manually; error handling confirmed via empty-response fallback.

---

## 5️⃣ Use Case 5 – Multi-query Adaptation (User Context Reuse)

**Scenario:**  
The user first searches for “shelter for women,” then “meal programs near Center City.”

**Adaptive behavior:**  
- Past keywords (“women,” “shelter”) influence the next search.  
- `user_keywords` boost services with matching themes (e.g., “family,” “support,” “meals”).  
- Groq’s summary reflects this context:
  > “These food programs also provide assistance for women and families.”

**Test coverage:**  
✅ `test_end_to_end.py` validates that user history is read correctly and influences retrieval scoring.

---

## ⚙️ Non-functional Use Cases

| Aspect | Description | Verification |
|---------|--------------|--------------|
| **Authentication** | Prevents access without valid username/password. | Manual login test. |
| **Map Rendering** | Displays markers with color-coded sources. | Visual verification in Streamlit. |
| **Error Handling** | Missing API keys or empty datasets handled gracefully. | Unit tests + manual. |
| **Performance** | Response time for typical query < 3 seconds. | Manual + time log display. |

---

## ✅ Summary of Critical Path Tests

| Layer | Function | Test File | Expected Result |
|--------|-----------|------------|----------------|
| Data ingestion | `load_services_csv` | `test_data_loading.py` | DataFrame contains required columns |
| Coordinate parsing | `parse_latlon` | `test_data_loading.py` | Correct lat/lon tuples |
| Retrieval | `hybrid_search` | `test_retri
