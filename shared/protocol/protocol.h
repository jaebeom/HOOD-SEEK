/*
 * 노드 간 UART 통신 규격 — C 헤더 (ESP32).
 *
 * 단일 소스 원칙: 규격 변경은 이 파일과 protocol.py를 같은 커밋에서 함께 수정한다.
 * 사람용 명세는 docs/communication.md 참고.
 * TBD 수치는 MVP 1 HW bring-up에서 확정한다.
 */
#ifndef HOODSEEK_PROTOCOL_H
#define HOODSEEK_PROTOCOL_H

/* 프레임 구조: SOF(1B) | TYPE(1B) | SEQ(1B) | LEN(1B) | PAYLOAD(LEN) | CRC(2B) */
#define PROTO_SOF 0xAA /* TBD: MVP 1에서 확정 */
#define PROTO_CRC_SIZE 2 /* CRC-16, 다항식 TBD */

/* 메시지 타입 — Pi Zero -> Pi 4 */
#define TYPE_PM_DATA 0x01
#define TYPE_GW_STATUS 0x02

/* Pi 4 -> Pi Zero */
#define TYPE_PI4_HEARTBEAT 0x10

/* Pi 4 -> ESP32 */
#define TYPE_CONTROL 0x20
#define TYPE_ESP_HEARTBEAT 0x21

/* ESP32 -> Pi 4 */
#define TYPE_ACK_STATUS 0x30

/* CONTROL payload 값 */
typedef enum { RISK_LOW = 0, RISK_MEDIUM = 1, RISK_HIGH = 2, RISK_CRITICAL = 3 } risk_level_t;
typedef enum { HOOD_OFF = 0, HOOD_LOW = 1, HOOD_MID = 2, HOOD_HIGH = 3 } hood_level_t;
typedef enum {
  INDUCTION_NORMAL = 0,
  INDUCTION_LIMIT = 1,
  INDUCTION_CUTOFF = 2,
  INDUCTION_LOCK = 3
} induction_cmd_t;

/* 통신 타이밍 기본값 */
#define HEARTBEAT_INTERVAL_MS 500
#define ESP32_CMD_TIMEOUT_MS 2000 /* 초과 시 fail-safe 진입 */

#endif /* HOODSEEK_PROTOCOL_H */
