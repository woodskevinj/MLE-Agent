from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Literal, Dict
from datetime import datetime

MemoryKind = Literal["episodic", "semantic", "working"]

@dataclass
class Memory:
    id: Optional[int]
    kind: MemoryKind
    text: str                           # raw content
    summary: Optional[str] = None       # short auto-summary
    tags: List[str] = field(default_factory=list)
    importance: float = 0.5             # 0..1
    create_at: datetime = field(default_factory=datetime.utcnow)
    last_accessed_at: datetime = field(default_factory=datetime.utcnow)
    meta: Dict[str, str] = field(default_factory=dict)      # e.g., {"task_id":"...", "tool":"search"}
    