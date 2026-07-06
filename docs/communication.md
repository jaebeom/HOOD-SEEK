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

## 메시지 설계 (초안)

Pi 4 → ESP32 제어 명령에 포함되어야 할 필드:

| 필드 | 설명 |
|---|---|
| `seq` | 시퀀스 번호 (중복/유실 감지) |
| `risk_level` | LOW / MEDIUM / HIGH / CRITICAL |
| `hood_level` | 후드 풍량 단계 (0=정지, 1=약풍, 2=중풍, 3=강풍) |
| `induction_cmd` | 인덕션 명령 (NORMAL / LIMIT / CUTOFF / LOCK) |
| `alert` | 부저·LED 경고 플래그 |
| `checksum` | 무결성 검증 |

ESP32 → Pi 4 응답: `seq` 에코 + 현재 액추에이터 상태 + 자체 fail-safe 상태.

> 상세 프레임 포맷(바이트 레이아웃, baud rate, CRC 방식)은 MVP 1(수동 제어 루프) 구현 시 확정한다.

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
