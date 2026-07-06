# models — 온디바이스 경량 모델

Pi 4에서 사용하는 경량 추론 모델을 관리합니다. 대용량 가중치 파일은 **저장소에 커밋하지 않고**(`.gitignore` 처리) GitHub 릴리스 첨부로 배포하며, `scripts/`의 다운로드 스크립트로 받습니다.

## 구조

| 디렉토리 | 내용 |
|---|---|
| `weights/` | 다운로드된 가중치 배치 위치 (`.onnx`, `.tflite` 등 — git에 커밋되지 않음) |
| `export_scripts/` | 모델 최적화·변환 스크립트 (PyTorch → ONNX → TFLite export, 양자화 등) — 변환 이력을 코드로 버전 관리 |

| 용도 | 후보 | 예상 크기 | 목표 지연 |
|---|---|---|---|
| 사용자 존재 판단 | 경량 객체 탐지 (OpenCV 전처리 병행) | 5~15MB | 100~300ms |
| 반려동물·물체 탐지 | YOLOv5n / YOLOv8n / TFLite 변환 모델 | 5~12MB | 150~500ms |
| 음성 인식 | Vosk / Whisper.cpp tiny / 경량 KWS | 50~150MB 또는 KWS 수준 | 0.5~2s |

- 데이터가 부족할 경우 객체 탐지와 ROI 기반 규칙을 병행한다.
- SmokeScore·HeatScore·위험도 판단은 규칙 기반으로 별도 모델이 없다.
