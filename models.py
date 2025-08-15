# models.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    created_at: datetime

@dataclass
class Prompt:
    id: int
    user_id: int
    prompt_text: str
    intended_use: str
    llm_used: str
    performance_score: int
    outcome: str
    notes: str
    created_at: datetime
    updated_at: datetime
