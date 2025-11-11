from __future__ import annotations
from typing import List, Optional, Dict
from datetime import datetime
from .models import Memory
from .store import SQLiteMemoryStore
from . import ranking

_DEFAULT_CONTEXT_BUDGET_CHARS = 2400 # keep it model-agnostic

class MemoryModule:
    def __init__(self, db_path: str = "agent_memory.db"):
        self.store = SQLiteMemoryStore(db_path)

    # ------------write-------------------
    def remember(
            self,
            text: str,
            *,
            kind: str = "episodic",
            tags: Optional[List[str]] = None,
            importance: float = 0.5,
            summary: Optional[str] = None,
            meta: Optional[Dict[str, str]] = None,
    ) -> int:
        m = Memory(
            id=None,
            kind=kind, text=text,
            summary=summary,
            tags=tags or [],
            importance=max(0.0, min(1.0, importance)),
            meta=meta or {}
        )
        return self.store.insert(m)
    
    #------------read---------------
    def redcall(self, query: str, k: int = 8) -> List[Memory]:
        # Accept natural or FTS query. Examples:
        # 'tool failure near:docker'
        # 'user:Kevin AND project:visionsense'
        results = self.store.search(query, limit=max(1, k * 2)) # get a few extra
        reranked = ranking.rerank(results)
        top = reranked[:k]
        self.store.update_last_access([m.id for m in top if m.id is not None])
        return top
    
    def recent(self, k: int = 12) -> List[Memory]:
        return self.store.recent(limit=k)
    
    # ---------------- context assembly ---------------------
    def context(self, task: str, token_budget_chars: int = _DEFAULT_CONTEXT_BUDGET_CHARS) -> str:
        # build a compact context: recent + task-relevant + high-importance facts
        buckets: List[str] = []

        # 1. task-specific search
        rel = self.recal(task, k=6)
        if rel:
            buckets.append(_format_block("Task-Relevant Memories", rel))

        # 2. most recent episodic traces
        recent_mem = self.recent(k=8)
        if recent_mem:
            buckets.append(_format_block("Recent Session", recent_mem))

        # 3. optional: top pinned/important facts
        # You can fetch by FTS query: tags:'pinned' if yo udecide to tag them
        pinned = self.recall("tags:pinned", k=3)
        if pinned:
            buckets.append(_format_block("Pinned Facts", pinned))

        ctx = "\n\n".join(buckets)
        if len(ctx) > token_budget_chars:
            ctx = ctx[: token_budget_chars - 200] + "\n\n[...truncated memory...]"
        return ctx
    
    # ------------------ maintenance ------------------------
    def decay(self, min_importance: float = 0.15, hours_threshold: float = 72.0) -> None:
        """
        Reduce importance slightly for old items; prefer to prune only truly low-value/stale ones.
        """
        rows = self.store.all_ids_with_scores()
        to_update = []
        now = datetime.utcnow()

        # NOTE: we don't expose batch importance updates on the store for brevity; you can add one.
        # For now we will do nothin here to keep the API smal (placeholder)

    def prune(self, max_items: int = 5000, drop_below: float = 0.10) -> int:
        """
        Evict low-importance items when exceeding size cap.
        """
        rows = self.store.all_ids_with_scores()
        if len(rows) <= max_items:
            return 0
        
        # Sort by importance asc, then oldest access first
        rows.sort(key=lambda r: (r[1], r[2]))
        to_delete = [r[0] for r in rows if r[1] <= drop_below]
        # keep within cap
        overflow = len(rows) - max_items
        if overflow > 0:
            to_delete = to_delete[:max(overflow, 0)]
        return self.store.delete(to_delete)
    

def _format_block(title: str, ms: List[Memory]) -> str:
    lines = [f"### {title}"]
    for m in ms:
        tag_str = f" [{','.join(m.tags)}]" if m.tags else ""
        summ = f" - {m.summary}" if m.summary else ""
        lines.append(f" - ({m.kind}{tag_str}; imp={m.importance:.2f}) {m.text}{summ}")
    return "\n".join(lines)