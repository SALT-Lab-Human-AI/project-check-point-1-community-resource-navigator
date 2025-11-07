import os
import re
import time
import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import streamlit as st
import pydeck as pdk
from dotenv import load_dotenv
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer

# -------------------------
# 0) CONFIG & ENV
# -------------------------
load_dotenv()

DATA_PATH = os.getenv("DATA_PATH", "data/services.csv")
EMB_MODEL = os.getenv("EMB_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
TOPK_BM25 = int(os.getenv("TOPK_BM25", "20"))
TOPK_FINAL = int(os.getenv("TOPK_FINAL", "5"))
DB_PATH = os.getenv("DB_PATH", "data/app.db")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama-3.3-70b-versatile"

PHILLY311_URL = "https://api.phila.gov/311/v1/requests"

# -------------------------
# 1) UI CONFIG + STYLING
# -------------------------
st.set_page_config(
    page_title="Community Resource Navigator",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

def load_css(file_name: str):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("prototype/styles.css")

# -------------------------
# 2) USER DATA & AUTH
# -------------------------
VALID_USERS = {"user1": "password1", "user2": "password2"}
USER_DISPLAY = {"user1": "Demo User 1", "user2": "Demo User 2"}

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            query TEXT,
            response TEXT,
            timestamp TEXT
        )
    """)
    conn.commit(); conn.close()

def save_chat(username, query, response):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO chat_history (username, query, response, timestamp) VALUES (?,?,?,?)",
                (username, query, response, datetime.utcnow().isoformat()))
    conn.commit(); conn.close()

def load_user_history(username, limit=10):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT query, response, timestamp FROM chat_history WHERE username=? ORDER BY id DESC LIMIT ?",
                (username, limit))
    rows = cur.fetchall(); conn.close()
    return rows

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # existing chat_history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            query TEXT,
            response TEXT,
            timestamp TEXT
        )
    """)
    # new users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit(); conn.close()

import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


def require_login():
    if "username" not in st.session_state:
        st.session_state["username"] = None

    if st.session_state["username"] is None:
        st.title("🧭 Community Resource Navigator")

        tabs = st.tabs(["Login", "Create Account"])

        # ----- LOGIN TAB -----
        with tabs[0]:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")

            if st.button("Login", key="login_button"):
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, name, email, password_hash FROM users WHERE email=?",
                    (email,)
                )
                user = cur.fetchone()
                conn.close()

                if user and verify_password(password, user[3]):
                    # store the user's name in session
                    st.session_state["username"] = user[1]
                    st.success(f"Welcome back, {user[1]}!")
                    st.rerun()
                else:
                    st.error("Invalid email or password.")

        # ----- CREATE ACCOUNT TAB -----
        with tabs[1]:
            name = st.text_input("Full Name", key="signup_name")
            new_email = st.text_input("Email (for login)", key="signup_email")
            new_pass = st.text_input("Password", type="password", key="signup_password")

            if st.button("Create Account", key="signup_button"):
                if name and new_email and new_pass:
                    conn = sqlite3.connect(DB_PATH)
                    cur = conn.cursor()
                    try:
                        cur.execute(
                            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
                            (name, new_email, hash_password(new_pass))
                        )
                        conn.commit()
                        st.success("Account created! You can now log in.")
                    except sqlite3.IntegrityError:
                        st.error("This email is already registered.")
                    conn.close()
                else:
                    st.warning("Please fill in all fields.")

        # stop rendering the rest of the app until user logs in
        st.stop()

    return st.session_state["username"]


# -------------------------
# 3) DATA & RETRIEVAL
# -------------------------
def load_services_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    rename = {"Organization Name":"name","Category":"category","Address":"address",
              "People Served":"eligibility","Description":"description",
              "Phone Number":"phone","LatLon":"latlon","Days":"days",
              "Time: Open":"open","Time: Close":"close"}
    df.rename(columns={k:v for k,v in rename.items() if k in df.columns}, inplace=True)
    for c in ["name","category","address","eligibility","description","phone","days","open","close","latlon"]:
        if c not in df.columns: df[c] = ""
    def normalize_hours(d, o, c):
        parts = []
        for val, label in [(d, ""), (o, "Open: "), (c, "Close: ")]:
            if isinstance(val, (int, float)) and pd.notna(val):
                val = str(int(val)) if val.is_integer() else str(val)
            if isinstance(val, str) and val.strip():
                parts.append(f"{label}{val.strip()}")
        return " | ".join(parts) if parts else ""

    df["hours"] = [normalize_hours(d,o,c) for d,o,c in zip(df["days"],df["open"],df["close"])]
    df["retrieval_text"] = (
        "Name: "+df["name"]+" | Category: "+df["category"]+" | Address: "+df["address"]+
        " | Hours: "+df["hours"]+" | People Served: "+df["eligibility"]+" | Description: "+df["description"]
    )
    df["lat"],df["lon"] = zip(*df["latlon"].apply(lambda v: (None,None) if not isinstance(v,str) or "," not in v else (float(v.split(",")[1]),float(v.split(",")[0]))))
    df["source"] = "local"
    return df.fillna("")

