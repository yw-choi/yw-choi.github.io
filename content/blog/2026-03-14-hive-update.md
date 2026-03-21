---
title: "Hive 업데이트: AI-Native CLI와 MCP 서버"
date: 2026-03-14
tags: ["lab", "ai", "github", "hive", "mcp", "cli"]
draft: false
---

[이전 글](/blog/2026-03-11-hive/)에서 Hive의 기본 설계를 소개했다. 그 후 3일 동안 핵심 도구 두 가지를 만들었다: [hive-cli](https://github.com/sogang-qmp/hive-cli)와 [hive-mcp](https://github.com/sogang-qmp/hive-mcp). 이 글에서는 세 리포지토리의 역할과 설계를 정리한다.

## 세 리포지토리의 구조

```
sogang-qmp/hive          시스템 명세, 가이드 문서 (코드 없음, 전부 markdown)
sogang-qmp/hive-cli      Go CLI — Claude Code가 사용하는 도구
sogang-qmp/hive-mcp      TypeScript MCP 서버 — Claude.ai(웹)가 사용하는 도구
```

Claude Code(터미널)는 CLI를 직접 실행할 수 있지만, Claude.ai(웹)는 MCP를 통해야 한다. 그래서 도구가 두 개다.

| 환경 | 도구 | 작동 방식 |
|------|------|-----------|
| **Claude Code** (터미널) | hive-cli | `hive` 명령어를 직접 실행 |
| **Claude.ai** (웹) | hive-mcp | MCP 프로토콜로 vesper 서버에 연결 |

두 경로 모두 최종적으로 `gh` CLI를 통해 `sogang-qmp` org의 리포지토리들을 읽고 쓴다.

## hive (명세와 문서)

[sogang-qmp/hive](https://github.com/sogang-qmp/hive)는 시스템의 중심 리포지토리지만 코드가 없다. 들어있는 것:

- **Spec**: 프로젝트 상태 모델, 템플릿 구조, AI 연동 방식, 롤아웃 계획
- **가이드 문서**: 셋업, 일상 워크플로우, 미팅 사이클, Claude 사용법, 서버 사용법 등
- **CLAUDE.md**: 각 프로젝트 리포에 들어갈 AI 컨텍스트 파일의 원본

핵심 원칙은 초기 버전에서 진화했다:

1. **GitHub is the source of truth** — 연구 데이터와 문서는 모두 GitHub 리포에 있다. 다만 이제 분석과 추천을 위한 overmind 서버, MCP 브릿지를 위한 hive-mcp 서버가 추가되었다. 서버가 날아가도 데이터는 GitHub에 그대로 남는다.
2. **Convention over infrastructure** — 폴더 구조와 네이밍 규칙이 시스템. CLI와 MCP 서버는 이 convention 위에서 동작하는 도구다.
3. **AI-native** — CLAUDE.md가 convention을 정의하고, AI가 직접 작업. CLI도 AI agent가 주 사용자로 설계되었다.
4. **Living documentation** — README가 프로젝트와 함께 진화하고, `reports/`가 논문의 building block이 된다.

## hive-cli: AI가 쓰는 CLI

[sogang-qmp/hive-cli](https://github.com/sogang-qmp/hive-cli)는 Go + Cobra로 만든 CLI다. 특이한 점은 **주 사용자가 사람이 아니라 Claude Code**라는 것이다. Google Workspace CLI(`gws`)를 만든 Justin Poehnelt의 글 ["You Need to Rewrite Your CLI for AI Agents"](https://justin.poehnelt.com/posts/rewrite-your-cli-for-ai-agents/)에서 영감을 받았다.

### 주요 명령어

```
hive projects                  프로젝트 목록 (--status, --person 필터)
hive project <id>              프로젝트 상세 정보
hive issues                    전체 리포 이슈 조회 (--project, --assignee 필터)
hive meeting prep <id>         미팅 준비: 최근 커밋 + 열린 이슈 수집
hive docs search <query>       lab-docs 검색
hive analytics upload          Claude Code 세션 로그 업로드
hive analytics summary         토큰 사용량 등 통계 조회
hive updates                   개인화된 추천 (overmind 서버)
hive schema <command>          명령어의 입출력 스키마 출력
```

### AI-Native 설계

일반적인 CLI는 사람이 읽기 좋은 텍스트를 출력한다. hive-cli는 반대다.

**1. JSON-first 출력**

모든 명령어의 기본 출력이 `--output json`이다. 사람이 읽으려면 `--output human`을 명시해야 한다. LLM이 JSON을 파싱하는 게 자연어 테이블을 파싱하는 것보다 정확하기 때문이다.

**2. 자기 기술적(self-describing) 스키마**

`hive schema projects`를 실행하면 해당 명령어의 플래그, 타입, 기본값, 응답 구조가 JSON으로 출력된다. MCP의 tool schema와 같은 역할을 CLI에서 구현한 것이다.

**3. `--fields` 플래그로 컨텍스트 윈도우 절약**

`hive projects --fields id,status,title`처럼 필요한 필드만 요청할 수 있다. AI agent가 컨텍스트 윈도우를 아끼면서 작업할 수 있다.

**4. 구조화된 에러**

에러도 JSON이다:
```json
{"error": {"code": "not_found", "message": "project 099 not found"}}
```
에러 코드가 정해져 있어(`not_found`, `auth_error`, `validation_error`, `gh_error`) AI agent가 에러 유형에 따라 다른 대응을 할 수 있다.

**5. SKILL.md — Claude Code 스킬 정의**

리포에 `SKILL.md`가 포함되어 있다. Claude Code가 이 파일을 읽고 hive CLI 사용법을 학습한다. 일반적인 워크플로우, `--dry-run`으로 사전 확인하기, 업데이트 알림 처리 방법 등이 적혀 있다.

**6. 설치 시 Claude Code에 자동 등록**

`make install`을 실행하면 `~/.claude/CLAUDE.md`에 hive CLI에 대한 힌트가 자동으로 추가된다. 이후 모든 Claude Code 세션에서 사용자가 "hive"를 언급하면 Claude가 CLI를 사용할 수 있게 된다.

### 동작 흐름

```
사용자: "프로젝트 현황 보여줘"
  → Claude Code가 SKILL.md 참조
  → hive projects --output json --fields id,title,status 실행
  → hive-cli가 gh api로 sogang-qmp org의 리포 목록 조회
  → 각 리포의 README.md YAML frontmatter에서 메타데이터 추출
  → JSON 반환
  → Claude Code가 사용자에게 자연어로 요약
```

## hive-mcp: Claude.ai를 위한 MCP 서버

[sogang-qmp/hive-mcp](https://github.com/sogang-qmp/hive-mcp)는 연구실 서버(vesper)에서 돌아가는 MCP 서버다. Claude.ai 웹에서 연구실 GitHub 리포에 접근할 수 있게 해준다.

### 인증

GitHub OAuth로 사용자별로 인증한다. Claude.ai에서 hive-mcp에 연결하면 GitHub 로그인으로 리다이렉트되고, 이후 해당 사용자의 토큰으로 작업이 수행된다.

### 제공하는 도구 (16개)

| 카테고리 | 도구 | 설명 |
|----------|------|------|
| **Hive** | `hive_projects`, `hive_issues`, `hive_meeting_prep`, `hive_updates` | hive CLI 래핑 |
| **GitHub** | `get_issue`, `create_issue` | 이슈 조회/생성 |
| **파일** | `read_file`, `write_file`, `edit_file`, `list_files`, `delete_file` | 리포 파일 CRUD (자동 클론) |
| **Git** | `git_status`, `git_commit`, `git_push` | Git 작업 |
| **분석** | `export_session`, `analytics_summary` | 사용 통계 |

파일 작업은 vesper 서버의 `~/repos/<github-username>/` 디렉토리에 샌드박싱된다. 리포를 처음 참조하면 자동으로 클론한다.

### 기술 스택

- TypeScript + Express 5
- MCP SDK (`@modelcontextprotocol/sdk`) — Streamable HTTP transport
- vesper 서버에서 systemd + nginx로 배포
- 내부적으로 `gh` CLI, `git`, `hive` CLI를 subprocess로 호출

## 세 리포의 관계

```
┌─────────────────────────────────────────────────┐
│                  사용자 (학생/교수)                │
│         터미널에서 Claude Code 사용                │
│         또는 웹에서 Claude.ai 사용                 │
└──────────┬────────────────────┬──────────────────┘
           │                    │
     Claude Code             Claude.ai
           │                    │
     hive-cli (Go)         hive-mcp (TS)
           │                    │
           └────────┬───────────┘
                    │
              gh CLI / GitHub API
                    │
         sogang-qmp GitHub org
         ├── hive (문서)
         ├── 000-project-template
         ├── 001-mos2-dislocation
         ├── 002-bgw-eval
         └── ...
```

