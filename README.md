# codex-lean-kit

OpenAI Codex용 작업 키트입니다. 앱 코드는 없고 **일하는 방식**만 담았습니다. 원칙은 다섯 가지입니다.
- 사람이 지휘하고 AI는 위임받은 일만 한다
- 숨은 요구사항은 질문으로 끌어낸다
- 테스트를 먼저 쓴다
- 증거 없이 완료라고 말하지 않는다
- 과설계하지 않는다

> 설치하면 작업 공간에 `AGENTS.md`, `.agents/skills/`(스킬 10개), `.codex/agents/`(역할 3개)가 생깁니다. 기존 파일은 덮어쓰지 않습니다.
>
> **처음 쓴다면 [GUIDE.md](GUIDE.md)부터 보세요.** 설치, 작업 순서, 상황별로 쓰는 스킬이 있습니다.

---

## 1. 왜 이렇게 만들었나

AI 실무 평가(Krafton Cofa Probe)는 결과물만이 아니라 **일하는 과정**을 봅니다.
- 근거: 공개 인터뷰, 공식 사이트, 대회 후기(Cofathon 3+1축 배점)를 교차 확인했습니다.
- 바탕 연구: Storey, *From Technical Debt to Cognitive and Intent Debt* (arXiv:2603.22106)

| 평가 축 | 배점 항목 | 키트의 장치 |
|---|---|---|
| 기술 | 유지보수성, 요구사항 충족, 기능 정확성, 실무 품질 위험, 완성도 | `lean-plan`(구조·DB), `tdd`, 작업별 리뷰, `quality-gate`(두 축 최종 리뷰), `verify-and-wrap` |
| 의도 | 목표 구체화, 재사용 작업 체계, 의도·맥락 유지, 검증 루프, 문제·제약 정의, 분해·위임 | 키트 자체, 질문 사다리, 합의 블록, 계획 문서, 작업 루프(위임 → 검증 → 리뷰 → 수정), 결정 기록 |
| 인지 | 동작·리스크 예측, 구조 이해, AI 결정 근거 이해 | 작업마다 3줄 설명(무엇 → 왜 → 위험), 결정 기록, 약점 브리프와 예상 질문 연습 |
| 소통 | 다른 사람이나 다른 세션이 이어갈 수 있는가 | `$handoff` → `docs/HANDOFF.md`, 미리 정한 두 시점에 실행 |

---

## 2. 구성과 원본

