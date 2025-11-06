import numpy as np
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from prototype.app import hybrid_search

def test_hybrid_search_topk():
    texts = ["Free meals for students", "Shelter for families", "Healthcare for seniors"]
    bm25 = BM25Okapi([t.lower().split() for t in texts])
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embs = embedder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    idx = hybrid_search("free food", bm25, embedder, embs, texts, df=None, k_final=2)
    assert len(idx) == 2
    assert isinstance(idx[0], (int, np.integer))
