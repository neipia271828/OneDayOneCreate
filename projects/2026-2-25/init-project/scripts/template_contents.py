"""All template file contents for the init-project scaffolding skill."""

from __future__ import annotations

# ---------------------------------------------------------------------------
# CLAUDE.md  ({project_name} placeholder for the project directory name)
# ---------------------------------------------------------------------------
CLAUDE_MD = """\
# CLAUDE.md

作業手順やこれまでの変更履歴についてはMANAGEMENT/以下を参照すること。

## 0. プロジェクトのファイル構造

```
/{project_name}
    /MANAGEMENT
        /COMPLETES          # 完了済みISSUE/TRIALのアーカイブ
        /ISSUES             # 進行中のISSUE/TRIAL
            ISSUE.md        # ISSUEテンプレート定義
            TRIAL.md        # TRIALテンプレート定義
            WANTED.md       # 優先度管理
            /example
                example-issue-2026-01-01-23-59.md
                /TRIALS
                    example-trial-2026-01-01-23-59.md
        /ROLE               # ロール定義
            WORKFLOW.md
            LEADER.md
            IMPLEMENTER.md
            ANALYST.md
            REVIEWER_VERIFICATER.md
        /SKILLS             # MANAGEMENT用スキル
            /public
                /issue-creator
                /trial-creator
                /spawn-team
        /tests              # ワークフロー仕様テスト
            test_management_workflow_spec.py
        HOWTOCONTRIBUTE.md
        POLICY.md
    AGENTS.md               # Codex-CLI設定
    CLAUDE.md               # Claude Code設定（本ファイル）
```

## 1. roleについて

role = IMPLEMENTER  ならば MANAGEMENT/ROLE/IMPLEMENTER.mdを読みなさい。
role = LEADER       ならば MANAGEMENT/ROLE/LEADER.mdを読みなさい。
role = ANALYST      ならば MANAGEMENT/ROLE/ANALYST.mdを読みなさい。
role = REVIEWER     ならば MANAGEMENT/ROLE/REVIEWER_VERIFICATER.mdを読みなさい。
role = VERIFICATER  ならば MANAGEMENT/ROLE/REVIEWER_VERIFICATER.mdを読みなさい。

最初に起動されたleadagent（Codex/Claude実行時に起動されるメインエージェント、すなわちこのセッションの自分自身）は、自身のroleをLEADERとして認識し、MANAGEMENT/ROLE/LEADER.mdを参照して行動すること。
"""

# ---------------------------------------------------------------------------
# AGENTS.md
# ---------------------------------------------------------------------------
AGENTS_MD = """\
# AGENTS.md

Codex-CLI向けの設定。CLAUDE.mdと共通の指示はCLAUDE.mdを参照すること。
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/ISSUES/ISSUE.md
# ---------------------------------------------------------------------------
ISSUE_TEMPLATE = """\
# ISSUESについて

ユーザーからの依頼について必ずISSUEを立てること。

file name format : summary-issue-2026-01-01-23-59.md
summary部分はissueの内容を完結に示せ。

```markdown
## WHERE
- file path

## ASSIGN
- ex)
- lead
- impl-frontend

## SUMMARY
- 依頼の目的
- 依頼の内容

## CRITERIA
- 達成基準を記述する
- 達成基準は必ず測定可能なものでなければならない

## VERIFICATION
- CRITERIAの判定方法を記述する。

## RELATION
- 関連するTRIAL一覧

## WANTED
TRUE

## FLAG
FLAG =  COMPLETE/INCOMPLETE

```

タスク完了した場合は

```markdown
FLAG = COMPLETE
```

に変更しMANAGEMENT/COMPLETES/にissueを移動する。

RELATIONが5つを超えた場合はWANTEDにissueを追加する。

作成したISSUEは
ISSUES/issue-name/
を作成し、そこに配置しなさい。
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/ISSUES/TRIAL.md
# ---------------------------------------------------------------------------
TRIAL_TEMPLATE = """\
# TRIALについて

file name format : summary-trial-2026-01-01-23-59.md
summary部分はtrialの内容を完結に示せ。

TRIAL作成時は必ず `trial-creator` SKILL を使用すること。

```markdown
# TRIALのファイル名

## 0.PARENT ISSUE/TRIAL
- 親となるISSUEまたはTRIALの名前。

<!-- 実行前に記述する。-->
<!-- PLANNING SECTION-->
## ENVIRONMENT
- 実装上の問題を解決する場合は問題が発生した時の環境を記述する。TODOの場合はスキップ。

## HYPOTHESIS
- 実装上の問題を解決する場合は問題の原因を推定して記述する。TODOの場合はスキップ。

## SOLUTION
- 実装上の問題を解決する方法を記述する。TODOの場合はスキップ。

## PLAN
- 実行に際する計画を立てる。
- SOLUTIONを実行する手順、使用するツールなどを記述する。

## CRITERIA
- 達成基準を記述する
- 達成基準は必ず測定可能なものでなければならない

## VERIFICATION
- CRITERIAの判定基準

<!-- TRIALを実行後に記述する -->
<!-- AFTER OVER SECTION-->
## SUMMARY
- 変更の要約/目的

## DETAIL
- 実装の詳細を記述する。

## CHANGES
- 変更箇所のfile path一覧
- ...

- 簡単な変更の場合
- filename.ex
2 1行ずつ
3 変更を示す


- 大規模な変更の場合
filename.ex
1
2 コードブロックで
3 変更を示す
4


<!-- REVIEWER_VERIFICATERが記述する。 -->
## REVIEW SUMMARY

- レビューの結果をまとめる。

## VERIFICATION SUMMARY

- VERIFICATIONの実行結果をまとめる。

<!-- ANALYSTが記述する。 -->
### DISCOVERY
- 検証によって発見された事実

### REFUTED HYPOTHESES
- 検証の結果、誤りだと判明した仮説・仮定（事前に想定していたが実際には成り立たなかったもの）

### SUPPORTED HYPOTHESES
- 検証の結果、正しいと裏付けられた仮説・仮定（事前の想定が実際に確認されたもの）

<!-- 実行後新たな問題/タスクが発生した場合はTRIALを作成し、ここにRELATIONとして記述する。 -->
## RELATION
- 子TRIAL

## STATUS
YET/PROGRESS/FINISH

```

TRIALを書いたら、親ISSUEのRELATIONに作成したTRIALを追加しなさい。
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/ISSUES/WANTED.md
# ---------------------------------------------------------------------------
WANTED_MD = """\
# WANTED.md

