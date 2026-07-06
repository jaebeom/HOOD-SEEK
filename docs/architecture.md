# 시스템 아키텍처

HOOD&SEEK는 **판단(Pi 4)**, **수집·감시(Pi Zero)**, **집행(ESP32)** 을 물리적으로 분리한 3-노드 협력형 구조입니다. 판단 노드가 다운되더라도 나머지 노드가 fail-safe 상태로 전환되어 안전을 보장합니다.

## 노드별 역할

### Raspberry Pi 4 — 고수준 판단 노드

영상·열화상·음성·PM 데이터를 결합하여 위험도를 판단하고 ESP32로 제어 명령을 전달합니다.

| 모듈 | 입력 | 출력 | 방식 | 목표 지연 |
|---|---|---|---|---|
| `smoke/` | SPS30 PM1.0/2.5/4/10 (Pi Zero 경유) | SmokeScore | 기준선 대비 상승률 + 지속시간 + 이동평균 + 히스테리시스 (AI 미사용) | ≤ 10ms |
| `thermal/` | MLX90640 열화상 (I2C) | HeatScore | 최고온도·온도 상승률·핫스폿 면적 계산 (AI 미사용) | ≤ 50ms |
| `vision/` (존재) | V4L2 카메라 | 사용자 존재 여부 → AbsentConfirmed | OpenCV 전처리 + 경량 객체 탐지 (5~15MB) | 100~300ms |
| `vision/` (접근) | V4L2 카메라 ROI | 위험 구역 침입 여부 | YOLOv5n/YOLOv8n/TFLite (5~12MB) + ROI 규칙 | 150~500ms |
| `voice/` | ReSpeaker Lite USB 2-Mic | 제한 명령어 | Vosk / Whisper.cpp tiny / KWS 중 택1 (오프라인) | 0.5~2s |
| `fusion/` | SmokeScore, HeatScore, AbsentConfirmed, 접근 이벤트, 음성 명령 | 위험 단계 + 제어 명령 | 규칙 기반 상태기계 | ≤ 10ms |

### Raspberry Pi Zero — 센서 게이트웨이

- 후드 흡입부 근처의 **SPS30 데이터를 안정적으로 수집·로그화**하여 Pi 4로 전달
- **Pi 4의 동작 상태를 감시**(watchdog)하고, Pi 4가 멈추거나 통신이 끊기면 fail-safe 전환을 트리거

### ESP32 — 액추에이터 MCU

- Pi 4가 전달한 위험도·제어 명령을 받아 **후드 팬 PWM, 인덕션 차단 시뮬레이션, 잠금 LED, 부저**를 제어
- 명령 **timeout과 fail-safe 조건**을 자체 확인 — 판단 노드를 신뢰하되 최종 안전 판단은 MCU가 수행
- 위험 상태에서는 인덕션 ON 또는 화력 증가 명령을 **거부**

## 설계 원칙

1. **판단과 집행의 분리** — 고수준 판단(Pi 4)이 실패해도 집행 계층(ESP32)이 독립적으로 안전 상태를 유지한다.
2. **설명 가능한 판단** — 딥러닝 단독 판단이 아닌 센서 융합 기반 규칙 상태기계로 구현하여 검증 가능성을 확보한다.
3. **온디바이스 우선** — 모든 추론·판단은 네트워크 없이 오프라인으로 동작한다.
4. **절대값이 아닌 추세** — PM·온도의 순간값이 아니라 기준선 대비 상승률과 지속 시간으로 판단하여 수증기·기름 입자에 의한 오탐을 줄인다.
5. **안전 우선순위** — 위험 단계가 HIGH 이상이면 사용자 음성 명령보다 안전 제어가 우선한다.

## 데이터 흐름

```
SPS30 ──(I2C/UART)──> Pi Zero ──(Serial/UART)──> Pi 4 smoke/  ─┐
MLX90640 ──(I2C, 짧은 배선)─────────────────────> Pi 4 thermal/ ─┤
V4L2 카메라 ──(USB)─────────────────────────────> Pi 4 vision/  ─┼─> fusion/ ──(UART)──> ESP32 ──> 팬 PWM / 차단 / LED / 부저
ReSpeaker Lite ──(USB)──────────────────────────> Pi 4 voice/   ─┘
```

핵심 통신은 Wi-Fi가 아닌 **UART/Serial을 우선** 사용하고, heartbeat와 timeout을 적용합니다. 상세 프로토콜은 [communication.md](communication.md) 참고.