def load_philly311_data(query: str, limit: int = 50) -> pd.DataFrame:
    """Fetch and normalize live Philly311 data."""
    try:
        params = {"limit": limit}
        resp = requests.get(PHILLY311_URL, params=params, timeout=5)
        if not resp.ok:
            return pd.DataFrame()
        data = resp.json().get("service_requests", [])
        records = []
        for d in data:
            desc = (d.get("service_name", "") + " - " + str(d.get("description", ""))).strip()
            if query.lower() in desc.lower():
                records.append({
                    "name": d.get("service_name", "Philly311 Request"),
                    "category": "311 City Service",
                    "address": d.get("address", "N/A"),
                    "eligibility": "",
                    "description": desc,
                    "phone": "",
                    "days": "",
                    "open": "",
                    "close": "",
                    "hours": "",
                    "latlon": f"{d.get('long', '')},{d.get('lat', '')}",
                    "lat": d.get("lat", None),
                    "lon": d.get("long", None),
                    "source": "philly311"
                })
        df = pd.DataFrame(records)
        if not df.empty:
            df["retrieval_text"] = (
                "Name: " + df["name"].astype(str) +
                " | Category: " + df["category"].astype(str) +
                " | Address: " + df["address"].astype(str) +
                " | Description: " + df["description"].astype(str)
            )
        return df
    except Exception as e:
        print(f"Philly311 fetch error: {e}")
        return pd.DataFrame()

@st.cache_resource
def build_indexes(texts):
    bm25 = BM25Okapi([t.lower().split() for t in texts])
    embedder = SentenceTransformer(EMB_MODEL)
    embs = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return bm25, embedder, embs

def hybrid_search(query,bm25,embedder,embs,texts,df,user_keywords=None,k_bm25=20,k_final=7):
    sb = bm25.get_scores(query.lower().split())
    q = embedder.encode([query],convert_to_numpy=True,normalize_embeddings=True)[0]
    se = embs @ q
    sb=(sb-sb.min())/(sb.max()-sb.min()+1e-9); se=(se-se.min())/(se.max()-se.min()+1e-9)
    fused=0.6*sb+0.4*se
    if user_keywords:
        boost=df["retrieval_text"].apply(lambda x:any(kw.lower() in x.lower() for kw in user_keywords)).astype(float)
        fused+=0.2*boost.values
    top_idx=np.argsort(fused)[::-1][:k_final]
    return top_idx

# -------------------------
# 4) GROQ HELPERS
# -------------------------
def groq_generate_answer(query,rows):
    if not GROQ_API_KEY: return "Missing GROQ_API_KEY."
    context="\n".join([f"- {r['name']} | {r['address']} | {r['category']} ({r.get('source','local')})" for r in rows])
    prompt = f"""
You are a helpful assistant for finding local services in Philadelphia.

User query: "{query}"

Here are the top relevant services (from local data and Philly311):
{context}

If you find at least one relevant match, return exactly 3 helpful matches like this:
1. Name — one-line factual summary
2. Name — one-line factual summary
3. Name — one-line factual summary

If none of the provided services match the request, do **not apologize**.
Instead, recommend **the 3 closest categories or related resources** from the list.
"""

    headers={"Authorization":f"Bearer {GROQ_API_KEY}","Content-Type":"application/json"}
    body={"model":GROQ_MODEL,"messages":[{"role":"system","content":"Helpful factual assistant."},{"role":"user","content":prompt}],
          "temperature":0.3,"max_tokens":300}
    try:
        resp=requests.post(GROQ_URL,headers=headers,json=body)
        data=resp.json()
        if "choices" in data: return data["choices"][0]["message"]["content"]
        return "⚠️ Groq error"
    except Exception as e:
        return f"Groq error: {e}"

# -------------------------
# 5) APP MAIN
# -------------------------
init_db()
df=load_services_csv(DATA_PATH)
bm25,embedder,embs=build_indexes(df["retrieval_text"].tolist())

username=require_login()
display_name=USER_DISPLAY.get(username,username)

if st.sidebar.button("Logout"):
    st.session_state["username"]=None; st.rerun()

