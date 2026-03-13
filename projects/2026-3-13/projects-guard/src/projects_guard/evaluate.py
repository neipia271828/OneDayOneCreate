from __future__ import annotations

import json

from .guard import load_cases, simulate_cases


def main() -> None:
    cases = load_cases()
    metrics = simulate_cases(cases)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
