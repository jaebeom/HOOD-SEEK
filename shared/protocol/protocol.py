"""노드 간 UART 통신 규격 — Python 공용 정의 (Pi 4 / Pi Zero).

단일 소스 원칙: 규격 변경은 이 파일과 protocol.h를 같은 커밋에서 함께 수정한다.
사람용 명세는 docs/communication.md 참고.
TBD 수치는 MVP 1 HW bring-up에서 확정한다.
"""

# 프레임 구조: SOF(1B) | TYPE(1B) | SEQ(1B) | LEN(1B) | PAYLOAD(LEN) | CRC(2B)
SOF = 0xAA          # TBD: MVP 1에서 확정
CRC_SIZE = 2        # CRC-16, 다항식 TBD

# 메시지 타입 — Pi Zero -> Pi 4
TYPE_PM_DATA = 0x01
TYPE_GW_STATUS = 0x02

# Pi 4 -> Pi Zero
TYPE_PI4_HEARTBEAT = 0x10

# Pi 4 -> ESP32
TYPE_CONTROL = 0x20
TYPE_ESP_HEARTBEAT = 0x21

# ESP32 -> Pi 4
TYPE_ACK_STATUS = 0x30

# CONTROL payload 값
RISK_LOW, RISK_MEDIUM, RISK_HIGH, RISK_CRITICAL = 0, 1, 2, 3
HOOD_OFF, HOOD_LOW, HOOD_MID, HOOD_HIGH = 0, 1, 2, 3
INDUCTION_NORMAL, INDUCTION_LIMIT, INDUCTION_CUTOFF, INDUCTION_LOCK = 0, 1, 2, 3

# 통신 타이밍 기본값 (config/thresholds*.yaml의 comm 섹션이 우선)
HEARTBEAT_INTERVAL_MS = 500
ESP32_CMD_TIMEOUT_MS = 2000
