# pi4 — 고수준 판단 노드 (Raspberry Pi 4)

영상·열화상·음성·PM 데이터를 결합해 위험도를 판단하고 ESP32로 제어 명령을 전달하는 메인 노드입니다. 모든 판단은 네트워크 없이 온디바이스로 동작합니다.

## 모듈 구성

| 디렉토리 | 담당 기능 | 방식 |
|---|---|---|
| `smoke/` | SmokeScore 계산 | PM 기준선 대비 상승률·지속시간·이동평균 + 히스테리시스 (규칙 기반, ≤10ms) |
| `thermal/` | HeatScore 계산 | MLX90640 최고온도·상승률·핫스폿 면적 (규칙 기반, ≤50ms) |
| `vision/` | 사용자 존재 판단 + 반려동물·물체 ROI 탐지 | OpenCV + 경량 객체 탐지 (YOLOv5n/v8n/TFLite 검토) |
| `voice/` | 제한 명령어 음성 인식 | Vosk / Whisper.cpp tiny / KWS 중 안정성 높은 방식 선택 |
| `fusion/` | 위험도 상태기계 | SmokeScore + AbsentConfirmed + HeatScore → LOW/MEDIUM/HIGH/CRITICAL (≤10ms) |
| `comm/` | Pi Zero·ESP32 통신 | UART/Serial 우선, heartbeat + timeout |
| `ui/` | 상태 표시·경고 UI, 로그 재생 뷰 | 확장 Iteration 단계에서 구현 (docs/roadmap.md 12~13번) |

판단 임계값은 코드에 하드코딩하지 않고 [config/](../config/)에서 관리합니다.

상태기계 설계는 [docs/risk-state-machine.md](../docs/risk-state-machine.md), 통신 프로토콜은 [docs/communication.md](../docs/communication.md) 참고.

## 개발 환경

- Python 3.9+ (Raspberry Pi OS)
- 의존성: `requirements.txt` (OpenCV, numpy, pyserial 등 — MVP 진행하며 확정)
