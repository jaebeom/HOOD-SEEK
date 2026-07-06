# DevOps 가이드

이 저장소의 CI/CD 구성과 로컬에서 같은 검사를 돌리는 방법을 정리합니다.

## CI 파이프라인 (`.github/workflows/ci.yml`)

`main` 푸시와 모든 PR에서 3개 잡이 **병렬로** 실행됩니다.

| 잡 | 검사 내용 | 실패하는 경우 |
|---|---|---|
| `lint` | `ruff`(Python 린트) + `config/*.yaml` 문법 검증 | 문법 오류, 미사용 import, 깨진 YAML |
| `consistency` | `scripts/check_protocol_sync.py` + `scripts/check_links.py` | `protocol.py` ↔ `protocol.h` 상수 불일치, 깨진 문서 링크 |
| `unit-tests` | `pytest tests/unit` (테스트 없으면 스킵) | 단위 테스트 실패 |

`consistency` 잡이 이 프로젝트의 핵심 안전장치입니다 — 3개 노드가 공유하는 UART 규격이 어긋난 채 병합되는 것을 기계적으로 막습니다.

## 로컬에서 CI와 같은 검사 돌리기

```bash
pip install -r requirements-dev.txt

ruff check .                            # 린트
python scripts/check_protocol_sync.py  # 프로토콜 동기화
python scripts/check_links.py          # 문서 링크
pytest tests/unit -q                    # 단위 테스트
```

## pre-commit (커밋 전 자동 검사)

CI까지 가기 전에 로컬 커밋 단계에서 같은 문제를 잡습니다. 팀원 각자 1회 설치:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

이후 `git commit` 때마다 자동 실행됩니다. 포함된 훅:

- 공백·개행 정리, YAML 문법 검사
- **1MB 초과 파일 커밋 차단** — 가중치(`.onnx`/`.tflite`) 실수 커밋 방지
- ruff 린트
- 프로토콜 동기화·문서 링크 검사 (CI와 동일 스크립트)

전체 파일 대상 수동 실행: `pre-commit run --all-files`

## 브랜치 전략 (권장)

1. `main` 직접 푸시 대신 `feat/<mvp>-<작업>` 브랜치 → PR → 리뷰 1인 이상 → 머지
2. GitHub 저장소 Settings → Branches → `main`에 branch protection rule 추가:
   - Require a pull request before merging
   - Require status checks to pass: `lint`, `consistency`, `unit-tests`
3. 이슈는 `.github/ISSUE_TEMPLATE/`의 MVP 작업·버그 템플릿 사용, PR은 자동 적용되는 템플릿의 체크리스트 확인

## 다음 단계 (개발 진행에 따라 추가)

| 시점 | 추가할 것 |
|---|---|
| MVP 1 (`esp32/platformio.ini` 생성 후) | `ci.yml`에 주석으로 준비해 둔 `esp32-build` 잡 활성화 — PlatformIO 빌드 + 네이티브 단위 테스트 |
| 모델 도입 (MVP 4~5) | 가중치 릴리스 업로드 워크플로 + `scripts/` 다운로드 스크립트 검증 잡 |
| 통합 단계 (9월~) | 센서 로그 재생(`scripts/replay_log.py`) 기반 시나리오 회귀 테스트를 CI에 편입 |
| 시연 준비 (10월) | 태그 푸시 시 릴리스 노트 자동 생성 (`release.yml`) |
