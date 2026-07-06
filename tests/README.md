# tests — 테스트 시나리오

[docs/test-scenarios.md](../docs/test-scenarios.md)의 5대 시나리오를 기준으로 구성합니다.

| ID | 시나리오 | 관련 모듈 |
|---|---|---|
| TS-1 | PM 기반 자동 후드 풍량 조절 | `pizero/sps30`, `pi4/smoke` |
| TS-2 | 사용자 부재 및 과열 위험 판단 | `pi4/vision`, `pi4/thermal`, `pi4/fusion` |
| TS-3 | 복합 위험 상황 End-to-End 제어 | 전체 |
| TS-4 | 비조리 중 반려동물 접근 제한 | `pi4/vision`, `esp32` |
| TS-5 | 음성 명령 및 안전 우선순위 검증 | `pi4/voice`, `pi4/fusion` |

## 구조

| 디렉토리 | 내용 |
|---|---|
| `unit/pi4/` | 판단 모듈 단위 테스트 (SmokeScore·HeatScore 계산, 상태기계 전이, 히스테리시스) |
| `unit/pizero/` | 게이트웨이 단위 테스트 (SPS30 파싱, watchdog timeout 판정) |
| `integration/` | TS-1 ~ TS-5 시나리오 매핑 통합 테스트 |

ESP32 펌웨어 단위 테스트(PWM 제어, 명령 거부, fail-safe 진입)는 PlatformIO 관례에 따라 [`esp32/test/`](../esp32/test/)에 둡니다.

통합 테스트는 센서 로그 재생(`scripts/replay_log.py`) 기반으로 실기기 없이도 판단 로직을 검증할 수 있게 구성할 예정입니다.
