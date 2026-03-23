---
title: "Julia: Slack과 Gmail로 쓰는 개인 AI 에이전트"
date: 2026-03-21
tags: ["ai", "agent", "claude", "architecture", "personal-ai"]
draft: false
---

Anthropic의 [Claude Code Channels](https://docs.claude.ai/en/docs/claude-code-channels)나 [OpenClaw](https://github.com/anthropics/openclaw) 같은 제품들이 나오고 있다. 이와 비슷하게 터미널이 아닌 Slack이나 이메일로 AI 에이전트와 대화하고, 여러 작업을 독립적인 쓰레드로 동시에 맡기는 걸 구현했다. 연구실 서버(vesper)에서 Python daemon으로 돌아가며, Slack DM이나 Gmail로 지시를 내리면 Claude Code가 실행되어 작업하고 같은 채널로 결과를 돌려준다.

코드는 [GitHub](https://github.com/yw-choi/julia)에 공개되어 있다. 이 글에서는 설계 결정들을 정리한다.

## 구조

전체 아키텍처는 단순하다.

```
Slack / Gmail  →  Python daemon  →  Claude Code subprocess
                  (이벤트 수신)      (판단, 도구 사용, 응답)
```

Python daemon은 얇다. Slack Socket Mode와 Gmail Pub/Sub에서 이벤트를 받아 Claude Code 프로세스를 spawn하는 것이 전부다. 도메인 로직은 없다. 판단, 계획, 도구 선택, 응답 생성은 전부 Claude Code가 한다. Julia의 행동을 바꾸고 싶으면 `CLAUDE.md` 텍스트 파일만 고치면 된다. daemon 재시작도 필요 없다.

## 독립적인 쓰레드

핵심 기능은 여러 작업을 동시에 맡길 수 있다는 것이다. Slack 쓰레드 하나, Gmail 쓰레드 하나가 각각 독립적인 Claude Code 세션에 매핑된다. 연구 계산 결과를 분석시키면서 동시에 다른 쓰레드에서 이메일 초안을 작성시킬 수 있다.

내부적으로 `dispatcher.py`가 이걸 관리한다. 각 쓰레드는 `slack:{thread_ts}` 또는 `email:{thread_id}` 형태의 키를 갖고, 세션 ID가 `state/sessions.json`에 매핑된다. 같은 쓰레드의 후속 메시지는 `claude --resume {session_id}`로 이전 컨텍스트를 이어받는다. 같은 쓰레드 내에서는 asyncio lock으로 직렬화하고, 다른 쓰레드끼리는 세마포어(최대 10개)로 병렬 실행한다. stdout은 pipe 대신 tempfile로 받아서 64KB 버퍼 데드락을 피한다.

## 채널

**Slack**: Socket Mode로 연결한다. DM과 `#julia-assistant` 채널에서는 모든 메시지에 반응하고, 다른 채널에서는 @멘션에만 반응한다. 메시지를 받으면 즉시 :eyes: 이모지를 달고, 완료하면 :white_check_mark:으로 바꾼다. Claude Code가 응답할 때는 `bin/slack_send.py` CLI를 호출한다.

**Gmail**: GCP Pub/Sub pull로 새 메일 알림을 받는다. 전용 계정(`julia.agent10@gmail.com`)을 쓰고, 허용된 발신자 목록(`JULIA_ALLOWED_SENDERS`)의 메일만 처리한다. 스팸, 프로모션, 자기가 보낸 메일은 걸러낸다. watch는 만료 하루 전에 자동 갱신된다.

두 채널 모두 파일 첨부를 지원한다. 첨부 파일을 `tmp/` 디렉토리에 내려받아 Claude Code 프롬프트에 경로를 넘긴다.

## 데이터는 복사하지 않는다

Julia는 자체 DB가 없다. GitHub repo가 프로젝트의 source of truth이고, Gmail/Calendar는 `gws` CLI로 실시간 조회하고, Google Drive는 rclone mount로 로컬 파일처럼 접근한다. 사실을 복사해서 캐싱하지 않고 매번 원본을 조회한다. Claude Code의 memory에는 여러 소스를 종합한 판단이나 사람-프로젝트 간 관계처럼, 단일 시스템에서는 뽑아낼 수 없는 합성된 지식만 기록한다.

memory 파일은 Obsidian 호환 마크다운이다. cron이 5분마다 Google Drive로 rsync하면 Mac의 Obsidian에서 AI의 knowledge graph를 열람할 수 있다.

## 운영

Watchdog이라는 별도 프로세스가 로그 파일을 감시한다. 에러가 발생하면 Claude Code를 호출해서 원인을 분석하고, GitHub issue를 생성하고, Slack으로 알림을 보낸다.

systemd 서비스로 배포한다. `julia.service`, `watchdog.service`, `rclone-drive.service` 세 개. Julia 서비스의 `TimeoutStopSec`은 5초로, 재배포 시 빠르게 재시작된다.

GitHub repo를 아젠다 시스템으로도 쓴다. 연구(`sogang-qmp/{NNN}-{name}`), 행정(`A{YYYY}-{NNN}`), 강의(`T{YYYY}-{semester}-{code}`), 행사(`E{YYYY}-{MM}-{title}`) 같은 네이밍 규칙으로 분류하고, `agenda_sync.py`가 README frontmatter를 읽어 Obsidian 대시보드를 생성한다.

---

결국 기존 도구(GitHub, Google Workspace, Slack, Obsidian) 위에 얇은 접착제를 올린 것이다. Python daemon은 이벤트 라우팅만 하고, `CLAUDE.md`가 시스템의 행동 전체를 정의한다. 코드를 고치지 않고 프롬프트만 고쳐서 행동을 바꿀 수 있다는 게 이 구조의 장점이다.
