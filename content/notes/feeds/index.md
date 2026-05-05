---
title: "Lab Tools: feeds (LLM-scored RSS reader)"
date: 2026-05-05
author:
  name: "Young Woo Choi"
  email: "ywchoi02@sogang.ac.kr"
---

> ⚠️ This note is meant to publish lab tools we actually use, but the present draft was written by Claude. It has not yet been reviewed by Y.W. Choi. Treat the description as agent-generated until that review happens.

A daily RSS reader that scores every incoming article 1 to 5 against my research profile, groups results into a single static HTML page, and posts the link to Slack. Lives at [`sogang-qmp/feeds`](https://github.com/sogang-qmp/feeds); the live output is at <https://vesper.sogang.ac.kr/feeds/>.

## Core idea

Most RSS readers give you the firehose. The point of `feeds` is to keep the firehose, but pre-sort it once a day so the highest-scored items are visible at a glance. Three pieces.

**1. Sources.** An OPML file (`feeds.opml`) lists the journal RSS feeds, grouped by folder; in practice this is a Feedly export. Two more sources are stitched in alongside RSS: GitHub (trending/searched repos that match the profile) and OpenAlex (curated literature recommendations). Everything is fetched into a single SQLite database (`feeds.db`), deduplicated by link.

**2. Scoring.** Every uncurated article is sent in batches to Claude Haiku with a `research_profile.yaml` describing the researcher (areas, keywords, current interests with weights). The model returns an integer score per article:

- **5** — directly related to a core topic or current interest
- **4** — closely related or trending in a related area
- **3** — somewhat related
- **2** — tangentially related
- **1** — not related

Articles matching `current_interests` topics are forced to score at least 4; trending GitHub repos in relevant areas get a +1 bonus. Failed batches are recorded and the affected articles are filed as score 1 rather than dropped, so nothing silently disappears. The profile YAML is free-form text passed straight into the prompt, which means tuning the agent's behavior is just rewriting English in one file.

**3. Output.** A static HTML page (`html/{YYYY-MM-DD}.html`, plus a `latest.html` symlink and an `index.html` listing) renders the scored articles grouped by OPML folder and feed, with a colored score column on the left so 5s and 4s pop visually. The same generator emits a "Literature" tab: 12 OpenAlex-derived recommendations split into Recent / Classic / Exploratory tiers, with Haiku writing one-sentence rationales. Once the page is built, `notify.py` posts the URL to a dedicated Slack channel.

A 90-day rotating log file records every API call and its cost. The whole pipeline runs from cron once a day:

```cron
0 9 * * * cd /path/to/feeds && python main.py fetch && python main.py curate
```

Static HTML is served by nginx (`nginx-feeds.conf`).

## Why this shape

A few decisions that turned out to matter:

- **Static HTML, no SPA.** The output is a single file per day with inline CSS. Serving via nginx means no runtime, no auth, no JS framework, no breakage when a dependency changes. The downside (no live filtering) is fine because the scoring already does the filtering.
- **Profile as free-form YAML.** Rewriting `current_interests` in English is the only knob; there is no rule engine to maintain. When a research direction changes, the agent's behavior changes the next morning.
- **Scoring runs once.** Articles are scored on first sight and never re-scored, so cost stays bounded as the DB grows.
- **Failures degrade, don't crash.** A failed Haiku batch becomes score-1 articles plus a Slack warning, not a missed daily run.

## Example output

The live page at <https://vesper.sogang.ac.kr/feeds/latest.html> is the canonical example. A typical day looks like this in shape (table abridged):

| Score | Title |
|---|---|
| **5** | Induced discommensurations in the lock-in transition of charge-density waves — Inagaki & Tanda |
| **5** | Polymer-free van der Waals assembly of 2D material heterostructures using muscovite crystals |
| **4** | Kinetically Arrested Twin-Domain State in Formamidinium Lead Iodide — Liang et al. |
| **4** | Polarization-controlled effective Rabi dynamics in driven graphene: a Floquet-Magnus approach |
| **3** | Demonstration of a fermion Quadrupling Condensate via Quantum Monte Carlo Simulation |
| ... | ... |
| **1** | Hantavirus crops up on a cruise ship — what scientists are watching |

181 articles is a typical daily volume. 5s and 4s are usually under 10 percent; the rest collapses into a long visual tail of 1s and 2s that can be skimmed in seconds.