| 스킬 | 언제 | 하는 일 | 원본 (이식 방식) |
|---|---|---|---|
| `$requirements-interview` | 과제를 처음 받았을 때, 담당자 답을 받았을 때 | **열린 질문 전부를 라운드마다 질문**(개수 제한 없음). 사실은 AI가 찾고, 결정은 담당자에게, 기술 선택은 우리가. 합의 블록 확인 | mattpocock `grilling`(충실 이식) + `to-questionnaire` + juxt `elicit`(질문 기법) |
| `$lean-plan` | 코드를 쓰기 전 | MVP 자르기, 구조 2안(기본: 기능별 모듈 + 순수 도메인, 의존 방향·패턴·SOLID·생활 체조 일부), 파일 구조, 인터페이스, 전역 제약, 리뷰 초점, 수직 슬라이스 작업, 자체 점검, 승인 후 handoff | superpowers `writing-plans`(충실 이식) + mattpocock `to-tickets` |
| `$tdd` | 기능이나 버그 수정을 구현할 때 | **테스트 1개 → 실패 확인 → 최소 코드 → 전체 테스트 → 반복**. 테스트를 한꺼번에 먼저 쓰는 방식 금지 | superpowers `test-driven-development` + mattpocock `tdd`(충실 이식) |
| `$delegate-build` | 계획의 작업을 구현할 때 | worker가 구현 → 상태별 처리 → 메인이 직접 검증하고 커밋 → 위험 작업은 **작업별 리뷰** → 같은 worker가 수정 → 3줄 설명 | superpowers `subagent-driven-development`(충실 이식) |
| `$debugging` | 테스트 실패, 버그, 예상과 다른 동작 | **근본 원인 4단계**: 조사 → 패턴 → 가설 → 수정. 3번 실패하면 구조를 재검토 | superpowers `systematic-debugging`(충실 이식) |
| `$quality-gate` | MVP가 처음부터 끝까지 동작할 때 | **두 리뷰어 병렬**: 명세 축과 품질 축(보안·DB·과설계·Fowler 냄새). 구체적 사례가 있는 결함만 보고 | mattpocock `code-review` + ponytail-review + cloudflare·ECC 체크리스트 |
| `$verify-and-wrap` | 기능이 다 됐을 때, 완료라고 말하기 전 | 확인 절차(명령 → 실행 → 결과 읽기 → 판단), PASS/FAIL/NOT_RUN, REPORT, 일치 검사, 담당자에게 보낼 결과 메시지, 약점 브리프 | superpowers `verification-before-completion`(충실 이식) + ECC `verification-loop` |
| `$handoff` | 계획 승인 직후, 마무리 때, `/compact`·`/new` 전 | `docs/HANDOFF.md`: 다음 세션용(상태, 다음 단계, 다음 스킬)과 다음 사람용(실행 방법, 코드 지도, 위험) | mattpocock `handoff` + Cofathon 후기 |
| `$ui-design` | 화면을 만들거나 고치기 전 (자동) | 도구로 서로 다른 방향 2개를 미리 보고 **스타일·색·폰트를 사용자에게 묻는다**(답 전에는 화면 코드 금지) → 답대로 `docs/design.md` 저장, 대비 4.5:1 확인 → CSS `:root` 변수로 적용 → 접근성 우선순위와 제출 전 체크리스트. 새 UI 의존성 금지, 폰트는 시스템 대체 포함 | nextlevelbuilder `ui-ux-pro-max-skill`(스크립트·데이터·참고 문서는 원본 그대로, 절차는 충실 이식) |
| `$data-check` | 데이터 파일이 있거나 계산한 숫자를 낼 때 (자동) | 읽기만 하며 살펴보기 → 데이터 계약(한 행의 의미, 키, 단위, 분모, 재검사) → 모르는 의미는 담당자 질문 → 계산 → **핵심 숫자는 다른 방법으로 한 번 더 계산** → REPORT에 모집단·제외 건수 | 자체 작성 (공개 Cofa 키트 비교에서 착안) |

### 이식 원칙
- **핵심 절차는 원본을 충실히 옮겼습니다.** 원본의 철칙, 단계, 표, 경고 신호, 변명과 반박 표, 출력 형식이 그대로 들어 있습니다.
- 바꾼 것은 세 종류뿐입니다.
  1. Codex에서 동작하지 않는 부분: Claude 전용 도구 이름, 다른 스킬 강제 호출, "your human partner"
  2. 시험 규정: push 금지, 모델 제한
  3. 180분 제한

| 원본에서 뺀 것 | 이유 |
|---|---|
| worktree, 통합 브랜치, 이슈 트래커 (SDD, implement-spec, to-tickets) | push 금지 환경. worker는 많아야 2개를, 서로 겹치지 않는 파일에만 돌리므로 분리가 필요 없음 |
| 질문을 메시지당 하나씩 (brainstorming) | 시간 제한. 대신 grilling의 "라운드마다 열린 질문 전부" 방식을 씀 |
| 6단계 전체 보안 감사 (cloudflare) | 수 시간짜리 감사 절차. 검증 원칙과 공격 유형만 가져옴 |
| graphify | 큰 기존 코드베이스용. README만 있는 빈 작업 공간에는 효과가 없음 |
| ponytail 플러그인·훅 설치 | 훅은 `/hooks` 신뢰가 필요하고 Codex 설정을 바꾼다(시험 규칙 위험). 원본이 안내하는 훅 없는 방식대로 ponytail AGENTS.md 원문을 그대로 AGENTS.md에 넣음 |
| 1% 규칙으로 모든 스킬 강제 호출 (using-superpowers) | 상황 스킬(tdd, debugging, handoff, ui-design, data-check, 담당자 답변)만 자동으로 쓰고, 단계 전환은 Codex가 제안하고 사람이 정함(AGENTS.md "Skill use") |

