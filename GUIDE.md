# 사용 설명서 (처음 쓰는 사람용)

설치하고 나서 **어떤 순서로, 어떤 상황에 어떤 스킬을 쓰는지**만 정리했습니다. 왜 이렇게 만들었는지는 [README.md](README.md)에 있습니다.

- 이 문서는 작업 공간에 설치되지 않고, Codex도 읽지 않습니다. 사람이 읽는 문서입니다.
- 외부 브라우저를 쓸 수 없는 환경이라면 터미널에서 `cat /tmp/kit/GUIDE.md`로 다시 봅니다.

## 1. 설치 (작업 공간 루트에서, 한 번)
```sh
git clone --depth 1 https://github.com/Ju-unn/codex-lean-kit /tmp/kit
sh /tmp/kit/install.sh
codex -m gpt-6.1-sol -c model_reasoning_effort="medium" --disable computer_use --disable browser_use
```
1. 키트는 **작업 공간 밖**(`/tmp/kit`)에 clone합니다. 작업 공간 안에 clone했다면 설치한 뒤 그 폴더를 지웁니다.
2. 설치되는 것: `AGENTS.md`, `.agents/skills/`(스킬 8개), `.codex/agents/`(역할 3개). 과제 README.md와 기존 파일은 건드리지 않습니다.
3. codex는 **설치한 다음에** 켭니다. 키트는 codex가 켜질 때 읽힙니다. 이미 켜져 있었다면 끄고 다시 켭니다.
4. 신뢰를 물으면 **trust**를 고릅니다. 역할 3개는 trust한 폴더에서만 로드됩니다.
5. 다른 터미널에서 역할을 확인합니다(토큰을 쓰지 않음).
   - `codex debug prompt-input -c 'model="gpt-6.1-sol"' hi | grep -c 'Available roles'`
   - 1이면 정상입니다. 출력에 오류 줄이 섞여 있으면 그 숫자는 믿지 않습니다.
   - 0이어도 진행할 수 있습니다. 키트가 역할의 모델을 직접 지정해 서브에이전트를 계속 씁니다.

처음 쓰는 환경이라면 더 확인합니다.
- 버전: `node --version && git --version && python3 --version && codex --version`
- `$`를 입력하면 스킬 8개가 팝업으로 뜹니다.
- 미리보기: `node -e "require('http').createServer((q,s)=>s.end('ok')).listen(3000,'0.0.0.0')"`를 실행하고 포트 3000으로 확인합니다(Ctrl+C로 종료).
- 플랫폼 도우미가 있으면 공개 스킬 적용 방법을 묻습니다. 안내가 다르면 그 안내를 따릅니다.

## 2. 스킬은 자동으로 쓰이나?
| 방법 | 동작 | 확실성 |
|---|---|---|
| `$스킬이름`을 입력하거나 문장에 스킬 이름을 씀 | Codex가 그 스킬을 반드시 읽고 따릅니다 | 확실함 |
| 그냥 요청함 ("계획 세워줘") | Codex가 스킬 설명을 보고 맞으면 스스로 씁니다. AGENTS.md에도 "단계를 요청받으면 그 스킬을 먼저 읽어라"가 있습니다 | 모델이 판단하므로 빠질 수 있음 |
| 다른 스킬이 부름 | `$lean-plan`과 `$verify-and-wrap` 끝의 `$handoff`, `$delegate-build` 안의 `$tdd`와 `$debugging`. worker는 항상 `$tdd`를 읽습니다 | 확실함 |

**단계를 바꿀 때는 `$스킬`을 직접 입력하세요.** 빠질 일이 없고, 단계를 넘긴 것이 내 결정이라는 기록이 대화에 남습니다. TDD, 디버깅, 인계는 대부분 알아서 따라옵니다.

## 3. 작업 순서
```
README를 직접 읽기
 └ "AGENTS.md의 Setup부터 해줘."            → 기준선 커밋, baseline 브랜치
$requirements-interview  ⇄  담당자            → 합의 확인
$lean-plan → 내가 승인 → ($handoff) → /new    → 계획 커밋
 └ "docs/HANDOFF.md를 읽고 이어서 진행해."
$delegate-build   (실패하면 $debugging)        → 작업마다 커밋
$quality-gate                                 → Must 수정
$verify-and-wrap → ($handoff)                 → REPORT
제출
```

