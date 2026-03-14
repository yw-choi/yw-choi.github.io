---
title: "Hive 업데이트: Markdown에서 MCP 서버까지"
date: 2026-03-14
tags: ["lab", "ai", "mcp", "infrastructure"]
draft: false
---

[이전 글](/blog/2026-03-11-hive/)에서 Hive를 소개하면서 "별도의 서버나 웹앱 없이 GitHub + markdown + Claude로 충분하다"고 했는데, 3일 만에 서버를 만들었다. YAGNI라고 해놓고.

변명을 하자면, 실제로 써보니 GitHub repo만으로는 부족한 부분이 금방 드러났다.

## 뭐가 부족했나

GitHub repo + CLAUDE.md 조합은 프로젝트 단위 작업에는 잘 맞는다. 그런데 **cross-project** 작업이 문제다. "전체 프로젝트 현황 보여줘", "지난주에 업데이트 없는 프로젝트 뭐야", "이번 주 미팅 준비 자료 만들어줘" 같은 요청을 하면 Claude가 여러 repo를 하나씩 돌면서 파일을 읽어야 한다. 느리고 토큰도 많이 쓴다.

또 하나는 **Claude Code 세션 추적**이다. 하루에 수십 개 세션을 돌리는데, 어떤 프로젝트에서 얼마나 작업했는지, 토큰은 얼마나 썼는지 전혀 파악이 안 됐다.

## 현재 구조

결국 가벼운 백엔드를 하나 올렸다.

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

**hive-server**는 FastAPI + SQLite다. 프로젝트, 태스크, 사람, 노트를 관리하고, Claude Code 세션 메타데이터(시작/종료 시간, 토큰 사용량, 사용 도구 등)를 수집한다. DB를 따로 관리하고 싶지 않아서 SQLite로 갔다.

**hive-mcp**는 이 서버 위에 [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) 레이어를 씌운 것이다. Claude.ai에서 integration으로 연결하면, 대화 중에 바로 Hive 데이터를 조회하고 수정할 수 있다. Claude Code에서도 MCP 서버로 연결해서 쓴다.

주요 MCP 도구들:

- `hive_projects` — 전체 프로젝트 목록과 상태 조회
- `hive_issues` — 프로젝트별 이슈 목록
- `hive_meeting_prep` — 특정 프로젝트의 최근 커밋 + 오픈 이슈를 모아서 미팅 자료 생성
- `hive_updates` — 오래된 프로젝트나 밀린 이슈 등 PI한테 필요한 알림
- `analytics_summary` — 기간별 Claude Code 사용 통계
- `read_file`, `write_file`, `edit_file` — GitHub repo 파일 직접 조작
- `git_commit`, `git_push` — 커밋과 푸시

## Overmind

`analytics_summary`가 꽤 유용하다. 지난 30일간 세션 246개, output 토큰 250만 개를 썼다는 걸 이제 숫자로 볼 수 있다. 프로젝트별, 날짜별로 어디에 시간을 쓰고 있는지 파악이 된다. Claude Code 세션이 끝날 때 `export_session`으로 요약을 남기면, 나중에 "지난주에 뭐 했더라" 할 때 찾아볼 수 있다.

내부적으로 이 분석 레이어를 Overmind라고 부르고 있다. 아직은 단순 로그 수집 수준이지만, 프로젝트 간 연결고리나 연구 방향 제안 같은 것도 해볼 수 있을 것 같다.

## 원래 철학은 살아있나

이전 글의 핵심 원칙이 "GitHub is everything, convention over infrastructure"였는데, 서버를 올리면서 이게 좀 흔들렸다. 다만 연구 데이터 자체는 여전히 GitHub repo에 있고, Hive 서버는 그 위에 메타데이터 레이어 역할만 한다. 서버가 날아가도 연구 데이터는 GitHub에 그대로 있다. 이 정도면 수용 가능한 트레이드오프라고 본다.

코드량도 아직 많지 않다. FastAPI 서버 + MCP 서버 합쳐서 수천 줄 정도. SQLite 파일 하나. 유지보수 부담이 크지 않은 선에서 관리하려고 한다.

## 다음

- 학생들 온보딩: MCP 연결 설정, 기본 사용법 교육
- 실제 프로젝트 데이터 마이그레이션
- Slack 연동 (미팅 리마인더, 이슈 알림)
- SmartFeed 데이터를 Hive에 통합하는 것도 고려 중
