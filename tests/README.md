# tests — 테스트 시나리오

[docs/test-scenarios.md](../docs/test-scenarios.md)의 5대 시나리오를 기준으로 구성합니다.

| ID | 시나리오 | 관련 모듈 |
|---|---|---|
| TS-1 | PM 기반 자동 후드 풍량 조절 | `pizero/sps30`, `pi4/smoke` |
| TS-2 | 사용자 부재 및 과열 위험 판단 | `pi4/vision`, `pi4/thermal`, `pi4/fusion` |
| TS-3 | 복합 위험 상황 End-to-End 제어 | 전체 |
| TS-4 | 비조리 중 반려동물 접근 제한 | `pi4/vision`, `esp32` |
| TS-5 | 음성 명령 및 안전 우선순위 검증 | `pi4/voice`, `pi4/fusion` |

단위 테스트는 각 모듈 옆에, 시나리오(통합) 테스트는 여기에 둡니다. 센서 로그 재생(`scripts/replay_log.py`) 기반으로 실기기 없이도 판단 로직을 검증할 수 있게 구성할 예정입니다.
