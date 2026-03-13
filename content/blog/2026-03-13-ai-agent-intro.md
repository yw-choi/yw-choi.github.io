---
title: "AI Agent 실전 활용 가이드: 교육과 행정 업무를 중심으로"
date: 2026-03-13
tags: ["ai", "agent", "claude", "chatgpt", "education", "productivity"]
draft: false
---

ChatGPT나 Claude 같은 AI 챗봇은 이제 많은 분들이 써보셨을 것입니다. 그런데 최근에는 한 단계 더 나아간 **AI Agent**가 빠르게 확산되고 있습니다. 단순히 질문에 답하는 것을 넘어, 이메일을 보내고, 일정을 잡고, 문서를 정리하는 등 **실제 업무를 대신 수행**하는 AI입니다.

이 글에서는 AI Agent가 무엇인지, 어떻게 시작하는지, 그리고 교육·행정 분야에서 바로 쓸 수 있는 활용 사례들을 정리해 보겠습니다. 코딩 지식은 전혀 필요 없습니다.

## AI 챗봇 vs AI Agent

|  | AI 챗봇 | AI Agent |
|--|---------|----------|
| **하는 일** | 질문에 답변 | 답변 + 실제 작업 수행 |
| **예시** | "이메일 초안 써줘" → 텍스트 출력 | "이메일 보내줘" → 실제로 Gmail에서 발송 |
| **외부 연동** | 없음 (복사-붙여넣기 필요) | 있음 (캘린더, 이메일, 문서 등 직접 접근) |

핵심 차이는 **도구 사용 능력**입니다. AI Agent는 이메일, 캘린더, 파일 시스템 등 외부 도구에 직접 접근하여 작업을 완료합니다. 사용자가 복사-붙여넣기할 필요가 없습니다.

## 어디서 시작하나요?

가장 쉽게 AI Agent를 경험할 수 있는 방법들입니다. 모두 웹브라우저에서 바로 사용 가능합니다.

### 1. Claude (Anthropic)

