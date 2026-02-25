#!/usr/bin/env python3
"""Scaffold the MANAGEMENT agent team system into a new project."""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path

from template_contents import (
    AGENTS_MD,
    ANALYST_MD,
    BOOTSTRAP_ISSUE_A,
    BOOTSTRAP_ISSUE_B,
    BOOTSTRAP_ISSUE_C,
    CLAUDE_MD,
    IMPLEMENTER_MD,
    ISSUE_CREATOR_SCRIPT,
    ISSUE_CREATOR_SKILL,
    ISSUE_CREATOR_YAML,
    ISSUE_TEMPLATE,
    LEADER_MD,
    MANAGEMENT_README,
    PROJECT_README,
    REVIEWER_VERIFICATER_MD,
    SPAWN_TEAM_SKILL,
    TEST_WORKFLOW_SPEC,
    TRIAL_CREATOR_SCRIPT,
    TRIAL_CREATOR_SKILL,
    TRIAL_CREATOR_YAML,
    TRIAL_TEMPLATE,
    WANTED_MD,
    WORKFLOW_MD,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold the MANAGEMENT agent team system into a new project.",
    )
    parser.add_argument(
        "--project-name",
        required=True,
        help="Project name in hyphen-case (e.g. my-awesome-app).",
    )
    parser.add_argument(
        "--target-dir",
        required=True,
        help="Directory to scaffold into.",
    )
    parser.add_argument(
        "--install-skills",
        action="store_true",
        help="Also copy skills to ~/.agent/skills/ for global discovery.",
    )
    parser.add_argument(
        "--timestamp",
        default=None,
        help="Timestamp override in YYYY-MM-DD-HH-MM format (for testing).",
    )
    return parser.parse_args()


def validate_project_name(name: str) -> None:
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789-")
    if not name or any(ch not in allowed for ch in name):
        raise ValueError(
            "project-name must be lowercase letters, digits, and hyphens only"
        )


def resolve_timestamp(ts: str | None) -> str:
    if ts is None:
        return datetime.now().strftime("%Y-%m-%d-%H-%M")
    try:
        datetime.strptime(ts, "%Y-%m-%d-%H-%M")
    except ValueError as exc:
        raise ValueError("timestamp must match YYYY-MM-DD-HH-MM") from exc
    return ts


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  Created: {path}")


