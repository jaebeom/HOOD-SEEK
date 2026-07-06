#!/usr/bin/env python3
"""shared/protocol/의 protocol.py와 protocol.h 상수 값 일치 여부를 검사한다.

두 파일은 노드 간 UART 규격의 단일 소스로, 같은 커밋에서 함께 수정돼야 한다.
CI와 pre-commit에서 실행되어 싱크가 깨진 채 병합되는 것을 막는다.
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY_FILE = ROOT / "shared" / "protocol" / "protocol.py"
H_FILE = ROOT / "shared" / "protocol" / "protocol.h"


def load_py_constants() -> dict:
    spec = importlib.util.spec_from_file_location("protocol", PY_FILE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return {
        name: value
        for name, value in vars(mod).items()
        if name.isupper() and isinstance(value, int)
    }


def load_h_constants() -> dict:
    text = H_FILE.read_text(encoding="utf-8")
    consts = {}
    # #define NAME 0xNN | NN
    for m in re.finditer(r"#define\s+(\w+)\s+(0x[0-9A-Fa-f]+|\d+)", text):
        consts[m.group(1)] = int(m.group(2), 0)
    # enum 멤버: typedef enum { NAME = N, ... } 본문에서 추출 (한 줄/여러 줄 모두)
    for body in re.findall(r"typedef\s+enum\s*\{(.*?)\}", text, re.S):
        for m in re.finditer(r"(\w+)\s*=\s*(\d+)", body):
            consts[m.group(1)] = int(m.group(2))
    return consts


def main() -> int:
    py_consts = load_py_constants()
    h_consts = load_h_constants()
    errors = []

    for name, py_val in sorted(py_consts.items()):
        # C 헤더는 매크로 충돌 방지를 위해 일부 상수에 PROTO_ 접두사를 사용
        h_val = h_consts.get(name, h_consts.get(f"PROTO_{name}"))
        if h_val is None:
            errors.append(f"{name}: protocol.h에 정의 없음")
        elif h_val != py_val:
            errors.append(f"{name}: protocol.py={py_val:#x}, protocol.h={h_val:#x} 불일치")

    if errors:
        print("[protocol-sync] 규격 불일치 발견 — 두 파일을 같은 커밋에서 함께 수정하세요:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"[protocol-sync] OK — {len(py_consts)}개 상수 일치")
    return 0


if __name__ == "__main__":
    sys.exit(main())