참고 문서(필요할 때만 읽힘):
- `lean-plan/references/stack-ts.md`, `lean-plan/references/data-model.md`
- `delegate-build/references/brief-template.md`, `delegate-build/references/task-review-template.md`
- `quality-gate/references/review-spec.md`, `review-quality.md`, `security.md`, `overengineering.md`
- `requirements-interview/references/question-techniques.md`

작업 공간에 생기는 문서:
- `docs/requirements.md`
- `docs/qna.md` (질문과 답 원문, 한 파일)
- `docs/design.md` (화면 기준, 화면이 있을 때만)
- `docs/plan.md` (결정 포함)
- `docs/worklog.md` (계속 덧붙이는 기록)
- `docs/HANDOFF.md` (인계 스냅샷)
- `docs/REPORT.md`

**과제 README.md는 건드리지 않습니다.**

---

## 3. 역할과 모델

| 역할 | 모델 / effort | 하는 일 | 이유 |
|---|---|---|---|
| 메인(지휘) | `gpt-6.1-sol` / medium | 질문 안건, 계획, 검증, 문서, 사람과 대화 | 판단의 질이 결과를 좌우함. 허용 모델 중 가장 강함 |
| explorer | `gpt-6-luna` / medium | 읽기 전용 탐색 | 가격 1/20. 읽기에는 깊은 추론이 필요 없음 |
| worker | `gpt-6.1-sol` / medium | 작업 1개를 TDD로 구현하고 바꾼 파일을 보고(커밋은 메인) | 같은 가격에 Sol 6.0보다 강함. 한 번에 맞추는 편이 싸다("turn count beats token price") |
| reviewer | `gpt-6.1-sol` / high | 작업별 리뷰, 최종 리뷰 2개(병렬) | 결함을 잡으려면 깊이가 필요함 |

- 허용 모델은 대회 권장 4종뿐입니다: `gpt-6.1-sol`, `gpt-6-sol`, `gpt-5.6-terra`, `gpt-6-luna`.
- `gpt-6-sol`과 `gpt-5.6-terra`는 예비용입니다.

---

## 4. 사용법
설치, 작업 순서, 상황별 스킬은 **[GUIDE.md](GUIDE.md)**에 있습니다.

### git 사용 원칙
자료 근거: "Git Push 불가", "Git Clone과 구분", 수집 기록에 "git 로그·diff"
- **clone**: 허용. 키트를 받을 때 한 번만 씁니다.
- **commit**: 로컬. 작업마다 하나씩 하며 채점 자료가 됩니다.
- **push**: 금지. 키트에 push 명령이 없고 AGENTS.md로도 막습니다.
- git이 안 되면 커밋 없이 진행하고, 끝낸 작업을 시각과 함께 `docs/worklog.md`에 기록합니다.

---

## 5. 토큰 원칙: 품질을 먼저, 낭비만 줄인다
- 가장 큰 낭비는 **재작업**입니다. 질문, 계획, TDD, 작업별 리뷰에는 토큰을 아끼지 않습니다.
- 줄이는 것은 품질과 무관한 낭비뿐입니다.
  - 서브에이전트에 대화 전체를 복사하지 않습니다(`fork_turns:"none"`).
  - 문서 본문 대신 경로를 넘깁니다.
  - 명령 출력은 `tail`로 자릅니다.
  - 탐색에는 싼 모델을 씁니다.
  - 계획을 마친 뒤 `/new`로 새 세션을 엽니다.
- 매 턴 로드되는 것은 AGENTS.md(약 100줄)와 스킬 설명뿐입니다. 스킬 본문과 참고 문서는 쓸 때만 읽힙니다.
- spawn 1회의 고정 비용은 약 4만 토큰(대부분 캐시)입니다(실측). 그래서 몇 줄짜리 수정은 메인이 직접 합니다.