| 분 (180분 기준) | 단계 | 입력 예시 | 끝나는 조건 | 내가 할 일 |
|---|---|---|---|---|
| 0–10 | 준비 | `AGENTS.md의 Setup부터 해줘.` | 기준선 커밋 | README를 먼저 직접 읽기, 시작 시각 적기 |
| 10–35 | 요구사항 | `$requirements-interview README 분석해서 요구사항 후보와 첫 라운드 질문 정리해줘. 코드는 아직 쓰지 마.` | 담당자가 합의 블록을 확인 | [담당자]·[자료] 질문은 담당자에게 전달하고 답을 `담당자 답변: …`으로 붙여넣기. [결정]은 내가 답하기 |
| 35–55 | 계획 | `$lean-plan 남은 시간 X분 기준으로 계획 세워줘.` | 승인 후 HANDOFF 작성 | 구조 2안 중 고르기, 범위 승인, `/new` 입력 |
| 55–135 | 구현 | `$delegate-build T1부터 진행해.` | MVP 작업이 테스트와 리뷰 통과 | 승인 요청 확인, 작업마다 나오는 3줄 설명 읽기, 기다리는 동안 남은 질문 |
| 135–155 | 점검 (기능 동결) | `$quality-gate 최종 리뷰해줘.` | Must 수정 완료 | Must와 나머지 나누기, 화면 직접 확인 |
| 155–170 | 마무리 | `$verify-and-wrap 검증하고 REPORT 작성해. 예상 질문으로 나를 점검해줘.` | REPORT와 HANDOFF가 코드·커밋과 맞음 | 예상 질문에 내 말로 답하기 |
| 170–180 | 제출 | — | 제출 완료 | 필수 파일과 저장 상태 확인 |

시간이 다르면 구간을 같은 비율로 줄입니다. 90분이면 절반입니다.

## 4. 상황별로 쓰는 것
| 이런 상황 | 입력 |
|---|---|
| 과제 README만 있다 | `AGENTS.md의 Setup부터 해줘.` 다음 `$requirements-interview` |
| 담당자가 답이나 자료를 줬다 | `담당자 답변: <붙여넣기>` |
| 구현 중에 새 요구사항이 나왔다 | `담당자 새 정보: <붙여넣기>. requirements.md에 반영하고 계획에 주는 영향만 알려줘.` |
| 테스트가 실패하거나 버그가 났다 | `$debugging 원인부터 찾아줘. 고치기 전에 원인과 변경 범위를 알려줘.` |
| 작은 수정을 바로 하고 싶다 | `$tdd <무엇을> 고쳐줘.` |
| 화면이 안 보인다 | `서버 실행해줘.` (0.0.0.0:3000에서 계속 돌고, `/ps`로 보임) |
| 대화가 길어졌다 (`/status`의 남은 컨텍스트가 40% 아래) | `$handoff` 다음 `/new`, 그리고 `docs/HANDOFF.md를 읽고 이어서 진행해.` |
| 지금 무엇을 할 차례인지 모르겠다 | `지금 단계와 다음에 쓸 스킬을 알려줘.` |
| 방금 바뀐 코드를 이해 못 했다 | `방금 바뀐 것을 무엇 → 왜 → 위험 3줄로 설명해줘.` |
| 중간에 리뷰를 받고 싶다 | `$quality-gate` |

- worker가 커밋하거나 명령을 실행할 때 승인 요청이 메인 화면에 뜰 수 있습니다. 내용을 보고 승인합니다.
- 서브에이전트(explorer, worker, reviewer)는 스킬이 알아서 띄웁니다. 직접 시킬 수도 있습니다: `explorer로 <무엇을> 찾아줘.`

## 5. 하지 말 것
- 작업 중에 AGENTS.md나 스킬 파일을 고치지 않습니다. 매 턴 같은 내용이어야 캐시가 유지됩니다.
- "다 만들어줘"처럼 한 번에 맡기지 않습니다. 단계마다 확인하고 승인합니다.
- 테스트 출력 없는 "완료"는 받지 않습니다.
- AI가 고치는 파일을 에디터에서 동시에 고치지 않습니다.
- push, 권장 외 모델, Computer Use, 승인·샌드박스 설정 변경은 쓰지 않습니다.

## 6. 작업 공간에 생기는 문서
| 파일 | 내용 | 만드는 스킬 |
|---|---|---|
| `docs/worklog.md` | 시각과 함께 계속 덧붙이는 작업 기록 | Setup, 이후 전체 |
| `docs/requirements.md` | 요구사항(R-n), 가정, 합의 블록 | `$requirements-interview` |
| `docs/plan.md` | 범위, 구조 2안, 작업 목록(T-n), 결정 기록 | `$lean-plan` |
| `docs/HANDOFF.md` | 다음 세션이나 다음 사람을 위한 인계 | `$handoff` |
| `docs/REPORT.md` | 최종 보고서: 검증 결과, 보안, 한계 | `$verify-and-wrap` |

## 7. 문제가 생기면
README.md의 "6. 문제가 생기면" 표를 봅니다. 역할이 안 뜰 때, clone이 안 될 때, 화면이 안 보일 때의 대처가 있습니다.