WANTEDは、RELATIONが5つを超えたISSUEを高難度案件として管理するためのリスト。

## 追加タイミング
- ISSUEのRELATIONが5つを超えた場合、LEADERが対象ISSUEをWANTEDへ追加する。

## 記述フォーマット
## issue name

    DIFFICULTY  - I ~ IIIII
    DEADLY      - I ~ IIIII
    URGENCY     - I ~ IIIII

    - summary

## 優先度要素の編集トリガー
- 以下の更新があった場合、LEADERまたはANALYSTがDIFFICULTY/DEADLY/URGENCYを再評価して変更する。
  - 新しい子TRIALが追加され、実装の複雑性が増えた場合
  - 検証で重大な失敗や副作用が発見された場合
  - 期限や外部依存の変更で緊急度が変わった場合

## 見直しタイミング
- 最低でも以下のタイミングで見直しを行う。
  - 週次の進行確認時
  - ISSUEのFLAGがINCOMPLETEのまま2回連続で継続した場合
  - ユーザーから優先度変更の要求があった場合

## 編集ルール
- 更新時はDIFFICULTY/DEADLY/URGENCYの変更理由を1行で追記する。
- 変更後の優先度に応じてIMPLEMENTERへの再割り当てをLEADERが判断する。
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/ROLE/WORKFLOW.md
# ---------------------------------------------------------------------------
WORKFLOW_MD = """\
# WORKFLOW

```mermaid
sequenceDiagram
    participant USER
    participant LEADER
    participant IMPLEMENTER
    participant ANALYST
    participant REVIEWER_VERIFICATER
    participant SKILL
    participant ISSUE_DOC as ISSUE.md
    participant TRIAL_DOC as TRIAL.md
    participant WANTED_DOC as WANTED.md

    USER ->> LEADER : タスク指示
    LEADER ->> ISSUE_DOC : ISSUE起票（WANTED/FLAGを設定）
    LEADER ->> IMPLEMENTER : /spawn ISSUEを作成し渡す

    IMPLEMENTER ->> SKILL : trial-creatorでTRIAL作成/更新（PLANNING）
    IMPLEMENTER ->> TRIAL_DOC : trial-creatorの出力を初期TRIALとして記録
    alt ISSUE.WANTED == TRUE
        IMPLEMENTER ->> ANALYST : /spawn PLANNING作成の依頼
        ANALYST -->> IMPLEMENTER : 推奨方針/根拠/リスク/次アクション
        IMPLEMENTER ->> TRIAL_DOC : 分析結果をPLANへ反映
    else ISSUE.WANTED != TRUE
        IMPLEMENTER ->> TRIAL_DOC : IMPLEMENTERがPLAN作成
    end

    loop ISSUEがCOMPLETEになるまで
        IMPLEMENTER ->> SKILL : タスクの実行
        IMPLEMENTER ->> TRIAL_DOC : AFTER OVER更新（SUMMARY/DETAIL/CHANGES）

        IMPLEMENTER ->> REVIEWER_VERIFICATER : /spawn レビュー/検証の依頼
        REVIEWER_VERIFICATER ->> SKILL : 必要に応じたテスト作成
        REVIEWER_VERIFICATER ->> TRIAL_DOC : REVIEW/VERIFICATIONを記述
        REVIEWER_VERIFICATER ->> ANALYST : /spawn DISCOVERY/REFUTED HYPOTHESES/SUPPORTED HYPOTHESES記述依頼
        ANALYST ->> TRIAL_DOC : D/R/Sを記述

        IMPLEMENTER ->> ISSUE_DOC : RELATIONにTRIALを追記
        alt ISSUE.RELATION > 5
            LEADER ->> WANTED_DOC : ISSUEを追加しDIFFICULTY/DEADLY/URGENCY初期評価
        end

        alt WANTED見直しトリガー発生
            LEADER ->> WANTED_DOC : 優先度を再評価して更新（理由追記）
            ANALYST ->> WANTED_DOC : 再評価の分析支援
        end

        IMPLEMENTER -->> LEADER : 検証完了の通知
        LEADER ->> ISSUE_DOC : CRITERIA達成を判定

        alt ISSUE == COMPLETE
            LEADER ->> ISSUE_DOC : FLAG = COMPLETE
            LEADER ->> ISSUE_DOC : MANAGEMENT/COMPLETESへ移動
            LEADER -->> USER : 完了の通知
        else ISSUE != COMPLETE
            LEADER ->> ISSUE_DOC : FLAG = INCOMPLETEを維持
            LEADER ->> IMPLEMENTER : /spawn 子TRIALの作成依頼
            IMPLEMENTER ->> SKILL : trial-creatorで子TRIAL作成
            IMPLEMENTER ->> TRIAL_DOC : 子TRIALを追記
            LEADER -->> USER : 現状の通知
        end
    end

    Note over LEADER,WANTED_DOC: WANTED見直しタイミング: 週次確認 / INCOMPLETE継続2回 / ユーザー優先度変更要求
    Note over LEADER,REVIEWER_VERIFICATER: 各タスクで担当agentを起動する際、ロール間の新規起動は必ず /spawn を使用する
    Note over IMPLEMENTER,SKILL: TRIAL作成時は必ず trial-creator を使用する
```
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/ROLE/LEADER.md
# ---------------------------------------------------------------------------
LEADER_MD = """\
# LEADER

`MANAGEMENT/ROLE/WORKFLOW.md` に従い、LEADERは進行管理と完了判定を担当する。

1. USERから依頼を受けたらISSUEを作成する。
   ISSUE作成時は必ず `issue-creator` SKILL を使用する。
   `MANAGEMENT/ISSUES/ISSUE.md` の書式に従い、`WANTED` の値を含めて起票する。

2. 作成したISSUEをIMPLEMENTERへ渡す。
   ロール起動は必ず `/spawn` を使用する。
   各タスクの担当agent起動は省略せず、委譲・依頼のたびに `/spawn` で起動する。
   `WANTED = TRUE` のISSUEは、IMPLEMENTERがANALYSTへPLANNING依頼を行う前提で委譲する。

3. IMPLEMENTERから「検証完了」の通知を受けるまで進行を管理する。
   必要に応じて、ユーザーへ中間状況を共有する。

4. 検証完了通知を受けたら、ISSUEのCRITERIA達成状況を判定する。
   達成している場合は `FLAG = COMPLETE` に更新し、ISSUEを `MANAGEMENT/COMPLETES/` へ移動する。
   達成していない場合は `FLAG = INCOMPLETE` のままとする。

