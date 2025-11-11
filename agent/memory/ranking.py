from __future__ import annotations
from typing import List, Tuple
from datetime import datetime
import math
from .models import Memory

def _age_hours(dt: datetime) -> float:
    return max(0.0, (datetime.utcnow() - dt).total_seconds() / 3600.0)

def score(memory: Memory, bm25_rank: int) -> float:
    """
    Lower is better (for sorting). Combine:
    - BM25 rank position
    - recency (hours since last accessed)
    - importance (0..1)
    """
    age = _age_hours(memory.last_accessed_at)
    # map to a small penalty; newer memories preferred
    recency_pen = math.log1p(age) # 0 for fresh; grows slowly
    importance_gain = (1.0 - memory.importance) * 2.0 # high importance -> negative gain
    return bm25_rank + recency_pen + importance_gain

def rerank(bm25_results: List[Memory]) -> List[(Memory)]:
    tuples: List[Tuple[float, Memory]] = []
    for i, m in enumerate(bm25_results):
        s = score(m, i + 1)
        tuples.append((s, m))
    tuples.sort(key=lambda x: x[0])
    return [m for _, m in tuples]
