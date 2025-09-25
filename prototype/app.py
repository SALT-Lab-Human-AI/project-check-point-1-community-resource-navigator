import os
import re
import time
import pandas as pd
import numpy as np
import streamlit as st
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

DATA_PATH = os.getenv("DATA_PATH", "data/services.csv")
EMB_MODEL = os.getenv("EMB_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOPK_BM25 = int(os.getenv("TOPK_BM25", "20"))
TOPK_FINAL = int(os.getenv("TOPK_FINAL", "5"))

# -------------------------
# 1) DATA LOADING & CLEANING
# -------------------------
def split_latlon(val):
    try:
        lon, lat = val.split(",")
        return float(lat.strip()), float(lon.strip())  # store as (lat, lon)
    except Exception:
        return None, None

def normalize_hours(days_raw, open_t, close_t):
    """Keep this simple for MVP. We’ll just combine text—don’t overfit parsing yet."""
    parts = []
    if isinstance(days_raw, str) and days_raw.strip():
        parts.append(days_raw.strip())
    if isinstance(open_t, str) and open_t.strip():
        parts.append(f"Open: {open_t.strip()}")
    if isinstance(close_t, str) and close_t.strip():
        parts.append(f"Close: {close_t.strip()}")
    return " | ".join(parts) if parts else ""

def load_services_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    # Make robust to casing
    rename = {
        "Id": "id",
        "Category": "category",
        "Organization Name": "name",
        "Address": "address",
        "Zip Code": "zip",
        "Days": "days",
        "Time: Open": "open",
        "Time: Close": "close",
        "People Served": "eligibility",
        "Description": "description",
        "Phone Number": "phone",
        "LatLon": "latlon",
    }
    for k,v in rename.items():
        if k in df.columns:
            df.rename(columns={k:v}, inplace=True)

    # Ensure missing columns exist
    for col in ["id","category","name","address","zip","days","open","close","eligibility","description","phone","latlon"]:
        if col not in df.columns:
            df[col] = ""

    # Lat/Lon split
    lats, lons = [], []
    for v in df["latlon"].astype(str).tolist():
        lat, lon = split_latlon(v)
        lats.append(lat)
        lons.append(lon)
    df["lat"] = lats
    df["lon"] = lons

    # Hours string
    df["hours"] = [normalize_hours(d, o, c) for d,o,c in zip(df["days"], df["open"], df["close"])]

    # Retrieval text (concise but rich)
    df = df.fillna("")
    df["retrieval_text"] = (
        "Name: " + df["name"].astype(str) + " | "
        "Category: " + df["category"].astype(str) + " | "
        "Address: " + df["address"].astype(str) + " | "
        "Zip: " + df["zip"].astype(str) + " | "
        "Hours: " + df["hours"].astype(str) + " | "
        "Eligibility: " + df["eligibility"].astype(str) + " | "
        "Description: " + df["description"].astype(str) + " | "
        "Phone: " + df["phone"].astype(str)
    )
    return df

# -------------------------
# 2) HYBRID RETRIEVAL
# -------------------------
@st.cache_resource
def build_indexes(texts):
    bm25 = BM25Okapi([t.lower().split() for t in texts])
    embedder = SentenceTransformer(EMB_MODEL)
    embs = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return bm25, embedder, embs

def hybrid_search(query, bm25, embedder, embs, texts, k_bm25=20, k_final=5):
    # BM25
    scores_b = bm25.get_scores(query.lower().split())
    idx_b = np.argsort(scores_b)[::-1][:k_bm25]
    # Embeddings
    q = embedder.encode([query], convert_to_numpy=True, normalize_embeddings=True)[0]
    scores_e = embs @ q
    idx_e = np.argsort(scores_e)[::-1][:k_bm25]
    # Union + fused score
    cand = list(set(idx_b).union(set(idx_e)))
    fused = [(i, 0.5*scores_b[i] + 0.5*scores_e[i]) for i in cand]
    fused.sort(key=lambda x:x[1], reverse=True)
    return [i for i,_ in fused[:k_final]]

# -------------------------
# 3) GENERATION (OFFLINE BASELINE)
# -------------------------
def card_from_row(r):
    parts = []
    if r.get("name"): parts.append(f"**{r['name']}**")
    if r.get("category"): parts.append(f"_{r['category']}_")
    if r.get("address"): parts.append(r["address"])
    if r.get("hours"): parts.append(f"Hours: {r['hours']}")
    if r.get("eligibility"): parts.append(f"Eligibility: {r['eligibility']}")
    if r.get("phone"): parts.append(f"Phone: {r['phone']}")
    return " • ".join(parts)

def offline_answer(query, rows):
    if not rows:
        return ("I don't know. I couldn't find a relevant service in the current dataset. "
                "You might broaden your query or call 211 for updated options.")
    cards = "\n".join([f"- {card_from_row(r)}" for r in rows[:3]])
    return f"Here are some options:\n\n{cards}\n\n(Verify hours by calling ahead.)"

# -------------------------
# 4) STREAMLIT UI
# -------------------------
st.set_page_config(page_title="Community Resource Navigator", page_icon="🧭", layout="wide")
st.title("🧭 Community Resource Navigator")
st.caption("Generative AI + RAG to find local services fast (prototype)")

df = load_services_csv(DATA_PATH)
bm25, embedder, embs = build_indexes(df["retrieval_text"].tolist())

with st.sidebar:
    st.markdown("### Dataset")
    st.write(f"Rows: {len(df)}")
    st.write("City: Philadelphia (prototype)")
    st.markdown("**Filters (optional MVP)**")
    sel_cat = st.multiselect("Category", sorted([c for c in df["category"].unique() if str(c).strip()]), [])
    sel_group = st.multiselect("People Served", ["Women","Men","Families","Children"], [])

query = st.text_input("What do you need?", placeholder="e.g., free dinner near 19107 on Sunday")
go = st.button("Search")

if go or query.strip():
    q = query.strip()
    t0 = time.time()
    # Filter pre-candidates (simple, optional)
    mask = pd.Series([True]*len(df))
    if sel_cat:
        mask &= df["category"].astype(str).str.contains("|".join([re.escape(x) for x in sel_cat]), case=False, na=False)
    if sel_group:
        mask &= df["eligibility"].astype(str).str.contains("|".join([re.escape(x) for x in sel_group]), case=False, na=False)
    sub_idx = df[mask].index.tolist()
    texts = df.loc[sub_idx, "retrieval_text"].tolist()

    if not texts:
        st.warning("No rows match current filters. Clearing filters might help.")
    else:
        # Build temporary indexes for filtered subset (fast for < few thousand rows)
        bm25_f = BM25Okapi([t.lower().split() for t in texts])
        embs_f = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        # Map filtered indices back to original df indices
        hits_local = hybrid_search(q, bm25_f, embedder, embs_f, texts, k_bm25=TOPK_BM25, k_final=TOPK_FINAL)
        hits_global = [sub_idx[i] for i in hits_local]
        rows = df.iloc[hits_global].to_dict(orient="records")
        answer = offline_answer(q, rows)
        st.markdown("### Answer")
        st.write(answer)
        st.caption(f"Latency: {time.time()-t0:.2f}s")

        with st.expander("See retrieved sources"):
            for r in rows:
                st.markdown(f"- **{r.get('name','')}**, {r.get('address','')}  \n"
                            f"  _{r.get('category','')}_  \n"
                            f"  Hours: {r.get('hours','')}  \n"
                            f"  People served: {r.get('eligibility','')}  \n"
                            f"  Phone: {r.get('phone','')}")