5. `ISSUE == COMPLETE` の場合は、ユーザーへ完了を通知する。

6. `ISSUE != COMPLETE` の場合は、IMPLEMENTERへ子TRIAL作成を依頼し、ユーザーへ現状と残作業を通知する。
   子TRIAL依頼時のロール起動も必ず `/spawn` を使用する。
   追加タスクが発生した場合も、担当agentへの新規依頼は毎回 `/spawn` で開始する。
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/ROLE/IMPLEMENTER.md
# ---------------------------------------------------------------------------
IMPLEMENTER_MD = """\
# IMPLEMENTER

`MANAGEMENT/ROLE/WORKFLOW.md` に従い、IMPLEMENTERは実装実行とレビュー/検証依頼の起点を担当する。

1. LEADERからISSUEを受け取ったら内容を確認し、TRIALを作成または更新する。
   TRIALの書式は `MANAGEMENT/ISSUES/TRIAL.md` に従う。
   TRIAL作成時は必ず `trial-creator` SKILL を使用する。

2. ISSUEの `WANTED` を確認して初動を分岐する。
   `WANTED = TRUE` の場合はANALYSTへPLANNING作成を依頼し、TRIALへ反映する。
   `WANTED != TRUE` の場合は、IMPLEMENTERがTRIALのPLANNINGを作成する。
   ANALYSTを起動する場合は必ず `/spawn` を使用する。

3. TRIALのPLANNINGに基づいて実装タスクを実行する。
   必要なスキルを選択して、変更を実施する。

4. 実装後にTRIALのAFTER OVERセクション（SUMMARY/DETAIL/CHANGES）を記述する。

5. TRIALをREVIEWER_VERIFICATERへ渡し、レビューと検証を依頼する。
   REVIEWER_VERIFICATERの起動は必ず `/spawn` を使用する。

6. REVIEWER_VERIFICATERの結果をTRIALへ反映し、LEADERへ「検証完了」を通知する。

7. LEADERから子TRIAL作成依頼を受けた場合は子TRIALを作成し、手順3以降を繰り返す。
   子TRIAL作成時も必ず `trial-creator` SKILL を使用する。
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/ROLE/ANALYST.md
# ---------------------------------------------------------------------------
ANALYST_MD = """\
# ANALYST

`MANAGEMENT/ROLE/WORKFLOW.md` に従い、ANALYSTは「問題の解像度を上げ、意思決定の質を引き上げる」ことを担当する。

## 起動ルール
- ANALYSTは他ロールから依頼されるとき、必ず `/spawn` で起動される。
- 主な起動トリガー:
  - `ISSUE.WANTED == TRUE` のPLANNING依頼
  - REVIEWER_VERIFICATERからの `DISCOVERY/REFUTED HYPOTHESES/SUPPORTED HYPOTHESES` 記述依頼
  - WANTED優先度再評価の分析支援依頼

## 基本方針
- ISSUE/TRIALの定義は参照情報であり、思考の拘束条件ではない。
- 形式を埋めることより、問題の本質を捉えることを優先する。
- 依頼内容をそのまま実行せず、目的・前提・成功条件を再定義してよい。

## 参照する情報源（優先順位）
1. 一次情報（最優先）
   - 現在のISSUE/TRIAL本文
   - `MANAGEMENT/ROLE/*.md` の役割定義
   - 実装対象ファイル、テスト、設定、実行ログ
   - 既存の失敗事例や再現手順

2. 意思決定履歴
   - `MANAGEMENT/COMPLETES/` 配下の過去ISSUE/TRIAL
   - 過去の採用案と不採用案、発生した副作用

3. 外部情報（必要時のみ）
   - 公式ドキュメント、標準仕様、一次ソース
   - 外部情報を使う場合は「出典」と「この案件への適用条件」を明記する。

## 使用ツールと用途
- `rg` / `rg --files`
  - 目的: 影響範囲・関連箇所の高速特定
  - 使用条件: 対象の所在が不明、または参照漏れの可能性があるとき

- `sed` / `cat` / `nl`
  - 目的: 文脈付き読解、行番号付き根拠の抽出
  - 使用条件: 判断根拠を明示したいとき

- `find` / `ls`
  - 目的: 構成把握、履歴・関連ディレクトリ確認
  - 使用条件: 全体像が曖昧な初期調査時

- 差分比較（`diff` など）
  - 目的: 変更前後の振る舞い差分確認
  - 使用条件: 複数案を比較するとき、回帰リスクを洗い出すとき

- テスト関連（プロジェクト既存のテスト実行、必要なら `/codex-test`）
  - 目的: 仮説の反証、再現性確認
  - 使用条件: 仕様解釈ではなく動作事実で判断すべきとき

## 分析フレームワーク
### 問題タイプ別の標準選定
1. 目的が曖昧な問題
- フレームワーク: 5W1H + 成功指標定義
- 選定基準: 「何を達成したら完了か」が曖昧な場合

2. 原因不明の不具合
- フレームワーク: 事象分解（MECE） + 5 Whys
- 選定基準: 再現はするが原因が特定できない場合

3. 複数案の選択が必要
- フレームワーク: 意思決定マトリクス（効果/コスト/リスク/可逆性）
- 選定基準: 2案以上が成立し、優先順位付けが必要な場合

4. 高不確実・探索型タスク
- フレームワーク: 仮説駆動（Hypothesis-Driven） + 小実験設計
- 選定基準: 情報不足が大きく、まず学習コスト最小化が必要な場合

5. ボトルネック改善
- フレームワーク: 制約条件分析（Bottleneck Analysis）
- 選定基準: 一部工程が全体速度を制限している場合

### フレームワーク選定手順
1. 問題を4軸で評価する。
   - 目的明確性（高/低）
   - 原因確実性（高/低）
   - 選択肢数（単一/複数）
   - 時間制約（厳しい/普通）

2. 上記4軸に対応する標準フレームワークを1つ選ぶ。

3. 不確実性が高い場合のみ、補助として仮説駆動を重ねる。

4. フレームワークを使う目的を1文で明示してから分析を開始する。

## 実行時の最小チェックリスト
- 事実と推測を分離して記述したか。
- 根拠は最低2系統以上の情報源から取得したか。
- 代替案を最低1つ以上提示したか。
- 推奨案の採用理由と不採用案の却下理由を明示したか。
- 主要リスクと監視ポイントを明示したか。
- 次アクションを「担当/順序/着手条件」付きで示したか。