def create_directory_structure(base: Path) -> None:
    dirs = [
        base / "MANAGEMENT" / "COMPLETES",
        base / "MANAGEMENT" / "ISSUES" / "example" / "TRIALS",
        base / "MANAGEMENT" / "ROLE",
        base / "MANAGEMENT" / "SKILLS" / "public" / "issue-creator" / "scripts",
        base / "MANAGEMENT" / "SKILLS" / "public" / "issue-creator" / "agents",
        base / "MANAGEMENT" / "SKILLS" / "public" / "trial-creator" / "scripts",
        base / "MANAGEMENT" / "SKILLS" / "public" / "trial-creator" / "agents",
        base / "MANAGEMENT" / "SKILLS" / "public" / "spawn-team",
        base / "MANAGEMENT" / "tests",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def write_templates(base: Path, project_name: str) -> None:
    # Root files
    write_file(
        base / "CLAUDE.md",
        CLAUDE_MD.format(project_name=project_name),
    )
    write_file(base / "AGENTS.md", AGENTS_MD)
    write_file(
        base / "README.md",
        PROJECT_README.format(project_name=project_name),
    )

    m = base / "MANAGEMENT"

    # ISSUES templates
    write_file(m / "ISSUES" / "ISSUE.md", ISSUE_TEMPLATE)
    write_file(m / "ISSUES" / "TRIAL.md", TRIAL_TEMPLATE)
    write_file(m / "ISSUES" / "WANTED.md", WANTED_MD)

    # Example placeholders (empty files)
    write_file(m / "ISSUES" / "example" / "example-issue-2026-01-01-23-59.md", "")
    write_file(
        m / "ISSUES" / "example" / "TRIALS" / "example-trial-2026-01-01-23-59.md",
        "",
    )

    # ROLE definitions
    write_file(m / "ROLE" / "WORKFLOW.md", WORKFLOW_MD)
    write_file(m / "ROLE" / "LEADER.md", LEADER_MD)
    write_file(m / "ROLE" / "IMPLEMENTER.md", IMPLEMENTER_MD)
    write_file(m / "ROLE" / "ANALYST.md", ANALYST_MD)
    write_file(m / "ROLE" / "REVIEWER_VERIFICATER.md", REVIEWER_VERIFICATER_MD)

    # SKILLS
    sp = m / "SKILLS" / "public"
    write_file(sp / "issue-creator" / "SKILL.md", ISSUE_CREATOR_SKILL)
    write_file(sp / "issue-creator" / "scripts" / "create_issue.py", ISSUE_CREATOR_SCRIPT)
    write_file(sp / "issue-creator" / "agents" / "openai.yaml", ISSUE_CREATOR_YAML)
    write_file(sp / "trial-creator" / "SKILL.md", TRIAL_CREATOR_SKILL)
    write_file(sp / "trial-creator" / "scripts" / "create_trial.py", TRIAL_CREATOR_SCRIPT)
    write_file(sp / "trial-creator" / "agents" / "openai.yaml", TRIAL_CREATOR_YAML)
    write_file(sp / "spawn-team" / "SKILL.md", SPAWN_TEAM_SKILL)

    # Tests
    write_file(m / "tests" / "test_management_workflow_spec.py", TEST_WORKFLOW_SPEC)

    # MANAGEMENT README
    write_file(m / "README.md", MANAGEMENT_README)


def generate_bootstrap_issues(
    base: Path, project_name: str, timestamp: str
) -> None:
    issues_dir = base / "MANAGEMENT" / "ISSUES"

    issue_specs = [
        ("install-management-skills", BOOTSTRAP_ISSUE_A, False),
        ("configure-project-environment", BOOTSTRAP_ISSUE_B, True),
        ("identify-recurring-task-skills", BOOTSTRAP_ISSUE_C, False),
    ]

    for slug, content, needs_format in issue_specs:
        issue_dir = issues_dir / slug
        trials_dir = issue_dir / "TRIALS"
        trials_dir.mkdir(parents=True, exist_ok=True)

        filename = f"{slug}-issue-{timestamp}.md"
        body = content.format(project_name=project_name) if needs_format else content
        write_file(issue_dir / filename, body)


def install_skills(base: Path) -> None:
    skills_src = base / "MANAGEMENT" / "SKILLS" / "public"
    skills_dst = Path.home() / ".agent" / "skills"
    skills_dst.mkdir(parents=True, exist_ok=True)

    for skill_dir in skills_src.iterdir():
        if not skill_dir.is_dir():
            continue
        dst = skills_dst / skill_dir.name
        if dst.exists():
            print(f"  Skipped (already exists): {dst}")
            continue
        shutil.copytree(skill_dir, dst)
        print(f"  Installed: {dst}")


def main() -> int:
    args = parse_args()
    validate_project_name(args.project_name)
    timestamp = resolve_timestamp(args.timestamp)

    base = Path(args.target_dir).resolve()
    if base.exists() and any(base.iterdir()):
        print(f"Warning: target directory is not empty: {base}")

    print(f"Scaffolding MANAGEMENT system into: {base}")
    print(f"Project name: {args.project_name}")
    print()

    print("[1/4] Creating directory structure...")
    create_directory_structure(base)

    print("[2/4] Writing template files...")
    write_templates(base, args.project_name)

    print("[3/4] Generating bootstrap ISSUEs...")
    generate_bootstrap_issues(base, args.project_name, timestamp)

    if args.install_skills:
        print("[4/4] Installing skills to ~/.agent/skills/...")
        install_skills(base)
    else:
        print("[4/4] Skipping skill installation (use --install-skills to enable)")

    print()
    print("Done! Next steps:")
    print(f"  cd {base}")
    print("  # Review CLAUDE.md and AGENTS.md")
    print("  # Process bootstrap ISSUEs in MANAGEMENT/ISSUES/")
    print("  # Run: /spawn-team to start the agent team")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
