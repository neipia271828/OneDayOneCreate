from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationCase:
    name: str
    prompt: str
    external_text: str
    malicious: bool


@dataclass(frozen=True)
class GuardDecision:
    blocked: bool
    score: int
    reasons: tuple[str, ...]
    response: str
    leaked: bool