## 成果物の最低要素
成果物の形式は自由。ただし以下は必須。
- 推奨方針（何を採るか）
- 根拠（どの情報源に基づくか）
- 主要リスク（何が失敗要因か）
- 次アクション（誰が、何を、どの順で行うか）

## 禁止事項
- ISSUE/TRIALの書式を満たすこと自体を目的化すること。
- 根拠のない断定で方針を固定すること。
- 代替案とリスクを示さずに単一案のみを押し通すこと。
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/ROLE/REVIEWER_VERIFICATER.md
# ---------------------------------------------------------------------------
REVIEWER_VERIFICATER_MD = """\
# REVIEWER_VERIFICATER

`MANAGEMENT/ROLE/WORKFLOW.md` に従い、REVIEWER_VERIFICATERはレビューと検証を一体で担当する。

1. IMPLEMENTERから受け取ったTRIALを確認し、変更内容をレビューする。
   仕様逸脱、実装漏れ、記録不足がないかを確認する。

2. 同じTRIALに対して検証を実行する。
   必要に応じてテストを追加し、変更内容がCRITERIAを満たすかを確認する。

3. テスト作成が必要な場合は `/codex-test` スキルを使用する。
   スキル実行時はTRIALをコンテキストとして渡す。

4. レビュー結果をTRIALの `REVIEW SUMMARY` に記述する。

5. 検証結果をTRIALの `VERIFICATION SUMMARY` に記載する。

6. ANALYSTに `DISCOVERY/REFUTED HYPOTHESES/SUPPORTED HYPOTHESES` の記述を依頼する。
   ANALYSTの起動は必ず `/spawn` を使用する。

7. 実施結果をIMPLEMENTERへ返却し、次アクション（修正継続またはLEADER通知）を判断できる状態にする。
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/SKILLS/public/issue-creator/SKILL.md
# ---------------------------------------------------------------------------
ISSUE_CREATOR_SKILL = """\
---
name: issue-creator
description: Create MANAGEMENT issue folders and issue markdown files that follow MANAGEMENT/ISSUES/ISSUE.md rules. Use when a new user request arrives and an ISSUE must be filed with required sections, filename format, and default flags.
---

# Issue Creator

Create a new ISSUE under `MANAGEMENT/ISSUES/<issue-name>/` using the project's required format.

## Run This Skill

1. Collect required inputs.
- `slug`: short hyphen-case identifier (example: `add-login-page`)
- `where`: one or more target file paths
- `summary_purpose`: purpose of the request
- `summary_detail`: request details
- `criteria`: measurable completion criteria (1+)
- `verification`: how criteria will be judged

2. Run the generator script.
```bash
python3 scripts/create_issue.py \\
  --slug "<slug>" \\
  --where "<file-or-dir>" \\
  --summary-purpose "<purpose>" \\
  --summary-detail "<detail>" \\
  --criteria "<criterion-1>" \\
  --verification "<how-to-verify>"
```

3. If assignment or wanted state is known, set options.
```bash
python3 scripts/create_issue.py \\
  --slug "<slug>" \\
  --where "<file-or-dir>" \\
  --summary-purpose "<purpose>" \\
  --summary-detail "<detail>" \\
  --criteria "<criterion-1>" \\
  --verification "<how-to-verify>" \\
  --assign lead \\
  --assign impl-core \\
  --wanted FALSE
```

4. Verify output path and contents.
- Confirm file path: `MANAGEMENT/ISSUES/<slug>/<slug>-issue-YYYY-MM-DD-HH-MM.md`
- Confirm sections: `WHERE/ASSIGN/SUMMARY/CRITERIA/VERIFICATION/RELATION/WANTED/FLAG`
- Confirm defaults: `RELATION` contains `なし`, `FLAG = INCOMPLETE`

## Notes

