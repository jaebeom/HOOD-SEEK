# esp32 — 액추에이터 MCU (ESP32)

Pi 4가 전달한 위험도와 제어 명령을 받아 최종 동작을 집행하는 안전 계층입니다. 판단 노드가 다운되어도 자체 fail-safe로 안전 상태를 유지합니다.

## 담당 기능

- 후드 팬 PWM 제어 (정지/약풍/중풍/강풍)
- 인덕션 차단 시뮬레이션
- 잠금 LED, 부저 경고
- 명령 timeout·fail-safe 조건 자체 확인
- 위험 상태(HIGH 이상) 또는 잠금 상태에서 인덕션 ON / 화력 증가 명령 **거부**

## 구조

| 디렉토리 | 내용 |
|---|---|
| `src/` | 펌웨어 소스 (Arduino / PlatformIO — MVP 1에서 확정) |
| `include/` | 공용 헤더 (명령 프로토콜 정의 등) |

Pi 4 ↔ ESP32 UART 메시지 포맷은 [docs/communication.md](../docs/communication.md) 참고.
