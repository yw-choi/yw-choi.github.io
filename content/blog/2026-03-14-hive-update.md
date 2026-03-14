---
title: "Hive 업데이트: Markdown에서 MCP 서버까지"
date: 2026-03-14
tags: ["lab", "ai", "mcp", "infrastructure"]
draft: false
---

[이전 글](/blog/2026-03-11-hive/)에서 Hive를 소개하면서 "별도의 서버 없이 GitHub + markdown으로 충분하다"고 했는데, 며칠 써보니 서버가 필요해져서 하나 올렸다.

## 부족했던 부분

GitHub repo + CLAUDE.md 조합은 프로젝트 단위 작업에는 괜찮다. 문제는 cross-project 작업이다. "전체 프로젝트 현황 보여줘", "업데이트 없는 프로젝트 뭐야" 같은 요청을 하면 Claude가 여러 repo를 하나씩 열어서 파일을 읽어야 한다. 느리고 토큰도 많이 든다.

Claude Code 세션 추적도 안 됐다. 하루에 세션을 수십 개 돌리는데, 어디에 시간을 쓰고 있는지 파악할 방법이 없었다.

## 현재 구조

```
Vesper (Lab Server)
├── hive-server    (FastAPI + SQLite)
│   ├── /projects, /tasks, /people, /notes  — CRUD API
│   └── /analytics  — Claude Code 세션 로그 수집
├── hive-mcp       (MCP Server)
│   └── Claude.ai / Claude Code에서 직접 호출
└── nginx reverse proxy
    └── vesper.sogang.ac.kr/hive-mcp
```

**hive-server**는 FastAPI + SQLite. 프로젝트, 태스크, 사람, 노트를 관리하고, Claude Code 세션 메타데이터(시작/종료 시간, 토큰 사용량, 사용 도구 등)를 수집한다.

**hive-mcp**는 이 서버 위에 [MCP](https://modelcontextprotocol.io/) 레이어를 올린 것이다. Claude.ai에서 integration으로 연결하면 대화 중에 Hive 데이터를 바로 조회·수정할 수 있다. Claude Code에서도 마찬가지.

주요 도구:

- `hive_projects` — 전체 프로젝트 목록과 상태
- `hive_issues` — 프로젝트별 이슈
- `hive_meeting_prep` — 최근 커밋 + 오픈 이슈를 모아 미팅 자료 생성
- `hive_updates` — 오래된 프로젝트, 밀린 이슈 알림
- `analytics_summary` — 기간별 Claude Code 사용 통계
- `read_file`, `write_file`, `edit_file` — GitHub repo 파일 직접 조작
- `git_commit`, `git_push` — 커밋, 푸시

## 세션 분석

`analytics_summary`가 쓸 만하다. 지난 30일간 세션 246개, output 토큰 약 250만 개. 프로젝트별·날짜별 작업 분포가 보인다. 세션이 끝날 때 `export_session`으로 요약을 남기면 나중에 되돌아볼 수 있다.

내부적으로 이 분석 레이어를 Overmind라고 부르고 있다. 아직 단순 로그 수집 수준이다.

## 트레이드오프

서버를 올리면서 "convention over infrastructure" 원칙이 좀 흔들렸다. 다만 연구 데이터 자체는 여전히 GitHub repo에 있고, Hive 서버는 메타데이터 레이어 역할만 한다. 서버가 날아가도 데이터는 GitHub에 그대로 남는다. 코드량도 FastAPI + MCP 합쳐서 수천 줄, DB는 SQLite 파일 하나.

## 다음

- 학생 온보딩: MCP 연결 설정, 기본 사용법
- 실제 프로젝트 데이터 마이그레이션
- Slack 연동 (미팅 리마인더, 이슈 알림)
- SmartFeed 데이터 통합 검토