- Keep `criteria` measurable.
- Use `--timestamp` only when deterministic reproduction is required.
- The script creates the parent directory and `TRIALS/` directory automatically.
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/SKILLS/public/issue-creator/scripts/create_issue.py
# ---------------------------------------------------------------------------
ISSUE_CREATOR_SCRIPT = '''\
#!/usr/bin/env python3
"""Create ISSUE markdown files for this repository's MANAGEMENT workflow."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a MANAGEMENT issue file with the required template.",
    )
    parser.add_argument("--slug", required=True, help="Issue slug in hyphen-case.")
    parser.add_argument(
        "--where",
        action="append",
        required=True,
        help="Target file/directory path. Repeatable.",
    )
    parser.add_argument(
        "--assign",
        action="append",
        default=[],
        help="Assignment label. Repeatable.",
    )
    parser.add_argument("--summary-purpose", required=True, help="Purpose of request.")
    parser.add_argument("--summary-detail", required=True, help="Detail of request.")
    parser.add_argument(
        "--criteria",
        action="append",
        required=True,
        help="Measurable completion criterion. Repeatable.",
    )
    parser.add_argument(
        "--verification",
        required=True,
        help="How to verify criteria.",
    )
    parser.add_argument(
        "--wanted",
        default="FALSE",
        choices=["TRUE", "FALSE"],
        help="Wanted flag.",
    )
    parser.add_argument(
        "--flag",
        default="INCOMPLETE",
        choices=["COMPLETE", "INCOMPLETE"],
        help="Initial issue flag.",
    )
    parser.add_argument(
        "--timestamp",
        default=None,
        help="Timestamp in YYYY-MM-DD-HH-MM format. Default: current local time.",
    )
    parser.add_argument(
        "--base-dir",
        default="MANAGEMENT/ISSUES",
        help="Base directory where issue folder will be created.",
    )
    return parser.parse_args()


def validate_slug(slug: str) -> None:
    if not slug:
        raise ValueError("slug is required")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    if any(ch not in allowed for ch in slug):
        raise ValueError("slug must be lowercase letters, digits, and hyphens only")


def resolve_timestamp(ts: str | None) -> str:
    if ts is None:
        return datetime.now().strftime("%Y-%m-%d-%H-%M")
    try:
        datetime.strptime(ts, "%Y-%m-%d-%H-%M")
    except ValueError as exc:
        raise ValueError("timestamp must match YYYY-MM-DD-HH-MM") from exc
    return ts


def bullet_lines(values: list[str], fallback: str | None = None) -> str:
    if values:
        return "\\n".join(f"- {item}" for item in values)
    if fallback is not None:
        return f"- {fallback}"
    return "-"


def build_issue_content(args: argparse.Namespace) -> str:
    return "\\n".join(
        [
            "## WHERE",
            bullet_lines(args.where),
            "",
            "## ASSIGN",
            bullet_lines(args.assign, fallback="lead"),
            "",
            "## SUMMARY",
            f"- {args.summary_purpose}",
            f"- {args.summary_detail}",
            "",
            "## CRITERIA",
            bullet_lines(args.criteria),
            "",
            "## VERIFICATION",
            f"- {args.verification}",
            "",
            "## RELATION",
            "- なし",
            "",
            "## WANTED",
            args.wanted,
            "",
            "## FLAG",
            f"FLAG = {args.flag}",
            "",
        ]
    )


def main() -> int:
    args = parse_args()
    validate_slug(args.slug)
    timestamp = resolve_timestamp(args.timestamp)

    issue_dir = Path(args.base_dir) / args.slug
    trials_dir = issue_dir / "TRIALS"
    issue_file = issue_dir / f"{args.slug}-issue-{timestamp}.md"

    issue_dir.mkdir(parents=True, exist_ok=True)
    trials_dir.mkdir(parents=True, exist_ok=True)

    if issue_file.exists():
        raise FileExistsError(f"Issue file already exists: {issue_file}")

    issue_file.write_text(build_issue_content(args), encoding="utf-8")

    print(f"Created issue file: {issue_file}")
    print(f"Created trials dir: {trials_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

# ---------------------------------------------------------------------------
# MANAGEMENT/SKILLS/public/issue-creator/agents/openai.yaml
# ---------------------------------------------------------------------------
ISSUE_CREATOR_YAML = """\
interface:
  display_name: "Issue Creator"
  short_description: "Generate MANAGEMENT issue files reliably."
  default_prompt: "Use $issue-creator to create a new MANAGEMENT issue directory and markdown file from request details."
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/SKILLS/public/trial-creator/SKILL.md
# ---------------------------------------------------------------------------
TRIAL_CREATOR_SKILL = """\
---
name: trial-creator
description: Create MANAGEMENT trial markdown files that follow MANAGEMENT/ISSUES/TRIAL.md rules. Use when IMPLEMENTER creates or updates a TRIAL for a parent ISSUE/TRIAL, including child TRIAL creation loops.
---

# Trial Creator

Create a new TRIAL file under the correct `TRIALS/` directory with the required sections.

## Run This Skill

1. Collect required inputs.
- `slug`: short hyphen-case identifier (example: `fix-render-timeout`)
- `parent`: parent ISSUE or TRIAL markdown path

2. Run the generator script.
```bash
python3 scripts/create_trial.py \\
  --slug "<slug>" \\
  --parent "<path-to-parent-issue-or-trial.md>"
```

3. Optionally control timestamp or parent RELATION update.
```bash
python3 scripts/create_trial.py \\
  --slug "<slug>" \\
  --parent "<path-to-parent-issue-or-trial.md>" \\
  --timestamp "YYYY-MM-DD-HH-MM" \\
  --add-to-parent-relation
```

4. Verify output.
- Confirm file path: `<issue-dir>/TRIALS/<slug>-trial-YYYY-MM-DD-HH-MM.md`
- Confirm parent path is written under `## 0.PARENT ISSUE/TRIAL`
- Confirm default status is `PROGRESS`

## Notes

- Use measurable criteria and verification statements after generation.
- Use `--add-to-parent-relation` to append the new TRIAL path to the parent file's `## RELATION` section.
- Script creates the target `TRIALS/` directory automatically when needed.
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/SKILLS/public/trial-creator/scripts/create_trial.py
# ---------------------------------------------------------------------------
TRIAL_CREATOR_SCRIPT = '''\
#!/usr/bin/env python3
"""Create TRIAL markdown files for this repository's MANAGEMENT workflow."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a MANAGEMENT trial file with the required template.",
    )
    parser.add_argument("--slug", required=True, help="Trial slug in hyphen-case.")
    parser.add_argument(
        "--parent",
        required=True,
        help="Path to parent ISSUE or TRIAL markdown file.",
    )
    parser.add_argument(
        "--timestamp",
        default=None,
        help="Timestamp in YYYY-MM-DD-HH-MM format. Default: current local time.",
    )
    parser.add_argument(
        "--status",
        default="PROGRESS",
        choices=["YET", "PROGRESS", "FINISH"],
        help="Initial TRIAL status.",
    )
    parser.add_argument(
        "--add-to-parent-relation",
        action="store_true",
        help="Append the generated trial path to parent\\'s RELATION section.",
    )
    return parser.parse_args()


def validate_slug(slug: str) -> None:
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    if not slug or any(ch not in allowed for ch in slug):
        raise ValueError("slug must be lowercase letters, digits, and hyphens only")


def resolve_timestamp(ts: str | None) -> str:
    if ts is None:
        return datetime.now().strftime("%Y-%m-%d-%H-%M")
    try:
        datetime.strptime(ts, "%Y-%m-%d-%H-%M")
    except ValueError as exc:
        raise ValueError("timestamp must match YYYY-MM-DD-HH-MM") from exc
    return ts


def detect_trials_dir(parent_file: Path) -> Path:
    if parent_file.parent.name == "TRIALS":
        return parent_file.parent
    return parent_file.parent / "TRIALS"


def build_trial_content(parent_path: str, status: str, filename: str) -> str:
    lines = [
        f"# {filename}",
        "",
        "## 0.PARENT ISSUE/TRIAL",
        f"- {parent_path}",
        "",
        "## ENVIRONMENT",
        "- TODO",
        "",
        "## HYPOTHESIS",
        "- TODO",
        "",
        "## SOLUTION",
        "- TODO",
        "",
        "## PLAN",
        "- TODO",
        "",
        "## CRITERIA",
        "- TODO",
        "",
        "## VERIFICATION",
        "- TODO",
        "",
        "## SUMMARY",
        "- TODO",
        "",
        "## DETAIL",
        "- TODO",
        "",
        "## CHANGES",
        "- TODO",
        "",
        "## REVIEW SUMMARY",
        "- TODO",
        "",
        "## VERIFICATION SUMMARY",
        "- TODO",
        "",
        "### DISCOVERY",
        "- TODO",
        "",
        "### REFUTED HYPOTHESES",
        "- TODO",
        "",
        "### SUPPORTED HYPOTHESES",
        "- TODO",
        "",
        "## RELATION",
        "- なし",
        "",
        "## STATUS",
        status,
        "",
    ]
    return "\\n".join(lines)


def append_relation(parent_file: Path, trial_rel_path: str) -> None:
    text = parent_file.read_text(encoding="utf-8")
    marker = "## RELATION"
    if marker not in text:
        return

    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == marker:
            insert_at = i + 1
            while insert_at < len(lines) and lines[insert_at].strip().startswith("-"):
                insert_at += 1
            lines.insert(insert_at, f"- {trial_rel_path}")
            parent_file.write_text("\\n".join(lines) + "\\n", encoding="utf-8")
            return


def main() -> int:
    args = parse_args()
    validate_slug(args.slug)
    timestamp = resolve_timestamp(args.timestamp)

    parent_file = Path(args.parent)
    if not parent_file.exists():
        raise FileNotFoundError(f"Parent file not found: {parent_file}")

    trials_dir = detect_trials_dir(parent_file)
    trials_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{args.slug}-trial-{timestamp}.md"
    trial_file = trials_dir / filename
    if trial_file.exists():
        raise FileExistsError(f"Trial file already exists: {trial_file}")

    parent_ref = parent_file.as_posix()
    content = build_trial_content(parent_ref, args.status, filename)
    trial_file.write_text(content, encoding="utf-8")

    trial_rel_path = trial_file.as_posix()
    if args.add_to_parent_relation:
        append_relation(parent_file, trial_rel_path)

    print(f"Created trial file: {trial_file}")
    if args.add_to_parent_relation:
        print(f"Updated parent RELATION: {parent_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'''

# ---------------------------------------------------------------------------
# MANAGEMENT/SKILLS/public/trial-creator/agents/openai.yaml
# ---------------------------------------------------------------------------
TRIAL_CREATOR_YAML = """\
interface:
  display_name: "Trial Creator"
  short_description: "Generate MANAGEMENT trial files reliably."
  default_prompt: "Use $trial-creator to create a new MANAGEMENT trial file for a parent issue or trial."
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/SKILLS/public/spawn-team/SKILL.md
# ---------------------------------------------------------------------------
SPAWN_TEAM_SKILL = """\
---
name: spawn-team
description: MANAGEMENT/ROLE/ の定義に基づき、LEADER/IMPLEMENTER/ANALYST/REVIEWER_VERIFICATER のagent teamを起動する。LEADERがISSUEを委譲する前にチームを立ち上げる際に使用する。
---

# Spawn Team

CLAUDE.md と MANAGEMENT/ROLE/*.md に従い、プロジェクトのワークフローロールをagent teamとして起動する。

## 前提

- このスキルを呼び出すエージェントは自身を **LEADER** として認識していること。
- MANAGEMENT/ROLE/WORKFLOW.md に定義されたワークフローに従って運用すること。

## Run This Skill

### 1. チーム名を決定する

引数でチーム名が渡された場合はそれを使用する。渡されなかった場合はユーザーに確認する。

### 2. TeamCreate でチームを作成する

```
TeamCreate:
  team_name: <チーム名>
  description: "MANAGEMENT workflow team"
  agent_type: "leader"
```

### 3. ロール定義を読み込む

以下のファイルを読み込み、各ロールのプロンプトに反映する。

- `MANAGEMENT/ROLE/WORKFLOW.md`
- `MANAGEMENT/ROLE/IMPLEMENTER.md`
- `MANAGEMENT/ROLE/ANALYST.md`
- `MANAGEMENT/ROLE/REVIEWER_VERIFICATER.md`

### 4. 各ロールのagentを起動する

以下の3エージェントを Task ツールで起動する。**全エージェントを並列で起動すること。**

LEADER（自分自身）はチームリーダーとして振る舞う。spawn不要。

#### IMPLEMENTER

```
Task:
  name: "implementer"
  team_name: <チーム名>
  subagent_type: "general-purpose"
  prompt: |
    あなたは IMPLEMENTER ロールです。

    ## 行動規則
    以下のファイルを読み、その内容に厳密に従って行動しなさい。
    - CLAUDE.md
    - MANAGEMENT/ROLE/IMPLEMENTER.md
    - MANAGEMENT/ROLE/WORKFLOW.md

    ## チーム内コミュニケーション
    - LEADERからISSUEを受け取ったら作業を開始する。
    - ANALYST への依頼は SendMessage で "analyst" 宛に送る。
    - REVIEWER_VERIFICATER への依頼は SendMessage で "reviewer-verificater" 宛に送る。
    - 検証完了後は SendMessage で "leader" 宛に通知する。
    - TRIAL作成時は必ず trial-creator スキルを使用する。

    まず上記ファイルを読み、タスクの割り当てを待ちなさい。
```

#### ANALYST

```
Task:
  name: "analyst"
  team_name: <チーム名>
  subagent_type: "general-purpose"
  prompt: |
    あなたは ANALYST ロールです。

    ## 行動規則
    以下のファイルを読み、その内容に厳密に従って行動しなさい。
    - CLAUDE.md
    - MANAGEMENT/ROLE/ANALYST.md
    - MANAGEMENT/ROLE/WORKFLOW.md

    ## チーム内コミュニケーション
    - IMPLEMENTER または REVIEWER_VERIFICATER から依頼を受けて作業を開始する。
    - 分析結果は依頼元に SendMessage で返却する。
    - PLANNING依頼の場合: 推奨方針/根拠/リスク/次アクションを返す。
    - D/R/S記述依頼の場合: DISCOVERY/REFUTED HYPOTHESES/SUPPORTED HYPOTHESES をTRIALに記述する。

    まず上記ファイルを読み、依頼を待ちなさい。
```

#### REVIEWER_VERIFICATER

```
Task:
  name: "reviewer-verificater"
  team_name: <チーム名>
  subagent_type: "general-purpose"
  prompt: |
    あなたは REVIEWER_VERIFICATER ロールです。

    ## 行動規則
    以下のファイルを読み、その内容に厳密に従って行動しなさい。
    - CLAUDE.md
    - MANAGEMENT/ROLE/REVIEWER_VERIFICATER.md
    - MANAGEMENT/ROLE/WORKFLOW.md

    ## チーム内コミュニケーション
    - IMPLEMENTER からレビュー/検証依頼を受けて作業を開始する。
    - ANALYST への D/R/S 記述依頼は SendMessage で "analyst" 宛に送る。
    - レビュー・検証完了後は SendMessage で依頼元の IMPLEMENTER に結果を返す。
    - テスト作成が必要な場合は /codex-test スキルを使用する。

    まず上記ファイルを読み、依頼を待ちなさい。
```

### 5. ユーザーに報告する

起動完了後、以下を報告する。

- チーム名
- 起動したロール一覧（LEADER=自分, IMPLEMENTER, ANALYST, REVIEWER_VERIFICATER）
- 次のアクション: ISSUEを作成してIMPLEMENTERへ委譲する（issue-creator スキル使用）
"""

