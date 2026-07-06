# scripts — 설치·실행 스크립트

노드별 환경 설정과 실행을 자동화하는 스크립트를 둡니다.

예정 목록 (MVP 진행하며 추가):

- `setup_pi4.sh` — Pi 4 의존성 설치 (OpenCV, pyserial, 음성 인식 런타임 등)
- `setup_pizero.sh` — Pi Zero SPS30 수집 환경 설치
- `flash_esp32.sh` — ESP32 펌웨어 빌드·플래시
- `run_demo.sh` — End-to-End 데모 실행
- `replay_log.py` — 센서 로그 재생 (임계값 보정용)
