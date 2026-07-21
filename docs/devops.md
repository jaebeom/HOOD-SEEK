# DevOps 가이드

이 저장소의 CI/CD 구성과 로컬에서 같은 검사를 돌리는 방법을 정리합니다. **Git·GitHub가 처음이거나 익숙하지 않다면 바로 아래 [팀원 협업 가이드](#-팀원-협업-가이드)부터 읽어주세요.**

---

## 👋 팀원 협업 가이드

Git이 익숙하지 않아도 괜찮습니다. 아래 순서만 따라 하면 되고, 막히면 팀 채팅에 바로 물어보세요 — **질문은 빠를수록 좋습니다.** 잘못 눌러서 뭔가 망가뜨릴까 봐 걱정할 필요 없어요. 이 저장소는 자동 검사(CI)가 지켜보고 있어서, 문제가 있는 코드는 합쳐지기 전에 걸러집니다.

### 0단계. 처음 한 번만 하는 준비

```bash
# 1) 저장소를 내 컴퓨터로 복사
git clone https://github.com/jaebeom/HOOD-SEEK.git
cd HOOD-SEEK

# 2) 개발 도구 설치 (린트, 테스트 도구)
pip install -r requirements-dev.txt

# 3) pre-commit 설치 — 커밋할 때마다 자동으로 검사해주는 "문지기"
pre-commit install
```

`pre-commit install`은 딱 한 번만 하면 됩니다. 이후 `git commit` 할 때마다 오타·깨진 링크·대용량 파일 같은 실수를 **커밋되기 전에** 자동으로 잡아줘요. 내가 실수해도 기계가 먼저 알려주니 안심하고 작업하면 됩니다.

자기 담당 노드의 실행 의존성도 설치해 두세요 (예: Pi 4 담당이면 `pip install -r pi4/requirements.txt`).

### 1단계. 작업을 시작할 때 (매번)

**main 브랜치에서 직접 작업하지 않습니다.** main은 "언제나 동작하는 완성본"을 보관하는 곳이고, 작업은 각자의 브랜치에서 합니다. 이렇게 하면 내 실험 코드가 팀원의 작업을 망칠 일이 없어요.

```bash
# 1) main을 최신 상태로
git checkout main
git pull origin main

# 2) 내 작업 브랜치 만들기
git checkout -b feat/mvp2-smoke-score
```

브랜치 이름 규칙:

| 접두사 | 용도 | 예시 |
|---|---|---|
| `feat/` | 기능 개발 | `feat/mvp2-smoke-score` |
| `fix/` | 버그 수정 | `fix/uart-timeout` |
| `docs/` | 문서 수정 | `docs/wiring-diagram` |

### 2단계. 작업하면서

- **커밋은 작게, 자주** 하세요. "하루치 몽땅 커밋 1개"보다 "의미 있는 단위로 5개"가 리뷰하기도, 되돌리기도 쉽습니다.
- 커밋 메시지는 "무엇을 왜"가 보이게:
  - 좋아요: `SmokeScore 이동평균 윈도우를 10초로 조정 (튀는 값 완화)`
  - 아쉬워요: `수정`, `ㅁㄴㅇㄹ`, `최종`
- **임계값 실험은 `config/thresholds.local.yaml`에서** 하세요. 이 파일은 git에 올라가지 않아서 마음껏 바꿔도 충돌이 안 납니다. 팀 공식값(`thresholds.yaml`)은 실측 검증 후에만 수정해요.
- **모델 가중치 같은 큰 파일은 커밋 금지** — 1MB 넘으면 pre-commit이 자동으로 막아줍니다. 가중치는 릴리스로 배포해요 ([models/README.md](../models/README.md)).
- 통신 규격(`shared/protocol/`)을 바꿀 땐 **`protocol.py`와 `protocol.h`를 반드시 같은 커밋에서 함께** 수정하세요. 하나만 바꾸면 검사가 실패합니다 (일부러 그렇게 만들었어요).

> 💡 **커밋했는데 빨간 글씨가 떠요!** 당황하지 마세요. pre-commit이 문제를 발견한 겁니다. 메시지를 읽어보면 대부분 "공백 정리했음", "이 링크가 깨졌음"처럼 원인이 적혀 있어요. 훅이 파일을 자동으로 고쳐준 경우라면 `git add .` 후 다시 커밋하면 됩니다.

### 3단계. 작업 올리기 (Pull Request)

```bash
git push -u origin feat/mvp2-smoke-score
```

푸시하면 터미널에 PR 생성 링크가 뜹니다. GitHub에서 **Pull Request(PR)** 를 만들면 — "내 브랜치의 변경사항을 main에 합쳐주세요"라는 요청이에요 — PR 템플릿이 자동으로 채워지니 항목대로 작성하면 됩니다.

머지(합치기)까지의 흐름:

1. PR 생성 → CI가 자동으로 돌기 시작 (2~3분)
2. 팀원 1명 이상에게 리뷰 요청
3. **CI 초록불 ✅ + 리뷰 승인** → Merge 버튼 클릭
4. 머지 후 브랜치는 삭제하고, 로컬에서 `git checkout main && git pull origin main`으로 최신화

### 4단계. CI가 빨간불이에요 😱

정상입니다! CI는 원래 문제를 잡으라고 있는 거예요. 저장소의 **Actions 탭 → 실패한 실행 → 빨간 X가 뜬 잡**을 클릭하면 어디서 실패했는지 로그가 보입니다.

| 실패한 잡 | 원인 | 해결 |
|---|---|---|
| `lint` | Python 문법·스타일 문제, 깨진 YAML | 로컬에서 `ruff check .` 실행 → 파일:줄번호가 나오니 그대로 수정 |
| `consistency` | `protocol.py` ↔ `protocol.h` 불일치, 깨진 문서 링크 | `python scripts/check_protocol_sync.py`, `python scripts/check_links.py`를 로컬 실행 → 메시지가 뭘 고칠지 알려줌 |
| `unit-tests` | 테스트 실패 | `pytest tests/unit -q`로 로컬 재현 → 코드 또는 테스트 수정 |

고친 뒤 **같은 브랜치에 다시 커밋·푸시하면 CI가 자동으로 재실행**됩니다. PR을 새로 만들 필요 없어요.

### 자주 겪는 상황 FAQ

**Q. 충돌(conflict)이 났대요.**
나와 팀원이 같은 파일의 같은 부분을 고쳤다는 뜻입니다. 침착하게:
```bash
git checkout 내브랜치
git pull origin main   # main의 최신 내용을 가져오면 충돌 부분이 표시됨
```
파일을 열면 `<<<<<<<` ~ `=======` ~ `>>>>>>>` 마커가 있어요. 위쪽이 내 코드, 아래쪽이 main의 코드입니다. 남길 내용만 남기고 마커를 지운 뒤 커밋하면 끝. **어느 쪽을 남겨야 할지 모르겠으면 그 코드를 쓴 팀원에게 물어보고 함께 해결하세요** — 혼자 추측으로 지우는 게 제일 위험합니다.

**Q. 실수로 main에서 작업(커밋)해버렸어요.**
푸시 전이라면 살릴 수 있어요:
```bash
git branch feat/my-work   # 지금 커밋을 새 브랜치로 백업
git checkout main
git reset --hard origin/main   # main을 원격 상태로 되돌림
git checkout feat/my-work      # 작업은 새 브랜치에 그대로 있음
```

**Q. 방금 커밋 메시지를 잘못 썼어요.**
푸시 전이면 `git commit --amend`로 바로 고칠 수 있습니다.

**Q. 절대 하면 안 되는 것은?**
- `main`에 직접 푸시 (PR 없이)
- 비밀번호·토큰·API 키 커밋 (한 번 올라가면 히스토리에 영원히 남습니다)
- `--force` 푸시 (공유 브랜치의 팀원 커밋이 날아갈 수 있어요. 필요하다 싶으면 먼저 물어보기)

**Q. 뭔가 단단히 꼬였어요.**
저장소를 새로 클론하는 것도 부끄러운 일이 아닙니다. 로컬이 아무리 꼬여도 푸시하지 않았다면 팀에는 아무 영향이 없어요. 그래도 헤매는 시간이 10분을 넘으면 팀 채팅에 스크린샷과 함께 올려주세요.

---

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
