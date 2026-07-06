# pizero — 센서 게이트웨이 (Raspberry Pi Zero)

후드 흡입부 근처에서 SPS30 데이터를 안정적으로 수집하고, Pi 4의 동작 상태를 감시하는 보조 노드입니다.

## 모듈 구성

| 디렉토리 | 담당 기능 |
|---|---|
| `sps30/` | SPS30 PM1.0/2.5/4/10 수집·로그화, Pi 4로 전달 (Serial/UART — 패킷 규격은 [shared/protocol/](../shared/protocol/) 참조) |
| `watchdog/` | Pi 4 heartbeat 감시 — 정지·단절 감지 시 fail-safe 전환 트리거 |

## 배치 주의사항

- SPS30은 기름·수증기가 직접 응축되지 않는 위치에 배치
- 상세 배선·배치는 [docs/hardware.md](../docs/hardware.md) 참고
