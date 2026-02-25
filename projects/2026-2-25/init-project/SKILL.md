---
name: init-project
description: 新しいプロジェクトにMANAGEMENTエージェントチームシステムをスキャフォールドする。ROLE定義、ISSUE/TRIALテンプレート、SKILL、テストスイート、ブートストラップISSUEを生成する。"/init-project"で使用。
---

# Init Project

新しいプロジェクトにMANAGEMENTエージェントチームシステムをスキャフォールドする。

## Run This Skill

### 1. 入力を収集する

- `project_name`: プロジェクト名（ハイフンケース、例: `my-awesome-app`）
- `target_dir`: スキャフォールド先のディレクトリパス（例: `~/projects/my-awesome-app`）

### 2. スキャフォールドスクリプトを実行する

```bash
python3 scripts/init_project.py \
  --project-name "<project_name>" \
  --target-dir "<target_dir>"
```

### 3. スキルのインストール（オプション）

スキャフォールド完了後、`--install-skills` を付けると MANAGEMENT/SKILLS/public/ 配下のスキルを ~/.agent/skills/ に自動コピーする。

```bash
python3 scripts/init_project.py \
  --project-name "<project_name>" \
  --target-dir "<target_dir>" \
  --install-skills
```

### 4. 出力を確認する

- ディレクトリ構成が正しいことを確認する
- `cd <target_dir> && python3 -m unittest MANAGEMENT/tests/test_management_workflow_spec.py -v` でテストが通ることを確認する
- CLAUDE.md のプロジェクト名が正しいことを確認する
- ブートストラップISSUEが3件生成されていることを確認する

### 5. ブートストラップISSUEに対応する

生成されたISSUEを順番に処理する:

1. **install-management-skills** - スキルのインストール（`--install-skills` で自動化可能）
2. **configure-project-environment** (WANTED=TRUE) - ユーザーと対話的に環境構築（言語、規約、依存関係、ファイル構造）
3. **identify-recurring-task-skills** (WANTED=TRUE) - ユーザーから定常タスクをヒアリングしSKILL化

## Notes

- 生成されたプロジェクトは `test_management_workflow_spec.py` テストをパスする
- すべてのテンプレートファイルは日本語で生成される
- CLAUDE.md はプロジェクト名をパラメータ化して生成される
- `--timestamp` オプションでテスト用のタイムスタンプを上書きできる
