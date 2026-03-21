---
title: "Julia: 개인 AI 에이전트를 설계하며 내린 10가지 결정"
date: 2026-03-22
tags: ["ai", "agent", "claude", "architecture", "personal-ai"]
draft: false
---

개인 AI 에이전트 Julia를 만들었다. 이메일이 오면 읽고 판단해서 답장하고, Slack 메시지에 반응하고, 일정을 확인하고, 문서를 정리한다. 이 글에서는 Julia를 설계하면서 내린 핵심 결정들과 그 배경을 정리한다.

## 1. Thin Daemon, Fat Brain

가장 근본적인 설계 결정이다. Julia의 Python daemon은 **이벤트를 수신하고 Claude Code를 실행하는 것이 전부**다. 판단, 계획, 도구 선택, 응답 생성은 모두 Claude Code 안에서 일어난다.

daemon에 도메인 로직이 없다는 것은, Julia의 행동을 바꾸고 싶을 때 `CLAUDE.md` 텍스트 파일 하나만 수정하면 된다는 의미다. daemon을 재시작할 필요도 없다. 코드와 지능이 완전히 분리되어 있다.

## 2. 데이터는 이미 있는 곳에 둔다

Julia는 자체 데이터베이스를 만들지 않는다. 대신 기존 시스템을 그대로 사용한다.

- **GitHub repos** = 모든 아젠다의 source of truth (README frontmatter가 구조화된 메타데이터)
- **Gmail/Calendar** = `gws` CLI로 실시간 조회
- **Google Drive** = rclone mount로 로컬 파일처럼 접근
- **Slack** = 실시간 커뮤니케이션 채널

사실을 복사해서 저장하지 않는다. 매 요청마다 원본을 조회한다. 이것이 "Live query over cache" 원칙이다. 캐시된 정보는 반드시 오래된 정보가 된다.

## 3. 메모리는 합성된 지식만

Claude Code의 memory 디렉토리는 **합성된 지식**만 저장한다. 여러 소스를 종합한 판단, 사람과 프로젝트 사이의 연결, 사용자 선호도처럼 어떤 단일 시스템에서도 조회할 수 없는 것들이다.

GitHub에서 `gh`로 조회 가능한 사실, Gmail에서 읽을 수 있는 내용은 memory에 쓰지 않는다. 이 구분이 없으면 memory는 금방 오래된 사실들의 무덤이 된다.

## 4. AI의 머릿속을 사람이 볼 수 있게

memory 파일을 Obsidian 호환 포맷으로 작성한다. frontmatter에 `tags`, `person`, `projects` 필드를 넣고, 본문에 `[[wikilinks]]`를 사용한다.

cron이 5분마다 memory를 Google Drive로 rsync하면, Mac의 Obsidian에서 AI의 knowledge graph를 탐색할 수 있다. Dataview 쿼리로 사람별, 프로젝트별 대시보드도 자동 생성된다. AI의 지식이 블랙박스가 아니라 투명한 문서가 된다.

## 5. GitHub을 아젠다 시스템으로

별도의 프로젝트 관리 도구를 도입하는 대신, GitHub repo 자체를 아젠다 항목으로 사용한다. 네이밍 규칙으로 분류한다:

| 분류 | 네이밍 패턴 | 예시 |
|------|------------|------|
| 연구 | `sogang-qmp/{NNN}-{name}` | `122-tmos2-relax` |
| 행정 | `yw-choi/A{YYYY}-{NNN}-{title}` | `A2026-001-reappointment` |
| 강의 | `yw-choi/T{YYYY}-{semester}-{code}` | `T2026-1-PHYG004` |
| 행사 | `yw-choi/E{YYYY}-{MM}-{title}` | `E2026-08-ccp2026` |

`agenda_sync.py`가 이 repo들의 README frontmatter를 읽어 Obsidian 대시보드를 자동 생성한다. GitHub이 버전 관리와 프로젝트 관리를 동시에 담당한다.

## 6. 이벤트 기반, 폴링 없음

Julia는 능동적이지 않다. 이벤트를 기다린다.

- **Gmail**: GCP Pub/Sub로 Google이 push → daemon이 pull
- **Slack**: Socket Mode로 실시간 WebSocket 연결

능동적인 요소는 인프라 유지보수용 cron 작업뿐이다 (memory rsync, agenda dashboard 갱신, 헬스체크). 시스템이 무엇을 할지 예측 가능하다.

## 7. 반드시 답장한다

`CLAUDE.md`에 명시한 가장 중요한 규칙이다. **Julia는 받은 채널로 반드시 응답해야 한다.** 이메일이 오면 이메일로 답장하고, Slack 메시지가 오면 같은 스레드에 답장한다.

이 규칙이 Julia를 백그라운드 자동화에서 **책임감 있는 대화 상대**로 바꿔준다. 사용자는 요청이 처리되었는지 항상 확인할 수 있다.

## 8. 우아하게 실패한다

완벽한 시스템은 없다. 대신 실패해도 괜찮도록 설계했다.

- **Grace timeout (60초)**: Claude Code가 오래 걸리면 "처리 중입니다" 메시지를 먼저 보내고, 백그라운드에서 계속 작업
- **동시성 제어**: 세마포어(limit 5)로 과부하 방지, 대기 중이면 사용자에게 알림
- **Watchdog**: 별도 프로세스가 로그를 감시하고, 에러 발생 시 자동으로 GitHub issue 생성 + Slack 알림
- **Drive 장애 격리**: rclone mount가 죽어도 Claude Code의 로컬 memory는 정상 작동

## 9. 서비스 생태계는 Convention으로

Julia는 `~/apps/` 아래 여러 서비스 중 하나다. 각 서비스는 자신의 `README.md`로 자기를 설명한다. Julia는 다른 서비스의 README를 읽어 동적으로 기능을 파악한다. 하드코딩된 서비스 레지스트리 같은 것은 없다.

## 10. Prompt Engineering = System Design

`CLAUDE.md`가 사실상 Julia의 전부다. 이 파일 하나에 다음이 모두 들어 있다:

- 정체성과 역할 정의
- 사용 가능한 도구 목록과 사용법
- 응답 규칙과 채널 매칭 요구사항
- 네이밍 규칙과 조직 분류 체계
- 메모리 기록 정책

Claude Code는 매번 실행될 때마다 이 파일을 로드한다. `CLAUDE.md`를 수정하면 코드 한 줄 안 건드리고 시스템의 행동이 바뀐다. 전통적인 시스템에서 코드 배포에 해당하는 것이 여기서는 텍스트 편집이다.

## 돌아보며

이 설계들의 공통점은 **기존 도구를 최대한 활용하고, 새로 만드는 것을 최소화**한 것이다. GitHub, Google Workspace, Obsidian, rclone — 이미 잘 작동하는 도구들 위에 얇은 접착제(thin daemon + CLAUDE.md)만 올렸다.

AI 에이전트 시스템을 처음부터 만들려면 웹 프레임워크, 데이터베이스, 인증 시스템, 큐 시스템 등이 필요하다고 생각하기 쉽다. 하지만 개인용이라면 Python asyncio daemon 하나와 잘 쓴 프롬프트 파일이면 충분했다. 복잡한 인프라 없이도 이메일을 읽고, 판단하고, 답장하는 AI를 만들 수 있다.