## 6. 문제가 생기면
| 증상 | 조치 |
|---|---|
| 역할 확인 결과가 0 (신뢰되지 않은 폴더) | `mkdir -p ~/.codex/agents && cp .codex/agents/*.toml ~/.codex/agents/` 후 codex 재시작. 사용자 수준 역할은 trust 없이도 로드됨(실측) |
| 실행 플래그 오류 | 플래그 없이 `codex` 실행 → `/model`에서 GPT-6.1-Sol, medium 선택 |
| 모델 이름이 다름 | `sed -i 's/gpt-6.1-sol/<실제 이름>/' .codex/agents/*.toml` |
| git clone 불가 | `curl -L https://github.com/Ju-unn/codex-lean-kit/archive/refs/heads/main.tar.gz \| tar xz -C /tmp && sh /tmp/codex-lean-kit-main/install.sh` |
| install.sh 실패 | `mkdir -p .agents .codex && cp -r /tmp/kit/.agents/skills .agents/ && cp -r /tmp/kit/.codex/agents .codex/` 실행. AGENTS.md는 복사하거나 기존 파일 뒤에 붙임 |
| Codex가 "agent_type 인자가 없다"고 함 | 역할이 로드되지 않은 것. 흔한 원인: 설치 전에 codex를 켬, 작업 공간 루트가 아닌 곳(아이콘 실행 등)에서 켬, trust를 안 고름. → 작업 공간 루트에서 codex 재시작 + trust, 그래도 0이면 첫 줄 조치. 그동안 키트는 역할 파일의 모델·effort를 직접 지정해 계속 위임함(실측: explorer가 gpt-6-luna/medium으로 뜸) |
| `spawn_agent` 자체가 없음 | 스킬마다 대안이 있음: 같은 절차를 메인이 직접 수행 |
| 웹 페이지가 안 보임 | "서버 실행해줘" → 미리보기 새로고침. `/ps`에 서버가 없으면(`/new` 뒤 등) 다시 요청. 그래도 안 되면 `curl localhost:3000`으로 확인, Vite면 allowedHosts 확인 |
| "Selected model is at capacity" | 서버가 붐비는 것. 잠시 뒤 다시 시도. 계속되면 `/model`에서 `gpt-6-sol`(medium)로 바꿔 진행하고, 나중에 되돌림. 서브에이전트는 키트가 자동으로 gpt-6-sol로 띄움. Astra는 금지 |
| `npm install` 실패 | 승인 후 한 번 다시 시도. 그래도 안 되면 키트가 Node 내장 기능(node:http, node:sqlite, node:test)으로 바꿔 진행하고 결정에 기록 |

## 7. 쓰지 않는 것
- **규정**:
  - `git push`, 외부 전송
  - 권장 외 모델(`gpt-6-astra` 등). spawn 도구에 Astra도 선택지로 보이므로, 역할 파일로 모델을 고정하고 AGENTS.md로 막습니다.
  - Computer Use, 브라우저 자동화
  - `--dangerously-*`, `-s danger-full-access`, `--approve-for-me`
- **effort**: `ultra`(작업을 자동 위임해 에이전트가 늘어남), `xhigh`, `max`
- **시험에 맞지 않는 것**: §2의 "원본에서 뺀 것" 표를 보세요.

## 8. 검증
- `python tests/check_kit.py`가 확인하는 것:
  - 모델 값 허용 목록 (금지 모델을 넣으면 잡아내는지 자체 테스트 포함)
  - 역할 필수 키
  - 스킬 형식 (Codex 내장 `quick_validate` 재사용)
  - 링크, 크기 예산, LF 줄바꿈
  - 설치 스크립트 (빈 폴더와 기존 파일이 있는 폴더에서 각각 2회)
- Codex 0.165.0 실측 (2026-10-29):
  - 신뢰하지 않은 폴더: AGENTS.md와 스킬은 로드되고 역할은 로드되지 않습니다.
  - 신뢰한 폴더: 역할이 로드되고 모델이 "cannot be changed"로 고정됩니다.
  - explorer 실행 결과 `gpt-6-luna`/medium이 확인됐습니다.
  - `~/.codex/agents`(사용자 수준)는 신뢰 없이도 로드됩니다.

## 9. 출처와 라이선스
- 이 키트는 MIT입니다(LICENSE).
- 옮기거나 각색한 원본은 모두 MIT이며 고지는 THIRD_PARTY_NOTICES.md에 있습니다:
  - obra/superpowers, mattpocock/skills, DietrichGebert/ponytail, affaan-m/ECC, cloudflare/security-audit-skill, softaworks/agent-toolkit, juxt/allium
