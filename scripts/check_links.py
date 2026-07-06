#!/usr/bin/env python3
"""저장소 내 마크다운 문서의 상대 링크가 실제 파일·디렉토리를 가리키는지 검사한다.

외부 URL(http/https/mailto)은 건드리지 않는다 — 문서 이동·이름 변경으로
깨진 내부 링크만 잡는다. CI와 pre-commit에서 실행된다.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK_RE = re.compile(r"\]\(([^)]+)\)")


def main() -> int:
    errors = []
    checked = 0
    for md in sorted(ROOT.rglob("*.md")):
        if ".git" in md.parts:
            continue
        for m in LINK_RE.finditer(md.read_text(encoding="utf-8")):
            target = m.group(1).split("#")[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            checked += 1
            if not (md.parent / target).exists():
                errors.append(f"{md.relative_to(ROOT)}: {target}")

    if errors:
        print("[docs-links] 깨진 상대 링크 발견:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"[docs-links] OK — 상대 링크 {checked}건 모두 유효")
    return 0


if __name__ == "__main__":
    sys.exit(main())
