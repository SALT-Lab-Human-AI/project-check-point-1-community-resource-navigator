from prototype.app import (
    load_services_csv,
    build_indexes,
    hybrid_search,
    groq_generate_answer
)

def test_end_to_end_pipeline(monkeypatch):
    df = load_services_csv("data/services.csv").head(10)
    bm25, embedder, embs = build_indexes(df["retrieval_text"].tolist())

    # Monkeypatch Groq API to avoid hitting real endpoint
    monkeypatch.setattr("prototype.app.groq_generate_answer",
                        lambda q, r: "1. Demo Org — Provides free meals\n2. Demo 2 — Shelter help\n3. Demo 3 — Health clinic")

    hits = hybrid_search("free meals", bm25, embedder, embs, df["retrieval_text"].tolist(), df, k_final=3)
    rows = df.iloc[hits].to_dict(orient="records")

    answer = groq_generate_answer("free meals", rows)
    assert "Demo Org" in answer
