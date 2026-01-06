# BrightBrief – System Architecture

## Overview

BrightBrief is a **daily automated pipeline** that converts curated, positive technology news into a published audio podcast episode.  
The system is designed to be **deterministic, repeatable, and recoverable**, prioritizing reliability and clarity over unnecessary complexity.

---

## High-Level Flow

1. Daily job trigger
2. News ingestion from trusted sources
3. Filtering and selection (signal over noise)
4. Summary generation
5. Script generation (two-narrator format)
6. Text-to-speech audio generation
7. Persistence and publishing
8. Frontend consumption

---

## Stage 1: Daily Trigger & Job Initialization

- A scheduled job (cron or managed scheduler) runs once per day.
- A new episode run is initialized with:
  - episode date
  - unique run ID
  - initial status (`started`)

### Failure considerations
- Job does not trigger
- Duplicate job runs
- Scheduler downtime

All failures must be logged and observable.

---

## Stage 2: News Ingestion

- Latest articles are fetched from predefined, reputable sources:
  - RSS feeds
  - Licensed APIs
- Raw article metadata is collected for processing.

### Failure considerations
- Source unavailable
- Empty or malformed feeds
- Partial ingestion

---

## Stage 3: Filtering & Selection (Signal Over Noise)

- A local LLM (e.g., DeepSeek R1) evaluates the fetched articles.
- Articles are filtered based on:
  - relevance to technology
  - positive or hopeful impact
  - novelty (not previously covered)

- A coverage log is used to prevent repeating previously covered stories.

### Output
- A curated list of selected stories (typically 3–5 items).

### Failure considerations
- Model timeout
- Over-filtering (no stories selected)
- Under-filtering (too many stories)

Fallback logic is required.

---

## Stage 4: Summary Generation

- For each selected article:
  - A concise, factual summary is generated.
  - Focus areas:
    - what happened
    - why it matters
    - positive impact or future implication

- Summaries are stored as structured text.

### Failure considerations
- Hallucinated details
- Loss of context
- Overly verbose summaries

---

## Stage 5: Script Generation (Two-Narrator Format)

- A complete episode script is generated from the summaries.
- The script follows a **structured format**, not free-form dialogue:

  - Intro – Narrator A
  - For each story:
    - Headline – Narrator A
    - Explanation & context – Narrator B
  - Outro – Narrator A

### Output
- A structured script object (e.g., JSON) with explicit narrator assignments.

### Failure considerations
- Script length outside target bounds
- Tone inconsistency
- Formatting issues affecting TTS

---

## Stage 6: Text-to-Speech (Audio Generation)

- The script is converted into audio using a TTS engine.
- Two fixed voices are used:
  - Voice A: intro, headlines, outro
  - Voice B: explanations

- Audio segments are stitched into a single episode file.

### Storage
- Final audio file is uploaded to object storage (S3-compatible).
- Audio file location is recorded.

### Failure considerations
- TTS engine errors
- Partial audio generation
- Audio quality issues

---

## Stage 7: Persistence & Publishing

- A database entry is created or updated containing:
  - episode date
  - selected headlines
  - summaries
  - reference/source links
  - audio file URL
  - final status (`published` or `failed`)

- Once persisted, the episode is considered publicly available.

### Failure considerations
- Database write failures
- Audio exists but metadata is missing
- Inconsistent episode state

All states must be recoverable.

---

## Stage 8: Frontend Consumption

- The frontend accesses episode data via backend APIs.
- It displays:
  - episode date/title
  - list of stories
  - summaries
  - audio playback using the stored audio URL

### Explicit boundary
The frontend **never** interacts directly with:
- news sources
- LLMs
- TTS systems

---

## Storage Responsibilities

### Database
- Episode metadata
- Job run state
- Covered article references
- Error and failure logs

### Object Storage
- Final audio files
- (Optional) generated scripts for debugging or reprocessing

---

## Key Design Principles

- Each stage is independently rerunnable
- No stage assumes downstream success
- Failures are logged and visible
- The system prefers boring reliability over clever optimization
- Previous episodes can be regenerated safely without side effects

---

## Notes

This architecture is intentionally designed to:
- Support solo development
- Allow incremental delivery
- Reflect real-world production constraints
- Scale in complexity only when justified