# ---------------------------------------------------------------------------
# MANAGEMENT/tests/test_management_workflow_spec.py
# ---------------------------------------------------------------------------
TEST_WORKFLOW_SPEC = '''\
"""MANAGEMENT workflow specification tests.

This test module treats markdown docs under MANAGEMENT/ as the source of truth
and verifies whether timing/trigger rules are explicitly defined.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

DOC_PATHS = {
    "issue": REPO_ROOT / "MANAGEMENT/ISSUES/ISSUE.md",
    "trial": REPO_ROOT / "MANAGEMENT/ISSUES/TRIAL.md",
    "wanted": REPO_ROOT / "MANAGEMENT/ISSUES/WANTED.md",
    "workflow": REPO_ROOT / "MANAGEMENT/ROLE/WORKFLOW.md",
    "leader": REPO_ROOT / "MANAGEMENT/ROLE/LEADER.md",
    "implementer": REPO_ROOT / "MANAGEMENT/ROLE/IMPLEMENTER.md",
    "analyst": REPO_ROOT / "MANAGEMENT/ROLE/ANALYST.md",
    "reviewer_verificater": REPO_ROOT / "MANAGEMENT/ROLE/REVIEWER_VERIFICATER.md",
}


class ManagementWorkflowSpecTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.docs = {
            key: path.read_text(encoding="utf-8")
            for key, path in DOC_PATHS.items()
        }

    def assertRegexAny(self, text: str, patterns: list[str], msg: str) -> None:
        for pattern in patterns:
            if re.search(pattern, text, flags=re.MULTILINE):
                return
        self.fail(msg)

    # --- Utilization timing definitions ---
    def test_issue_utilization_timing_is_defined(self) -> None:
        issue = self.docs["issue"]
        workflow = self.docs["workflow"]
        self.assertIn("ユーザーからの依頼について必ずISSUEを立てること", issue)
        self.assertRegexAny(
            workflow,
            patterns=[
                r"LEADER ->> IMPLEMENTER : /spawn ISSUEを作成し渡す",
                r"LEADER ->> IMPLEMENTER : ISSUEを作成し渡す",
            ],
            msg="WORKFLOWでISSUE受け渡しタイミングが定義されていません。",
        )

    def test_trial_utilization_timing_is_defined(self) -> None:
        workflow = self.docs["workflow"]
        implementer = self.docs["implementer"]
        self.assertRegex(
            workflow,
            r"TRIALの作成|子TRIALの作成依頼",
            msg="WORKFLOWでTRIAL利用タイミングが定義されていません。",
        )
        self.assertIn("TRIALを作成または更新", implementer)

    def test_wanted_utilization_timing_is_defined(self) -> None:
        issue = self.docs["issue"]
        workflow = self.docs["workflow"]
        implementer = self.docs["implementer"]
        self.assertRegex(
            issue,
            r"RELATIONが5つを超えた場合はWANTEDにissueを追加する",
            msg="ISSUE.mdにWANTED追加トリガーがありません。",
        )
        self.assertRegexAny(
            workflow,
            patterns=[
                r"ISSUE\\.WANTED\\s*==\\s*TRUE",
                r"else\\s+ISSUE\\s*==\\s*WANTED",
            ],
            msg="WORKFLOWでWANTED分岐が定義されていません。",
        )
        self.assertIn("`WANTED = TRUE` の場合はANALYSTへPLANNING作成を依頼", implementer)

    # --- Edit trigger definitions ---
    def test_issue_edit_triggers_are_defined(self) -> None:
        issue = self.docs["issue"]
        self.assertIn("FLAG = COMPLETE", issue)
        self.assertIn("MANAGEMENT/COMPLETES/にissueを移動", issue)

    def test_trial_edit_triggers_are_defined(self) -> None:
        trial = self.docs["trial"]
        self.assertIn("実行前に記述する", trial)
        self.assertIn("TRIALを実行後に記述する", trial)
        self.assertIn("TRIALを書いたら、親ISSUEのRELATIONに作成したTRIALを追加しなさい", trial)

    def test_incomplete_issue_edit_trigger_is_defined(self) -> None:
        leader = self.docs["leader"]
        self.assertIn("`ISSUE != COMPLETE`", leader)
        self.assertIn("IMPLEMENTERへ子TRIAL作成を依頼", leader)

    def test_wanted_priority_edit_trigger_is_defined(self) -> None:
        """WANTEDの優先度要素をいつ更新するかが明記されているかを検証する。"""

        wanted = self.docs["wanted"]
        # DIFFICULTY/DEADLY/URGENCY の更新タイミングを示す規則が必要。
        self.assertIn("DIFFICULTY", wanted)
        self.assertIn("DEADLY", wanted)
        self.assertIn("URGENCY", wanted)
        self.assertRegexAny(
            wanted,
            patterns=[
                r"(更新|見直し|再評価|変更).*(場合|タイミング)",
                r"(場合|タイミング).*(更新|見直し|再評価|変更)",
            ],
            msg=(
                "WANTED.mdにDIFFICULTY/DEADLY/URGENCYの編集トリガー"
                "（いつ更新するか）が定義されていません。"
            ),
        )

    def test_spawn_is_required_for_role_handoff(self) -> None:
        workflow = self.docs["workflow"]
        leader = self.docs["leader"]
        implementer = self.docs["implementer"]
        reviewer_verificater = self.docs["reviewer_verificater"]
        analyst = self.docs["analyst"]

        self.assertIn("/spawn ISSUEを作成し渡す", workflow)
        self.assertIn("/spawn PLANNING作成の依頼", workflow)
        self.assertIn("/spawn レビュー/検証の依頼", workflow)
        self.assertIn("/spawn DISCOVERY/REFUTED HYPOTHESES/SUPPORTED HYPOTHESES記述依頼", workflow)
        self.assertIn("/spawn 子TRIALの作成依頼", workflow)

        self.assertIn("ロール起動は必ず `/spawn` を使用", leader)
        self.assertIn("ANALYSTを起動する場合は必ず `/spawn` を使用", implementer)
        self.assertIn("REVIEWER_VERIFICATERの起動は必ず `/spawn` を使用", implementer)
        self.assertIn("ANALYSTの起動は必ず `/spawn` を使用", reviewer_verificater)
        self.assertIn("必ず `/spawn` で起動される", analyst)

    def test_trial_dnp_owner_is_analyst(self) -> None:
        trial = self.docs["trial"]
        self.assertIn("<!-- ANALYSTが記述する。 -->", trial)
        self.assertRegexAny(
            trial,
            patterns=[
                r"### DISCOVERY",
                r"### REFUTED HYPOTHESES",
                r"### SUPPORTED HYPOTHESES",
            ],
            msg="TRIAL.mdにD/R/Sセクションが存在しません。",
        )

    def test_trial_creator_skill_is_required(self) -> None:
        workflow = self.docs["workflow"]
        implementer = self.docs["implementer"]
        trial = self.docs["trial"]

        self.assertIn("trial-creatorでTRIAL作成/更新", workflow)
        self.assertIn("trial-creatorで子TRIAL作成", workflow)
        self.assertIn("TRIAL作成時は必ず `trial-creator` SKILL を使用", implementer)
        self.assertIn("子TRIAL作成時も必ず `trial-creator` SKILL を使用", implementer)
        self.assertIn("TRIAL作成時は必ず `trial-creator` SKILL を使用すること。", trial)


if __name__ == "__main__":
    unittest.main(verbosity=2)
'''