st.sidebar.success(f"Logged in as {display_name}")
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;">
<h2 style="color:white; font-weight:800;">🧭 Community Resource Navigator</h2>
<span style="color:#666;">AI-powered local support finder for Philadelphia</span>
</div>
""", unsafe_allow_html=True)

# --- Sidebar filters & history
with st.sidebar:
    st.markdown("### Filters")
    sel_cat=st.multiselect("Category",sorted([c for c in df["category"].unique() if str(c).strip()]),[])
    sel_group=st.multiselect("People Served",["Women","Men","Families","Children"],[])
    st.markdown("---"); st.markdown("### Recent Searches")
    for i,(q,_,ts) in enumerate(load_user_history(username,limit=5)):
        if st.button(f"🔁 {q}",key=f"hist_{i}"):
            st.session_state["user_query"]=q; st.rerun()

# --- Main layout
col1,col2=st.columns([2,1])
with col1:
    st.markdown("### Ask for help")
    query=st.text_input("What do you need?",value=st.session_state.get("user_query",""),placeholder="e.g., free dinner near 19107 on Sunday")
    if st.button("Search") and query.strip():
        q=query.strip(); t0=time.time()
        query_parts = [q]

        if sel_cat:
            query_parts.append("Categories: " + ", ".join(sel_cat))
        if sel_group:
            query_parts.append("People Served: " + ", ".join(sel_group))

        # Final unified query (this will go into BM25 + embeddings)
        final_query = " ".join(query_parts)

        sub_df = df.copy()


        # --- Load additional Philly311 data
        philly_df=load_philly311_data(q)
        combined_df=pd.concat([sub_df,philly_df],ignore_index=True)

        history_rows=load_user_history(username,limit=5)
        user_keywords=[w for h in history_rows for w in re.findall(r"\\b\\w+\\b",h[0].lower()) if len(w)>3]

        texts=combined_df["retrieval_text"].tolist()
        bm25_f=BM25Okapi([t.lower().split() for t in texts])
        embs_f=embedder.encode(texts,convert_to_numpy=True,normalize_embeddings=True)
        hits=hybrid_search(final_query,bm25_f,embedder,embs_f,texts,combined_df,user_keywords=user_keywords,k_bm25=TOPK_BM25,k_final=TOPK_FINAL)
        rows=combined_df.iloc[hits].to_dict(orient="records")

        with st.spinner("Generating recommendations..."):
            answer=groq_generate_answer(q,rows)
        save_chat(username,q,answer)

        st.markdown("### 🔍 Recommended Services")
        st.caption(f"Generated in {time.time()-t0:.2f}s (includes live Philly311 data)")

        lines = [l.strip() for l in answer.split("\n") if l.strip()]
        for i, line in enumerate(lines, start=1):
            name_desc = re.split(r"\d+\.\s+", line)[-1].strip()
            name, desc = (name_desc.split("—", 1) + [""])[:2]
            name = name.strip()
            desc = desc.strip()

            matched = next((r for r in rows if r["name"].lower() in name.lower()), None)

            st.markdown(f"### 🏠 {i}. {name}")
            st.write(desc)

            if matched:
                with st.expander("📋 Details"):
                    st.write(f"**Source:** {matched.get('source','local')}")
                    st.write(f"**Address:** {matched.get('address', 'N/A')}")
                    if matched.get("phone"):
                        st.write(f"📞 **Phone:** [{matched['phone']}](tel:{matched['phone']})")
                    if matched.get("hours"):
                        st.write(f"🕓 **Hours:** {matched['hours']}")
                    
                    if matched.get("address") and isinstance(matched["address"], str) and matched["address"].strip():
                        st.markdown(f"[🌐 Open in Google Maps](https://www.google.com/maps/search/?api=1&query={matched['address'].replace(' ', '+')})")
            st.markdown("---")

with col2:
    st.markdown("### 📍 Map of Services")
    if "rows" in locals() and rows:
        map_df=pd.DataFrame([{"lat":r["lat"],"lon":r["lon"],"name":r["name"],"category":r["category"],"source":r.get("source","local")} for r in rows if r.get("lat") and r.get("lon")])
        if not map_df.empty:
            layer=pdk.Layer("ScatterplotLayer",data=map_df,get_position=["lon","lat"],get_radius=120,
                            get_fill_color=["source == 'philly311' ? 255 : 46",
                                            "source == 'philly311' ? 165 : 103",
                                            "source == 'philly311' ? 0 : 209",180],
                            pickable=True)
            deck = pdk.Deck(
                map_style=None,  # disables Mapbox, uses default OpenStreetMap
                layers=[layer],
                initial_view_state=pdk.ViewState(
                    latitude=39.9526,
                    longitude=-75.1652,
                    zoom=11
                ),
            tooltip={"text": "{name}\n{category}\n(Source: {source})"}
)

            st.pydeck_chart(deck)
        else:
            st.caption("No mappable locations yet.")
