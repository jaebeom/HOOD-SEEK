# shared/protocol — 노드 간 통신 규격 단일 소스

Pi 4, Pi Zero, ESP32가 주고받는 UART 프레임·메시지 타입의 **코드 정의 단일 소스**입니다. 세 노드가 각자 상수를 재정의하면 싱크가 깨지므로, 규격 변경은 반드시 이 디렉토리에서만 합니다.

| 파일 | 사용처 |
|---|---|
| `protocol.py` | Pi 4 (`pi4/comm/`), Pi Zero — Python 공용 정의 |
| `protocol.h` | ESP32 (`esp32/`) — C 헤더 |

## 규칙

1. **문서 ↔ 코드 역할 분담**: [docs/communication.md](../../docs/communication.md)는 사람이 읽는 명세, 이 디렉토리는 코드가 참조하는 정의. 둘은 항상 일치해야 한다.
2. 규격 변경 시 `protocol.py`와 `protocol.h`를 **같은 커밋에서 함께** 수정하고, `docs/communication.md`도 갱신한다 (PR 템플릿 체크리스트 항목).
3. TBD 수치(baud rate, SOF 값, CRC 다항식)는 MVP 1 HW bring-up에서 확정 후 채운다.

## 참조 방법

- Python (Pi 4 / Pi Zero): 배포 스크립트에서 `shared/protocol/protocol.py`를 각 노드에 복사하거나 `PYTHONPATH`에 저장소 루트를 추가해 import
- ESP32: PlatformIO `platformio.ini`의 `build_flags`/`lib_extra_dirs`로 이 디렉토리를 include 경로에 추가 (MVP 1에서 확정)