# ---------------------------------------------------------------------------
# MANAGEMENT/README.md
# ---------------------------------------------------------------------------
MANAGEMENT_README = """\
# README.md

/spawn-team
でエージェントを起動して下さい。
"""

# ---------------------------------------------------------------------------
# Bootstrap ISSUE A: install-management-skills
# ---------------------------------------------------------------------------
BOOTSTRAP_ISSUE_A = """\
## WHERE
- MANAGEMENT/SKILLS/public/
- ~/.agent/skills/

## ASSIGN
- lead

## SUMMARY
- MANAGEMENTスキルをClaude Code / Codex-CLIに登録する
- MANAGEMENT/SKILLS/public/ 配下の issue-creator, trial-creator, spawn-team を ~/.agent/skills/ にコピーし、エージェントがスキルとして発見・使用できるようにする

## CRITERIA
- ~/.agent/skills/issue-creator/SKILL.md が存在する
- ~/.agent/skills/trial-creator/SKILL.md が存在する
- ~/.agent/skills/spawn-team/SKILL.md が存在する
- 各スキルのscripts/ディレクトリとagents/ディレクトリが正しくコピーされている

## VERIFICATION
- ls -la ~/.agent/skills/issue-creator/ ~/.agent/skills/trial-creator/ ~/.agent/skills/spawn-team/ で存在を確認する

## RELATION
- なし

## WANTED
FALSE

## FLAG
FLAG = INCOMPLETE
"""

