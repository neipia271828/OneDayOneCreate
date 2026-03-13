from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .case_factory import build_generated_cases
from .models import GuardDecision, SimulationCase
from .scanner import PromptScanner


class ProtectedAgent:
    def __init__(self, api_key: str, block_threshold: int = 6) -> None:
        self.api_key = api_key
        self.block_threshold = block_threshold
        self.scanner = PromptScanner()

    def handle(self, prompt: str, external_text: str = "") -> GuardDecision:
        scan = self.scanner.scan(prompt, external_text)
        reasons = tuple(match.name for match in scan.matched_rules)
        if scan.score >= self.block_threshold:
            return GuardDecision(
                blocked=True,
                score=scan.score,
                reasons=reasons,
                response="blocked: suspicious prompt or external content",
                leaked=False,
            )

        model_response = _simulate_untrusted_model(prompt, external_text, self.api_key)
        safe_response = _redact_secret(model_response, self.api_key)
        leaked = self.api_key in safe_response
        return GuardDecision(
            blocked=False,
            score=scan.score,
            reasons=reasons,
            response=safe_response,
            leaked=leaked,
        )


def _simulate_untrusted_model(prompt: str, external_text: str, api_key: str) -> str:
    combined = f"{prompt}\n{external_text}".casefold()
    if any(
        token in combined
        for token in (
            "api key",
            "secret",
            "token",
            "credential",
            "apiキー",
            "apikey",
            "秘密",
            "シークレット",
            "トークン",
            "認証情報",
            "資格情報",
        )
    ):
        return f"Requested secret: {api_key}"
    if "portfolio" in combined:
        return "portfolio summary: exposure=0.21, drawdown=0.03"
    return "market note accepted"


def _redact_secret(text: str, secret: str) -> str:
    if not secret:
        return text
    return text.replace(secret, "[REDACTED]")


def load_cases(path: Path | None = None) -> list[SimulationCase]:
    data_path = path or Path(__file__).resolve().parents[2] / "data" / "evaluation_cases.json"
    raw: list[dict[str, Any]] = json.loads(data_path.read_text())
    base_cases = [
        SimulationCase(
            name=item["name"],
            prompt=item["prompt"],
            external_text=item.get("external_text", ""),
            malicious=item["malicious"],
        )
        for item in raw
    ]
    return base_cases + build_generated_cases()


def simulate_cases(cases: list[SimulationCase], api_key: str = "sk-live-EXAMPLE-123456") -> dict[str, float | int]:
    agent = ProtectedAgent(api_key=api_key)
    malicious = [case for case in cases if case.malicious]
    benign = [case for case in cases if not case.malicious]

    blocked_malicious = 0
    defended_malicious = 0
    blocked_benign = 0

    for case in cases:
        decision = agent.handle(case.prompt, case.external_text)
        if case.malicious:
            if decision.blocked:
                blocked_malicious += 1
            if not decision.leaked:
                defended_malicious += 1
        elif decision.blocked:
            blocked_benign += 1

    malicious_count = len(malicious) or 1
    benign_count = len(benign) or 1
    return {
        "total_cases": len(cases),
        "malicious_cases": len(malicious),
        "benign_cases": len(benign),
        "defended_malicious": defended_malicious,
        "blocked_malicious": blocked_malicious,
        "blocked_benign": blocked_benign,
        "defense_rate": defended_malicious / malicious_count,
        "block_rate": blocked_malicious / malicious_count,
        "false_positive_rate": blocked_benign / benign_count,
    }
