from __future__ import annotations
import json, sqlite3, threading, re
from typing import Iterable, List, Tuple, Optional
from datetime import datetime
from .models import Memory

_SCHEMA = """
PRAGMA journal_mode=WAL;

CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    text TEXT NOT NULL,
    summary TEXT,
    tags TEXT NOT NULL,               -- JSON array of strings
    importance REAL NOT NULL,
    created_at TEXT NOT NULL,
    last_accessed_at TEXT NOT NULL,
    meta TEXT NOT NULL                -- JSON object
);

-- FTS5 index for BM25-style search
CREATE VIRTUAL TABLE IF NOT EXISTS fts_memories USING fts5(
    text, summary, tags, content='memories', content_rowid='id'
);

-- keep FTS in sync
CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
  INSERT INTO fts_memories(rowid, text, summary, tags)
  VALUES (new.id, new.text, coalesce(new.summary,''), new.tags);
END;

CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
  INSERT INTO fts_memories(fts_memories, rowid, text, summary, tags)
  VALUES ('delete', old.id, old.text, coalesce(old.summary,''), old.tags);
END;

CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
  INSERT INTO fts_memories(fts_memories, rowid, text, summary, tags)
  VALUES ('delete', old.id, old.text, coalesce(old.summary,''), old.tags);
  INSERT INTO fts_memories(rowid, text, summary, tags)
  VALUES (new.id, new.text, coalesce(new.summary,''), new.tags);
END;
"""

def _sanitize_to_fts_query(q: str) -> str:
    """
    Convert natural language into a tolerant FTS5 query.
    - keep alphanumerics
    - drop punctuation that confuses the parser (e.g., '?', ':', etc.)
    - OR-join tokens with prefix matches to avoid syntax errors
    """
    tokens = re.findall(r"[A-Za-z0-9_]+", q)
    if not tokens:
        return ""  # will return 0 rows cleanly
    # add '*' for prefix search where useful (skip tiny tokens)
    safe = " OR ".join([t if len(t) < 3 else f"{t}*" for t in tokens])
    return safe

class SQLiteMemoryStore:
    """
    Lightweight, fast store with FTS5 (BM25). No external dependencies.
    """

    def __init__(self, path: str = "agent_memory.db"):
        self.path = path
        self._lock = threading.RLock()
        with self._conn() as cx:
            cx.executescript(_SCHEMA)
            # Ensure FTS is fully populated from content table (no-op if fresh)
            try:
                cx.execute("INSERT INTO fts_memories(fts_memories) VALUES ('rebuild')")
            except sqlite3.OperationalError:
                # On old SQLite builds 'rebuild' may not exist; safe to ignore
                pass

    def _conn(self):
        cx = sqlite3.connect(self.path, check_same_thread=False)
        cx.row_factory = sqlite3.Row
        return cx

    def insert(self, m: Memory) -> int:
        with self._lock, self._conn() as cx:
            cur = cx.execute(
                """INSERT INTO memories(kind,text,summary,tags,importance,created_at,last_accessed_at,meta)
                   VALUES(?,?,?,?,?,?,?,?)""",
                (
                    m.kind,
                    m.text,
                    m.summary,
                    json.dumps(m.tags),
                    float(m.importance),
                    m.created_at.isoformat(),
                    m.last_accessed_at.isoformat(),
                    json.dumps(m.meta or {}),
                ),
            )
            return int(cur.lastrowid)

    def update_last_access(self, ids: Iterable[int]) -> None:
        now = datetime.utcnow().isoformat()
        ids = list(ids)
        if not ids:
            return
        with self._lock, self._conn() as cx:
            cx.executemany(
                "UPDATE memories SET last_accessed_at=? WHERE id=?",
                [(now, _id) for _id in ids],
            )

    def delete(self, ids: Iterable[int]) -> int:
        ids = list(ids)
        if not ids:
            return 0
        with self._lock, self._conn() as cx:
            cx.executemany("DELETE FROM memories WHERE id=?", [(i,) for i in ids])
            return cx.total_changes

    def search(self, query: str, limit: int = 8) -> List[Memory]:
        # Sanitize NL into FTS-friendly text
        fts_query = _sanitize_to_fts_query(query)
        if not fts_query:
            return []

        with self._lock, self._conn() as cx:
            rows = cx.execute(
                """
                SELECT m.*, bm25(fts_memories) AS score
                FROM fts_memories
                JOIN memories m ON m.id = fts_memories.rowid
                WHERE fts_memories MATCH ?
                ORDER BY score ASC
                LIMIT ?
                """,
                (fts_query, limit),
            ).fetchall()
        return [self._row_to_memory(r) for r in rows]

    def recent(self, limit: int = 20) -> List[Memory]:
        with self._lock, self._conn() as cx:
            rows = cx.execute(
                """
                SELECT * FROM memories
                ORDER BY datetime(last_accessed_at) DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [self._row_to_memory(r) for r in rows]

    def all_ids_with_scores(self) -> List[Tuple[int, float, str]]:
        with self._lock, self._conn() as cx:
            rows = cx.execute("SELECT id, importance, last_accessed_at FROM memories").fetchall()
        return [(r["id"], float(r["importance"]), r["last_accessed_at"]) for r in rows]

    def _row_to_memory(self, r: sqlite3.Row) -> Memory:
        return Memory(
            id=int(r["id"]),
            kind=r["kind"],
            text=r["text"],
            summary=r["summary"],
            tags=json.loads(r["tags"]) if r["tags"] else [],
            importance=float(r["importance"]),
            created_at=datetime.fromisoformat(r["created_at"]),
            last_accessed_at=datetime.fromisoformat(r["last_accessed_at"]),
            meta=json.loads(r["meta"]) if r["meta"] else {},
        )
