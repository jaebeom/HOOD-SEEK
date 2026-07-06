# 디바이스 간 통신

## 원칙

- **핵심 통신은 UART/Serial 우선** — Wi-Fi 지연, 포트 충돌 등의 불안정 요인을 회피
- 모든 링크에 **heartbeat + timeout** 적용
- 통신 단절 시 각 노드가 **fail-safe 상태로 자율 전환**

## 통신 링크

| 링크 | 매체 | 방향 | 내용 |
|---|---|---|---|
| SPS30 ↔ Pi Zero | I2C/UART | 센서 → 게이트웨이 | PM1.0, PM2.5, PM4, PM10 원시 데이터 |
| Pi Zero ↔ Pi 4 | Serial/UART | 양방향 | PM 데이터 전달 + Pi 4 heartbeat 감시 |
| MLX90640 ↔ Pi 4 | I2C (짧은 배선) | 센서 → Pi 4 | 열화상 프레임 |
| V4L2 카메라 ↔ Pi 4 | USB | 센서 → Pi 4 | 영상 스트림 |
| ReSpeaker Lite ↔ Pi 4 | USB | 센서 → Pi 4 | 2-Mic 오디오 |
| Pi 4 ↔ ESP32 | UART | 양방향 | 위험도·제어 명령 ↓ / ACK·상태 ↑ |

## 프레임 구조 (모든 UART 링크 공통 골격)

Pi Zero ↔ Pi 4, Pi 4 ↔ ESP32의 시리얼 메시지는 아래 공통 프레임을 사용합니다.

> **코드 정의 단일 소스는 [`shared/protocol/`](../shared/protocol/)** (`protocol.py` + `protocol.h`)입니다. 이 문서는 사람용 명세이며, 규격 변경 시 둘을 같은 커밋에서 함께 갱신합니다.

| 필드 | 크기 | 설명 |
|---|---|---|
| `SOF` | 1B | 프레임 시작 마커 (값 TBD, 예: `0xAA`) |
| `TYPE` | 1B | 메시지 타입 (아래 표) |
| `SEQ` | 1B | 시퀀스 번호 — 중복/유실 감지, 응답 매칭 |
| `LEN` | 1B | Payload 길이 |
| `PAYLOAD` | LEN | 메시지별 데이터 |
| `CRC` | 2B | CRC-16 무결성 검증 (다항식 TBD) |

> **TBD 항목**(baud rate, SOF 값, CRC 다항식, Payload 바이트 오프셋)은 MVP 1(수동 제어 루프) HW bring-up에서 실측 후 확정하고 이 문서를 갱신한다.

## 메시지 타입

### Pi Zero → Pi 4

| TYPE | 이름 | Payload |
|---|---|---|
| `0x01` | `PM_DATA` | PM1.0 / PM2.5 / PM4 / PM10 측정값 + 측정 시각 |
| `0x02` | `GW_STATUS` | Pi Zero 상태, SPS30 오류 플래그 |

### Pi 4 → Pi Zero

| TYPE | 이름 | Payload |
|---|---|---|
| `0x10` | `HEARTBEAT` | Pi 4 상태 요약 (watchdog 감시 대상) |

### Pi 4 → ESP32

| TYPE | 이름 | Payload |
|---|---|---|
| `0x20` | `CONTROL` | 아래 제어 필드 |
| `0x21` | `HEARTBEAT` | (없음) — timeout 갱신용 |

`CONTROL` Payload 필드:

| 필드 | 설명 |
|---|---|
| `risk_level` | LOW / MEDIUM / HIGH / CRITICAL |
| `hood_level` | 후드 풍량 단계 (0=정지, 1=약풍, 2=중풍, 3=강풍) |
| `induction_cmd` | 인덕션 명령 (NORMAL / LIMIT / CUTOFF / LOCK) |
| `alert` | 부저·LED 경고 플래그 |

### ESP32 → Pi 4

| TYPE | 이름 | Payload |
|---|---|---|
| `0x30` | `ACK_STATUS` | 수신 `SEQ` 에코 + 현재 액추에이터 상태 + 자체 fail-safe 상태 |

ESP32는 위험 상태(HIGH 이상) 또는 잠금 상태에서 `CONTROL`의 인덕션 ON/화력 증가에 해당하는 명령을 거부하고, 거부 사실을 `ACK_STATUS`에 반영합니다.

## Heartbeat / Timeout / Fail-safe

```
Pi 4 ──(주기적 heartbeat)──> Pi Zero, ESP32
```

- **Pi 4 정지 또는 통신 단절 감지 시:**
  - Pi Zero: watchdog이 단절을 기록하고 fail-safe 전환 신호
  - ESP32: 마지막 명령 수신 후 timeout 초과 시 자율적으로 fail-safe 상태 진입
- **ESP32 fail-safe 동작:**
  - 인덕션 차단(시뮬레이션) 상태 유지
  - 후드는 안전 기본값으로 동작
  - 위험 상태에서는 인덕션 ON / 화력 증가 명령 거부

## 예상 장애요인 및 해결방안

| 장애요인 | 해결방안 |
|---|---|
| 수증기·기름 입자·환기 영향으로 PM 값 흔들림 | PM 절대값 대신 상승률·지속시간 사용, 열화상 정보와 교차 검증 |
| Wi-Fi 지연, UART 배선 불량, 포트 충돌 | 핵심 통신은 UART/Serial 우선, heartbeat와 timeout 적용 |
