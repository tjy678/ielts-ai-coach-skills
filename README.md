# IELTS Study Coach

<p align="center">
  <strong>📊 AI-powered IELTS preparation system with a local Dashboard</strong><br>
  <sub>Writing · Reading · Listening · Speaking · Vocabulary · Mock Exams · Smart Analysis</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8%2B-green" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-brightgreen" alt="License">
  <img src="https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

---

## Overview

IELTS Study Coach is a comprehensive, AI-powered IELTS preparation system built on the [CodeBuddy](https://www.codebuddy.ai) Skill architecture.

> 🇨🇳 中文用户请参阅 [README_zh-CN.md](./README_zh-CN.md) It combines **10 specialized coaching modules** with a **local web-based Dashboard** for visualizing your study progress.

All data is stored **100% locally** — no cloud uploads, no account required.

### Key Features

- **📝 Writing Coach** — 4-dimension essay scoring (TR/CC/LR/GRA) with paragraph-level rewrites
- **📖 Reading Coach** — Synonym extraction, T/F/NG logic breakdown, error root-cause analysis
- **🎧 Listening Coach** — Error tracking by section, intensive listening tasks, trap identification
- **🗣️ Speaking Coach** — 5 universal stories covering 80% of Part 2 topics + Part 3 predictions
- **📚 Vocabulary Coach** — Spaced repetition system, synonym drills, topic vocabulary, spelling practice
- **📋 Mock Exam System** — Enter Cambridge test number, raw correct counts/estimated bands, and error Q#s after self-administered mock exams; auto band conversion + per-subject radar + error records
- **🔍 Smart Analysis** — AI matches exam answers to your error data (local answer bank first, web search fallback), generates per-question error diagnosis + writing scores
- **📊 Dashboard** — 7-tab visualization panel with radar charts, trend lines, bar charts, doughnut charts, heatmaps

---

## Table of Contents

- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Dashboard](#dashboard)
- [API Reference](#api-reference)
- [Data Format](#data-format)
- [Module Reference](#module-reference)
- [IELTS Scoring Guide](#ielts-scoring-guide)
- [Platform Compatibility](#platform-compatibility)
- [FAQ](#faq)
- [Changelog](#changelog)
- [License](#license)

---

## Screenshots

> The Dashboard features a dark-themed UI with 7 tabs: Overview, Writing, Reading, Listening, Speaking, Vocabulary, and Mock Exams. Charts are powered by Chart.js.

---

## Project Structure

```
.
├── index.html               # Dashboard single-page application
├── server.py                # Local HTTP server (port 8765) with API endpoints
├── README.md                # This file (English)
├── README_zh-CN.md          # Chinese documentation
├── .gitignore               # Excludes user data from version control
├── data/                    # Data storage directory
│   ├── profile.json         # User profile (target band, exam date, current level)
│   ├── progress.json        # 4-subject progress tracking
│   ├── history.json         # Activity history index (auto-rebuilt on startup)
│   ├── writing/
│   │   └── index.json       # Essay scoring records
│   ├── reading/
│   │   ├── index.json       # Reading analysis records
│   │   └── synonyms.json    # Accumulated synonym library
│   ├── listening/
│   │   ├── index.json       # Listening test records
│   │   └── errors.json      # Error logbook
│   ├── speaking/
│   │   ├── index.json       # Speaking practice records
│   │   └── stories.json     # Universal story library
│   ├── vocab/
│   │   ├── index.json       # Vocabulary learning records
│   │   ├── wordbank.json    # Word bank
│   │   └── review-log.json  # Spaced repetition review log
│   ├── exam/
│   │   └── index.json       # Mock exam history (scores, errors, essay data)
│   └── dashboard/
│       └── stats-cache.json # Dashboard cache
├── materials/               # Study materials folder (user-provided)
│   └── README.md            # Materials folder guide
├── analysis-reports/        # Exam analysis reports (Markdown)
│   └── README.md            # Reports folder guide
├── ielts/                   # Main entry: diagnostics, study plan, routing
├── ielts-writing/           # Writing Skill: 4-dimension scoring
├── ielts-reading/           # Reading Skill: error analysis
├── ielts-listening/         # Listening Skill: error tracking
├── ielts-speaking/          # Speaking Skill: story library
├── ielts-vocab/             # Vocabulary Skill: spaced repetition
├── ielts-dashboard/         # Dashboard Skill: visualization
├── ielts-exam/              # Exam Skill: result entry & evaluation
├── ielts-analysis/          # Analysis Skill: smart report generation
└── ielts-data/              # Data Skill: storage/backup/migration (internal)
```

---

## Quick Start

### Prerequisites

- **Python 3.8+** (standard library only, no pip install required)
- A modern web browser (Chrome, Firefox, Edge, Safari)

### 1. Start the Server

```bash
cd ielts-study-coach
python server.py
```

You will see:

```
  IELTS 备考 Dashboard 服务器已启动 (v1.0)
  ========================================
  地址: http://localhost:8765/index.html
  ...
```

### 2. Open the Dashboard

Navigate to **http://localhost:8765/index.html** in your browser.

> ⚠️ **Do not double-click index.html directly.** The Dashboard uses `fetch()` to load JSON data, which requires HTTP protocol. `file://` protocol will be blocked by CORS.

### 3. Connect with CodeBuddy Skills

Install the Skill definition files into your CodeBuddy `skills/` directory, then trigger any module via chat:

| You say | What happens |
|---------|-------------|
| `我要备考雅思` | Diagnostic assessment + study plan |
| `批改作文` + paste essay | Writing: 4-dimension scoring |
| `分析阅读` + paste questions | Reading: error analysis |
| `听力错题` + error details | Listening: root cause analysis |
| `口语素材 Part 2` | Speaking: generate story |
| `背单词` | Vocabulary: spaced repetition |
| `模考` | Mock exam: enter results |
| `智能解读 exam-id` | Smart analysis: full report |

---

## Dashboard

### Tabs Overview

| Tab | Content |
|-----|---------|
| **Overview** | Score cards, estimated overall band, radar chart, trend chart, recent activity |
| **Writing** | Score trend, 4-dimension radar, recent essay history, common deduction items |
| **Reading** | Accuracy trend, question type doughnut chart, recent reading records, error history |
| **Listening** | Accuracy trend (by Section), Section 1-4 comparison bar chart, recent listening records, error history |
| **Speaking** | Self-rating trend, 4-dimension radar, Part 2 topic coverage progress, recent practice records |
| **Vocabulary** | Word growth, review accuracy trend, level distribution, review queue |
| **Mock Exam** | Result entry form (Cambridge #/Test #/date/scores/error Q#s), exam stats (count/best/average), overall trend, per-subject radar, per-subject score changes, exam history, error records, analysis report management |

### Tech Stack

- **Frontend**: Pure HTML/CSS/JavaScript single-page application
- **Charts**: [Chart.js 4.4](https://www.chartjs.org/) (CDN loaded)
- **Backend**: Python `http.server` with custom API endpoints
- **Storage**: Local JSON files + `localStorage` cache
- **Theme**: Dark mode, responsive design

---

## API Reference

`server.py` provides the following endpoints on port 8765:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/save` | POST | Persist JSON data to `data/` directory |
| `/api/analysis/save` | POST | Save analysis report as Markdown file |
| `/api/analysis/save-report` | POST | AI backfill: save report + update exam status |
| `/api/analysis/list` | POST | List all saved analysis reports |
| `/api/analysis/delete` | POST | Delete a specific analysis report |
| `/api/writing/save-score` | POST | AI backfill: writing scores + update index + progress |

### Example: Save Data

```bash
curl -X POST http://localhost:8765/api/save \
  -H "Content-Type: application/json" \
  -d '{"path": "data/profile.json", "data": {"targetBand": 7.0}}'
```

### Security

- All write endpoints validate paths to ensure they stay within `data/` or `analysis-reports/`
- Filenames are sanitized to prevent path traversal attacks
- CORS headers are set for local development

---

## ⚠️ Important Notice

- **This repository does NOT contain any Cambridge IELTS test content** (including but not limited to original passages, audio recordings, questions, or official answer keys)
- Smart Analysis uses local answer bank (`data/known-answers.json`) first, falling back to AI + public internet resources for unlisted tests
- The Dashboard's built-in report generator supports local answer data, added at your discretion
- This project only provides the study tool framework and is not responsible for user-added data content
- All data is stored 100% locally — nothing is uploaded to any server

---

## Data Format

### Exam Record (`data/exam/index.json`)

```json
{
  "exams": [{
    "id": "exam-1782024625616",
    "timestamp": "2026-06-21T04:00:00.000Z",
    "type": "full",
    "source": "Cambridge 15 Test 2",
    "scores": {
      "listening": 6.5, "reading": 6.0,
      "writing": 5.5, "speaking": 5.0,
      "overall": 5.8
    },
    "rawCorrect": { "listening": 26, "reading": 23 },
    "errorDetails": {
      "listening": { "section1": [], "section2": [13,14,19], ... },
      "reading": { "passage1": [1,3,5], ... }
    },
    "essayData": {
      "task1": { "text": "...", "scores": {...}, "aiScored": true },
      "task2": { "text": "...", "scores": {...}, "aiScored": true }
    },
    "writingStatus": "scored",
    "analysisStatus": "scored",
    "analysisReport": "analysis-reports/exam-c15-test2-20260621-v2.md"
  }],
  "stats": {
    "totalExams": 1,
    "bestOverall": 6.5,
    "averageOverall": 5.8,
    "lastExamDate": "2026-06-21T04:00:00.000Z"
  }
}
```

### Writing Score Format

```json
{
  "id": "exam-xxx-task1",
  "taskType": "task1",
  "scores": {
    "tr": 6.0,     // Task Response / Achievement
    "cc": 6.5,     // Coherence & Cohesion
    "lr": 5.5,     // Lexical Resource
    "gra": 6.0,    // Grammatical Range & Accuracy
    "overall": 6.0
  }
}
```

### Data Consistency

- On Dashboard startup, `syncProgressFromExams()` rebuilds all module indexes from `exam/index.json`
- Data is read from disk JSON first (`forceReload=true`), bypassing localStorage cache
- `history.json` is always in sync with exam records

---

## Module Reference

### ielts (Main Entry)
Diagnostic assessment (5 questions) → personalized study plan → module routing.

**Triggers**: `我要备考雅思`, `IELTS`, `重新摸底`

### ielts-writing (Writing Coach)
4-dimension scoring: TR/TA, CC, LR, GRA (25% each). Paragraph-level analysis with rewrites.

**Triggers**: `批改作文`, `帮我看看这篇`, `写作`, `Task 1`, `Task 2`

### ielts-reading (Reading Coach)
Synonym extraction, T/F/NG logic breakdown, passage structure analysis, error classification.

**Error types**: synonym missed, location error, NG misjudgment, over-inference, keyword deviation

**Triggers**: `分析阅读`, `这道为什么错`, `同义替换`, `T/F/NG`

### ielts-listening (Listening Coach)
Error tracking by section (S1-S4), intensive listening task generation, trap identification.

**Error types**: spelling, synonym missed, distracted by distractors, lost track, prediction error, focus lapse, word limit ignored

**Triggers**: `听力错题`, `精听`, `听力`, `Section`

### ielts-speaking (Speaking Coach)
5 universal stories covering ~50 Part 2 topics. Topic matching, 2-minute material generation, Part 3 predictions.

**Triggers**: `口语素材`, `Part 2`, `话题分组`, `万能故事`, `口语`

### ielts-vocab (Vocabulary Coach)
Spaced repetition with 7 levels (0 → Mastered). 4 training modes: SRS review, synonym drills, topic vocabulary, spelling practice.

**Triggers**: `背单词`, `同义替换训练`, `词汇`, `vocab`

### ielts-exam (Mock Exam)
After self-administered mock exams, enter Cambridge test number, raw correct counts/estimated bands, and error Q#s in the Dashboard's Exam tab. Auto band conversion, overall score calculation, and history tracking. Dashboard shows overall trend, per-subject radar, and per-subject score changes.

**Triggers**: `模考`, `录入模考`, `估分`, `模考评估`

### ielts-analysis (Smart Analysis)
Reads pending exam records, checks local answer bank (`data/known-answers.json`) first, falls back to public internet resources for unlisted tests. Generates per-question error analysis + weakness diagnosis + improvement recommendations. Async backfill to Dashboard via API.

**Triggers**: `智能解读`, `模考解读`, `分析模考`, `模考报告`

### ielts-dashboard (Dashboard Skill)
Triggers the visualization Skill that generates a single-file HTML Dashboard with radar charts, trend lines, bar charts, doughnut charts, and error heatmaps.

**Triggers**: `看进度`, `Dashboard`, `我的数据`, `统计`, `趋势`

### ielts-data (Data Layer)
Internal module for data I/O, backup, restore, and migration.

---

## IELTS Scoring Guide

### Overall Band Calculation

```
Overall = Average of 4 subjects, rounded to nearest 0.5
.25 and .75 round up (e.g., 7.25 → 7.5, 6.75 → 7.0)
```

### Listening & Reading Band Conversion (Academic)

| Band | Listening (/40) | Reading (/40) |
|------|-----------------|---------------|
| 9.0 | 39-40 | 39-40 |
| 8.5 | 37-38 | 37-38 |
| 8.0 | 35-36 | 35-36 |
| 7.5 | 32-34 | 33-34 |
| 7.0 | 30-31 | 30-32 |
| 6.5 | 26-29 | 27-29 |
| 6.0 | 23-25 | 23-26 |
| 5.5 | 18-22 | 19-22 |
| 5.0 | 16-17 | 15-18 |

### Writing Dimensions

**Task 1**: TA (Task Achievement) · CC · LR · GRA
**Task 2**: TR (Task Response) · CC · LR · GRA

### Study Strategy

| Time to exam | Phase | Focus |
|-------------|-------|-------|
| > 3 months | Foundation | Vocabulary, grammar, familiarize with question types |
| 1-3 months | Intensive | Practice tests, techniques, error analysis |
| 2-4 weeks | Sprint | Mock exams, weakness targeting, time management |
| < 2 weeks | Final | Maintain momentum, essay templates, high-frequency speaking |

---

## Platform Compatibility

| Platform | Status | Notes |
|----------|--------|-------|
| **Windows** | ✅ Fully supported | Tested on Windows 10/11 with Python 3.8+ |
| **macOS** | ✅ Fully supported | Tested on macOS 12+ with built-in Python 3 |
| **Linux** | ✅ Fully supported | Tested on Ubuntu 20.04+ with Python 3.8+ |

### Compatibility Notes

- **Python**: Uses only standard library modules (`http.server`, `socketserver`, `os`, `json`, `urllib.parse`, `re`). No `pip install` needed.
- **Paths**: All file paths use `os.path.join()` and `os.path.normpath()` for cross-platform compatibility.
- **Encoding**: All JSON files use UTF-8 encoding with `ensure_ascii=False`.
- **Server**: `allow_reuse_address = True` is set for quick restarts across all platforms.
- **Browser**: Works in any modern browser (Chrome, Firefox, Edge, Safari). Chart.js is loaded from CDN.
- **Line endings**: `.gitignore` handles cross-platform line ending differences.

---

## FAQ

### Q: Where is my data stored? Is it safe?
All data is stored in the `data/` directory as local JSON files. Nothing is uploaded to any cloud service. You can copy, backup, or delete the entire directory at any time.

### Q: Why can't I just double-click index.html?
The Dashboard uses `fetch()` to load JSON data files, which requires HTTP protocol. Open it via `http://localhost:8765/index.html` after starting `python server.py`.

### Q: Charts aren't showing?
Chart.js is loaded from CDN and requires internet access on first load. If offline, data cards and lists still work; only charts will be blank.

### Q: How do I backup my data?
Copy the entire project directory. All data, configuration, and Dashboard files are self-contained.

### Q: How do I migrate to another computer?
Copy the entire project directory to the new computer. No installation or configuration needed.

### Q: How do I reset everything?
Say `重新摸底` in chat, or manually replace the JSON files in `data/` with the empty templates from the repository.

### Q: Why is the `materials/` directory mostly empty?
Study materials (Cambridge PDFs, vocabulary lists, sample essays, etc.) are copyrighted and must be provided by you.

### Q: Can I contribute?
Yes! Pull requests are welcome. Please see the [License](#license) section for details.

---

## Changelog

### v1.0.0 (2026-06-21) — First Stable Release

**Bug Fixes:**
- Unified IELTS rounding logic across all score calculation functions
- Fixed unrecorded subjects pulling down overall average (now excludes null/zero scores)
- Fixed ghost entries in `history.json` (now auto-rebuilt on startup)
- Fixed `syncProgressFromExams` using stale localStorage cache (now `forceReload=true`)
- Fixed unsorted exam array causing incorrect "latest exam" selection
- Fixed inconsistent field names in `listening/index.json` and `reading/index.json`

**Improvements:**
- Unified writing score format to `{tr, cc, lr, gra, overall}` across all code paths
- Added `DELETE /api/analysis/delete` endpoint for report management
- Added `allow_reuse_address` for cross-platform server restart compatibility
- Improved cross-platform path handling

**Cleanup:**
- Removed unused functions: `loadJSONSync()`, `buildReportPreview()`, `updateAnalyzeButton()`
- Removed duplicate/outdated analysis reports
- Cleaned `history.json` from 3 ghost records to 1 valid record

---

## License

[MIT License](https://opensource.org/licenses/MIT)

Copyright (c) 2026 tjy678

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

<p align="center">
  <sub>Made with ❤️ for IELTS test takers worldwide</sub>
</p>
