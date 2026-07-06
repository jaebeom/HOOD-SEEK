# config — 임계값·제어 정책 설정

판단 로직의 임계값을 코드에 하드코딩하지 않고 여기서 버전 관리합니다. 개발 일정에 따라 **매월 측정 결과를 기반으로 임계값과 제어 정책을 보정**하며, 보정 이력이 커밋 히스토리로 남습니다.

## 보정 워크플로

1. 실조리 환경에서 센서 로그 수집 (`pizero/sps30/` 로그, 열화상 캡처)
2. `scripts/replay_log.py`(예정)로 로그를 재생하며 현재 임계값의 오탐/미탐 확인
3. `thresholds.yaml` 수정 → 시나리오 테스트(TS-1~TS-5) 통과 확인 → 커밋

## 파일

| 파일 | 버전 관리 | 내용 |
|---|---|---|
| `thresholds.example.yaml` | O | 임계값 스키마 예시 (실측 전 초기값) |
| `thresholds.yaml` | O | 팀 공식 보정본 — 매월 보정 이력이 커밋 히스토리로 남음 |
| `thresholds.local.yaml` | X (gitignore) | 개인 실험·로컬 환경용 오버라이드 |

## 로드 우선순위

```
thresholds.local.yaml > thresholds.yaml > thresholds.example.yaml
```

개인 주방·실험실 환경에 맞춘 값은 `thresholds.local.yaml`에만 적어 팀원 간 Git 충돌을 방지합니다. 실측 검증을 거쳐 팀 공식값으로 확정된 것만 `thresholds.yaml`에 반영해 커밋합니다.