[claude.ai](https://claude.ai)에서 사용할 수 있습니다.

- **MCP (Model Context Protocol) 연동**: 설정에서 Google Drive, Gmail, Google Calendar, Slack, Notion 등을 연결할 수 있습니다. 연결하면 Claude가 이메일을 읽고, 일정을 확인하고, 슬랙 메시지를 보내는 등의 작업을 직접 수행합니다.
- 설정 방법: claude.ai → 좌측 하단 프로필 → Settings → Integrations에서 원하는 서비스 연결
- 자세한 안내: [Claude Integrations 공식 문서](https://support.anthropic.com/en/articles/11175166-how-do-i-connect-integrations-in-claude-ai)

### 2. ChatGPT (OpenAI)

[chatgpt.com](https://chatgpt.com)에서 사용할 수 있습니다.

- **GPTs & Actions**: 특정 업무에 특화된 커스텀 챗봇(GPTs)을 만들거나, 외부 API를 연결하여 실제 작업을 수행하게 할 수 있습니다.
- **플러그인**: 웹 검색, PDF 읽기, 데이터 분석 등 다양한 도구를 ChatGPT 안에서 바로 사용 가능합니다.
- 자세한 안내: [ChatGPT Actions 공식 문서](https://platform.openai.com/docs/actions)

### 3. Google Gemini

[gemini.google.com](https://gemini.google.com)에서 사용할 수 있습니다.

- Google Workspace(Gmail, Calendar, Drive, Docs)와 자연스럽게 통합되어 있습니다. 이미 Google 생태계를 쓰고 계시다면 진입 장벽이 가장 낮습니다.
- 자세한 안내: [Gemini Extensions 가이드](https://support.google.com/gemini/answer/13695044)

## 활용 사례: 교육

### 강의 자료 준비

> "다음 주 고체물리 강의에서 band structure를 다루는데, 학부 3학년 수준에 맞는 퀴즈 5문항 만들어줘. 난이도는 중간으로."

AI Agent에 강의 노트 PDF를 첨부하면, 해당 내용을 기반으로 퀴즈, 연습 문제, 요약 슬라이드 초안 등을 생성할 수 있습니다.

### 과제 피드백 초안 작성

> "학생이 제출한 이 보고서를 읽고, 주요 개선점 3가지와 잘한 점 2가지를 정리해줘."

학생 보고서를 업로드하면 구조, 논리, 표현 등에 대한 피드백 초안을 만들어줍니다. 최종 판단은 교수님이 하시되, 초안 작성 시간을 크게 줄일 수 있습니다.

### 실라버스 및 루브릭 작성

> "물리학실험 과목의 보고서 평가 루브릭을 만들어줘. 평가 항목은 실험 설계, 데이터 분석, 결론 도출, 보고서 형식 4가지로."

기존 실라버스를 첨부하면 일관된 형식으로 업데이트하거나, 새 과목의 초안을 빠르게 작성할 수 있습니다.

## 활용 사례: 행정

### 이메일 처리

> "오늘 온 메일 중 학생 요청 건만 모아서 요약해줘. 급한 건은 따로 표시하고."

Claude나 Gemini에 이메일을 연동하면, 매일 쌓이는 메일을 분류·요약하고 답장 초안까지 작성해줍니다.

### 회의록 정리

> "오늘 교수회의 녹음 파일인데, 안건별로 정리하고 각 안건의 결정사항과 후속 조치를 표로 만들어줘."

회의 녹음 파일이나 메모를 올리면 구조화된 회의록으로 변환해줍니다.

### 공문·보고서 초안

> "BK21 실적 보고서 양식인데, 우리 연구실 실적 데이터로 초안 채워줘."

양식과 데이터를 함께 제공하면, 형식에 맞춰 초안을 작성해줍니다. 반복되는 정기 보고서 작성 시간을 크게 절약할 수 있습니다.

### 일정 관리

> "다음 주 대학원 입시 면접 일정 잡아줘. 면접관 3명의 Google Calendar에서 공통 빈 시간을 찾아서."

캘린더 연동이 되어 있으면, 여러 사람의 빈 시간을 자동으로 확인하고 일정을 잡아줍니다.

## 활용 사례: 연구

### 논문 탐색 및 요약

> "최근 2년간 topological phonon 관련 논문 중 주요 리뷰 논문 5편을 찾아서 각각 한 문단으로 요약해줘."

AI가 웹 검색을 통해 관련 논문을 찾고 핵심 내용을 요약해줍니다. 새로운 분야를 빠르게 파악할 때 유용합니다.

### 데이터 시각화

> "이 CSV 파일의 band gap 데이터를 pressure에 대해 그래프로 그려줘. 실험값과 계산값을 구분해서."

ChatGPT나 Claude에 데이터 파일을 첨부하면 코드를 몰라도 그래프를 생성할 수 있습니다.

### 논문 초고 교정

> "이 manuscript 초고의 영어 표현을 다듬어줘. 학술 논문 스타일로, 원래 의미가 바뀌지 않게."

논문 교정 서비스에 보내기 전에 AI로 1차 교정을 하면 시간과 비용을 절약할 수 있습니다.

## 시작할 때 알아두면 좋은 것들

1. **구체적으로 지시하세요**: "잘 써줘"보다 "학부 3학년 수준으로, 500자 이내로, 핵심 개념 3가지를 포함해서 써줘"가 훨씬 좋은 결과를 냅니다.

2. **민감한 정보에 주의하세요**: 학생 개인정보, 미발표 연구 데이터 등은 외부 AI 서비스에 올리기 전에 한번 더 생각해 보시기 바랍니다. 각 서비스의 데이터 정책을 확인하시는 것이 좋습니다.

3. **결과를 검증하세요**: AI는 그럴듯하지만 틀린 답을 할 수 있습니다 (hallucination). 특히 숫자, 인용, 사실 관계는 반드시 확인하시기 바랍니다.

4. **반복 작업부터 시작하세요**: 처음부터 거창한 활용을 하려 하지 마시고, 매주 반복하는 단순 업무(이메일 정리, 회의록, 성적 입력 안내문 등)부터 AI에게 맡겨보세요.

## 더 읽어볼 자료

- [Anthropic Claude 공식 사이트](https://claude.ai) — MCP 연동으로 Agent 기능 사용 가능
- [OpenAI ChatGPT](https://chatgpt.com) — GPTs, 플러그인으로 확장 가능
- [Google Gemini](https://gemini.google.com) — Google Workspace 통합
- [MCP (Model Context Protocol) 소개](https://modelcontextprotocol.io/) — AI Agent가 외부 도구와 연결되는 표준 프로토콜
- [Ethan Mollick의 AI 교육 활용 블로그](https://www.oneusefulthing.org/) — Wharton 교수의 AI 교육 활용 사례 (영문)
- [UNESCO AI and Education 가이드](https://www.unesco.org/en/digital-education/artificial-intelligence) — 교육 분야 AI 활용 가이드라인
