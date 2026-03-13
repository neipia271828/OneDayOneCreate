from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


@dataclass(frozen=True)
class RuleMatch:
    name: str
    score: int
    pattern: str


@dataclass(frozen=True)
class ScanResult:
    score: int
    matched_rules: tuple[RuleMatch, ...]

    @property
    def should_block(self) -> bool:
        return self.score >= 6


class PromptScanner:
    def __init__(self) -> None:
        self._rules: tuple[RuleMatch, ...] = (
            RuleMatch("instruction_override", 3, r"ignore (all|any|previous|prior) (rules|instructions)"),
            RuleMatch("instruction_override_ja", 3, r"(これまで|以前|直前)の(指示|命令|ルール)は無視"),
            RuleMatch("secret_request", 4, r"(show|reveal|print|dump|return|expose).{0,24}(api[_ -]?key|secret|token|credential)"),
            RuleMatch("secret_request_ja", 4, r"((表示|出力|教えて|返して|見せて|公開).{0,24}(apiキー|apikey|秘密|シークレット|トークン|認証情報|資格情報))|((apiキー|apikey|秘密|シークレット|トークン|認証情報|資格情報).{0,24}(表示|出力|教えて|返して|見せて|公開))"),
            RuleMatch("exfiltration", 4, r"(send|post|upload|transmit|forward|leak|exfiltrat\w*).{0,24}(api[_ -]?key|secret|token|credential)"),
            RuleMatch("exfiltration_ja", 4, r"(送信|アップロード|転送|流出|漏洩|投稿).{0,24}(apiキー|apikey|秘密|シークレット|トークン|認証情報|資格情報)"),
            RuleMatch("tool_subversion", 3, r"(run|execute|call).{0,24}(shell|bash|command|curl|wget)"),
            RuleMatch("tool_subversion_ja", 3, r"(実行|呼び出し).{0,24}(shell|bash|コマンド|curl|wget)"),
            RuleMatch("system_prompt", 3, r"(system prompt|hidden prompt|developer message)"),
            RuleMatch("system_prompt_ja", 3, r"(システムプロンプト|隠しプロンプト|開発者メッセージ|内部指示)"),
            RuleMatch("role_play_escape", 2, r"(pretend|simulate|roleplay).{0,24}(developer|admin|root)"),
            RuleMatch("role_play_escape_ja", 2, r"(ふりをして|として振る舞い|ロールプレイ).{0,24}(管理者|admin|root|開発者)"),
            RuleMatch("encoding_evasion", 2, r"(base64|rot13|hex|unicode).{0,24}(decode|encoded?)"),
            RuleMatch("encoding_evasion_ja", 2, r"(base64|rot13|hex|unicode).{0,24}(復号|デコード|エンコード)"),
            RuleMatch("do_not_tell", 2, r"(do not tell|don't tell|without telling|silently)"),
            RuleMatch("do_not_tell_ja", 2, r"(黙って|知らせずに|内緒で|ユーザーには知らせずに)"),
            RuleMatch("credential_target", 3, r"(env|environment variable|vault|config).{0,24}(api[_ -]?key|secret|token)"),
            RuleMatch("credential_target_ja", 3, r"(env|環境変数|vault|設定ファイル|config).{0,24}(apiキー|apikey|秘密|シークレット|トークン)"),
            RuleMatch("jailbreak", 3, r"(bypass|override|disable).{0,24}(guard|filter|policy|safeguard|safety)"),
            RuleMatch("jailbreak_ja", 3, r"(無効化|迂回|解除).{0,24}(guard|フィルタ|ポリシー|安全機構|ガード)"),
        )

    def scan(self, *texts: str) -> ScanResult:
        hits: list[RuleMatch] = []
        score = 0
        for text in texts:
            normalized = normalize_text(text)
            for rule in self._rules:
                if re.search(rule.pattern, normalized):
                    hits.append(rule)
                    score += rule.score
        # Strong signal if multiple independent secret-targeting patterns co-occur.
        unique_names = {hit.name for hit in hits}
        if ({"instruction_override", "secret_request"} <= unique_names) or (
            {"instruction_override_ja", "secret_request_ja"} <= unique_names
        ):
            score += 2
        if (
            ({"exfiltration", "credential_target"} & unique_names and "secret_request" in unique_names)
            or ({"exfiltration_ja", "credential_target_ja"} & unique_names and "secret_request_ja" in unique_names)
        ):
            score += 2
        deduped_hits = tuple(_dedupe_preserve_order(hits))
        return ScanResult(score=score, matched_rules=deduped_hits)


def normalize_text(text: str) -> str:
    lowered = text.casefold()
    collapsed = re.sub(r"\s+", " ", lowered)
    return collapsed.strip()


def _dedupe_preserve_order(items: Iterable[RuleMatch]) -> list[RuleMatch]:
    seen: set[str] = set()
    result: list[RuleMatch] = []
    for item in items:
        if item.name in seen:
            continue
        seen.add(item.name)
        result.append(item)
    return result