# ---------------------------------------------------------------------------
# Bootstrap ISSUE B: configure-project-environment
# ---------------------------------------------------------------------------
BOOTSTRAP_ISSUE_B = """\
## WHERE
- {project_name}/

## ASSIGN
- lead

## SUMMARY
- プロジェクト環境を設定する
- ユーザーと対話的に以下を確認し設定する: 使用言語・フレームワーク、コーディング規約や設計ガイドライン等の合意形成ドキュメント、依存関係のインストール、ファイル構造の整備

## CRITERIA
- 使用言語・フレームワークがドキュメントに記録されている
- コーディング規約や設計ガイドライン等の合意形成ドキュメントが作成されている
- 依存関係がインストールされている（該当する場合）
- プロジェクトのファイル構造がCLAUDE.mdに反映されている

## VERIFICATION
- CLAUDE.mdのファイル構造セクションがプロジェクトの実際の構造と一致することを確認する
- 合意形成ドキュメントに使用技術・規約が明記されていることを目視確認する

## RELATION
- なし

## WANTED
TRUE

## FLAG
FLAG = INCOMPLETE
"""

# ---------------------------------------------------------------------------
# Bootstrap ISSUE C: identify-recurring-task-skills
# ---------------------------------------------------------------------------
BOOTSTRAP_ISSUE_C = """\
## WHERE
- MANAGEMENT/SKILLS/public/
- ~/.agent/skills/

## ASSIGN
- lead

## SUMMARY
- 定常的に繰り返すタスクを特定し、カスタムSKILLとして作成する
- ユーザーと対話的に繰り返しタスクをヒアリングし、SKILLを作成・インストールする

## CRITERIA
- ユーザーが繰り返しタスクを最低1つ特定している（または「なし」と明言している）
- 特定されたタスクごとにSKILLが作成され ~/.agent/skills/ にインストールされている
- 各SKILLのSKILL.mdが正しいYAMLフロントマターを持つ

## VERIFICATION
- 作成されたSKILLが ~/.agent/skills/ に存在することを ls で確認する
- 各SKILL.mdのフロントマターが name と description を持つことを確認する

## RELATION
- なし

## WANTED
TRUE

## FLAG
FLAG = INCOMPLETE
"""

# ---------------------------------------------------------------------------
# Project root README.md
# ---------------------------------------------------------------------------
PROJECT_README = """\
# {project_name}

## セットアップ

### 1. 前提条件
- Claude Code または Codex-CLI がインストールされていること
- Python 3.10以上

### 2. MANAGEMENTスキルのインストール

以下のいずれかの方法でスキルをインストールする:

#### 方法A: 自動インストール（推奨）
エージェントを起動すると、ブートストラップISSUE「install-management-skills」が自動的に処理される。

#### 方法B: 手動インストール
```bash
cp -r MANAGEMENT/SKILLS/public/issue-creator ~/.agent/skills/
cp -r MANAGEMENT/SKILLS/public/trial-creator ~/.agent/skills/
cp -r MANAGEMENT/SKILLS/public/spawn-team ~/.agent/skills/
```

### 3. エージェントの起動
```
/spawn-team
```
でエージェントチームを起動する。

### 4. ブートストラップISSUE
初回起動時、以下のISSUEが用意されている:
1. **install-management-skills** - スキルのインストール
2. **configure-project-environment** - プロジェクト環境の設定（対話的）
3. **identify-recurring-task-skills** - 定常タスクSKILLの特定（対話的）

## ワークフロー概要
MANAGEMENT/ROLE/WORKFLOW.md を参照。
"""
