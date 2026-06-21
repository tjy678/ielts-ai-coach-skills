# IELTS 备考 AI 教练skills

<p align="center">
  <strong>📊 基于 AI 的雅思备考skills，配备本地可视化 Dashboard</strong><br>
  <sub>写作 · 阅读 · 听力 · 口语 · 词汇 · 模考 · 智能解读</sub>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/版本-1.0.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8%2B-green" alt="Python">
  <img src="https://img.shields.io/badge/许可证-MIT-brightgreen" alt="License">
  <img src="https://img.shields.io/badge/平台-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey" alt="Platform">
</p>

---

## 概述

IELTS 备考 AI 教练skills是一个基于 [CodeBuddy](https://www.codebuddy.ai) Skill 架构的全方位雅思备考工具。它整合了 **10 个专项训练模块** 和一个 **本地 Web Dashboard**，帮助你可视化追踪备考进度。

所有数据 **100% 本地存储** —— 无需上传云端，无需注册账号。

### 核心功能

- **📝 写作教练** —— 四维评分（TR/CC/LR/GRA）+ 逐段改写对比
- **📖 阅读教练** —— 同义替换提取 + T/F/NG 逻辑拆解 + 错因分析
- **🎧 听力教练** —— 按 Section 追踪错题 + 精听任务 + 陷阱识别
- **🗣️ 口语教练** —— 5 个万能故事覆盖 80% Part 2 话题 + Part 3 预测
- **📚 词汇教练** —— 间隔重复系统 + 同义替换训练 + 话题词汇 + 拼写训练
- **📋 模考系统** —— 模考后录入剑桥真题编号、各科正确数/估分、错题号，自动换算 Band + 各科雷达图 + 错题记录
- **🔍 智能解读** —— AI 根据你录入的错题号匹配真题答案（优先本地答案库，未收录则联网检索），生成逐题错因诊断 + 写作评分
- **📊 Dashboard** —— 7 个标签页可视化面板，雷达图/趋势图/柱状图/环形图/热力图

---

## 目录

- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [Dashboard](#dashboard)
- [API 参考](#api-参考)
- [数据格式](#数据格式)
- [模块说明](#模块说明)
- [雅思评分对照](#雅思评分对照)
- [平台兼容性](#平台兼容性)
- [常见问题](#常见问题)
- [更新日志](#更新日志)
- [许可证](#许可证)

---

## 项目结构

```
.
├── index.html               # Dashboard 单页应用
├── server.py                # 本地 HTTP 服务器（端口 8765，含 API 端点）
├── README.md                # 英文说明文档
├── README_zh-CN.md          # 本文件（中文说明文档）
├── .gitignore               # 版本控制忽略规则
├── data/                    # 数据存储目录
│   ├── profile.json         # 用户档案（目标分、考试日期、当前水平）
│   ├── progress.json        # 四科进度追踪
│   ├── history.json         # 活动历史索引（启动时自动重建）
│   ├── writing/
│   │   └── index.json       # 写作批改记录
│   ├── reading/
│   │   ├── index.json       # 阅读分析记录
│   │   └── synonyms.json    # 同义替换累计库
│   ├── listening/
│   │   ├── index.json       # 听力测试记录
│   │   └── errors.json      # 错题本
│   ├── speaking/
│   │   ├── index.json       # 口语练习记录
│   │   └── stories.json     # 万能故事库
│   ├── vocab/
│   │   ├── index.json       # 词汇学习记录
│   │   ├── wordbank.json    # 生词库
│   │   └── review-log.json  # 间隔重复复习日志
│   ├── exam/
│   │   └── index.json       # 模考历史（含分数、错题、作文数据）
│   └── dashboard/
│       └── stats-cache.json # Dashboard 缓存
├── materials/               # 备考资料文件夹（用户自行放入）
│   └── README.md            # 资料文件夹说明
├── analysis-reports/        # 模考智能解读报告（Markdown）
│   └── README.md            # 报告文件夹说明
├── ielts/                   # 主入口：摸底诊断、备考计划、模块路由
├── ielts-writing/           # 写作 Skill：四维评分批改
├── ielts-reading/           # 阅读 Skill：错题诊断分析
├── ielts-listening/         # 听力 Skill：错题追踪
├── ielts-speaking/          # 口语 Skill：故事素材库
├── ielts-vocab/             # 词汇 Skill：间隔重复
├── ielts-dashboard/         # Dashboard Skill：可视化面板
├── ielts-exam/              # 模考 Skill：模考结果录入与评估
├── ielts-analysis/          # 解读 Skill：智能报告生成
└── ielts-data/              # 数据 Skill：存储/备份/迁移（内部模块）
```

---

## 快速开始

### 环境要求

- **Python 3.8+**（仅使用标准库，无需 pip 安装任何依赖）
- 现代浏览器（Chrome、Firefox、Edge、Safari）

### 1. 启动服务器

```bash
cd ielts-study-coach
python server.py
```

你将看到：

```
  IELTS 备考 Dashboard 服务器已启动 (v1.0)
  ========================================
  地址: http://localhost:8765/index.html
  ...
```

### 2. 打开 Dashboard

在浏览器中访问 **http://localhost:8765/index.html**。

> ⚠️ **不要直接双击 index.html 文件。** Dashboard 通过 `fetch()` 加载 JSON 数据，需要 HTTP 协议。`file://` 协议会被 CORS 拦截。

### 3. 配合 CodeBuddy Skills 使用

将 Skill 定义文件安装到 CodeBuddy 的 `skills/` 目录下，然后在对话中触发相应模块：

| 你说的话 | 触发功能 |
|---------|---------|
| `我要备考雅思` | 摸底诊断 + 备考计划 |
| `批改作文` + 粘贴文章 | 写作：四维评分 |
| `分析阅读` + 粘贴题目 | 阅读：错题分析 |
| `听力错题` + 错误详情 | 听力：根因分析 |
| `口语素材 Part 2` | 口语：生成故事素材 |
| `背单词` | 词汇：间隔重复训练 |
| `模考` | 模考：录入模考结果 |
| `智能解读 exam-id` | 智能解读：完整分析报告 |

---

## Dashboard

### 标签页概览

| 标签页 | 内容 |
|--------|------|
| **总览** | 四科分数卡片、预估总分、雷达图、四科走势图、最近活动 |
| **写作** | 分数走势、四维雷达图、最近批改记录、高频扣分项 |
| **阅读** | 正确率走势、错题题型分布环形图、最近阅读记录、错题历史 |
| **听力** | 正确率走势（按 Section）、Section 1-4 对比柱状图、最近听力记录、错题历史 |
| **口语** | 自评走势、四维雷达图、Part 2 话题覆盖进度、最近练习记录 |
| **词汇** | 词汇量增长、复习正确率走势、各等级分布、待复习队列 |
| **模考** | 模考结果录入表单（剑桥编号/Test/日期/各科分数/错题号）、模考统计（次数/最高/均分）、总分走势、四科雷达图、四科分数变化图、模考历史记录、错题记录、解读报告管理 |

### 技术栈

- **前端**：纯 HTML/CSS/JavaScript 单页应用
- **图表**：[Chart.js 4.4](https://www.chartjs.org/)（CDN 加载）
- **后端**：Python `http.server` + 自定义 API 端点
- **存储**：本地 JSON 文件 + `localStorage` 缓存
- **主题**：深色模式，响应式设计

---

## API 参考

`server.py` 在 8765 端口提供以下 API 端点：

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/save` | POST | 持久化 JSON 数据到 `data/` 目录 |
| `/api/analysis/save` | POST | 保存解读报告 Markdown 文件 |
| `/api/analysis/save-report` | POST | AI 回填：保存报告 + 更新模考状态 |
| `/api/analysis/list` | POST | 列出所有已保存的解读报告 |
| `/api/analysis/delete` | POST | 删除指定解读报告文件 |
| `/api/writing/save-score` | POST | AI 回填：写作四维评分 + 更新索引 + 进度 |

### 示例：保存数据

```bash
curl -X POST http://localhost:8765/api/save \
  -H "Content-Type: application/json" \
  -d '{"path": "data/profile.json", "data": {"targetBand": 7.0}}'
```

### 安全性

- 所有写入端点会验证路径，确保操作仅限于 `data/` 或 `analysis-reports/` 目录
- 文件名经过清理以防止路径遍历攻击
- 设置了 CORS 头以支持本地开发

---

## ⚠️ 重要声明

- **本仓库不包含任何剑桥雅思真题内容**（包括但不限于真题原文、录音、题目、标准答案等）
- 智能解读优先使用本地答案库（`data/known-answers.json`），未收录的试卷通过 AI + 互联网公开资源检索真题信息
- Dashboard 内置的报告生成功能支持本地答案数据，由用户自行添加
- 本项目仅提供备考工具框架，不对用户自行添加的数据内容负责
- 所有数据 100% 本地存储，不上传任何服务器

---

## 数据格式

### 模考记录 (`data/exam/index.json`)

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

### 写作评分格式

```json
{
  "id": "exam-xxx-task1",
  "taskType": "task1",
  "scores": {
    "tr": 6.0,     // Task Response（任务回应）/ Task Achievement（任务完成度）
    "cc": 6.5,     // Coherence & Cohesion（连贯与衔接）
    "lr": 5.5,     // Lexical Resource（词汇资源）
    "gra": 6.0,    // Grammatical Range & Accuracy（语法范围与准确度）
    "overall": 6.0
  }
}
```

### 数据一致性

- Dashboard 启动时，`syncProgressFromExams()` 会从 `exam/index.json` 全量重建所有模块索引
- 数据优先从磁盘 JSON 读取（`forceReload=true`），绕过 localStorage 缓存确保一致性
- `history.json` 始终与模考记录保持同步

---

## 模块说明

### ielts（主入口）
摸底诊断（5 个问题）→ 个性化备考计划 → 模块路由分发。

**触发词**：`我要备考雅思`、`IELTS`、`重新摸底`

### ielts-writing（写作教练）
四维评分：TR/TA、CC、LR、GRA（各占 25%）。逐段分析与改写建议。

**触发词**：`批改作文`、`帮我看看这篇`、`写作`、`Task 1`、`Task 2`

### ielts-reading（阅读教练）
同义替换提取、T/F/NG 逻辑拆解、段落结构分析、错题分类诊断。

**错因类型**：未识别同义替换、定位错误、NG 误判、过度推断、关键词偏差

**触发词**：`分析阅读`、`这道为什么错`、`同义替换`、`T/F/NG`

### ielts-listening（听力教练）
按 Section（S1-S4）追踪错题、生成精听任务、识别高频陷阱。

**错因类型**：拼写错误、未识别同义替换、被干扰项迷惑、跟丢、预测错误、走神、忽略字数限制

**触发词**：`听力错题`、`精听`、`听力`、`Section`

### ielts-speaking（口语教练）
5 个万能故事覆盖约 50 个 Part 2 话题。话题匹配、2 分钟素材生成、Part 3 预测。

**触发词**：`口语素材`、`Part 2`、`话题分组`、`万能故事`、`口语`

### ielts-vocab（词汇教练）
7 级间隔重复系统（0 → 已掌握）。4 种训练模式：间隔重复、同义替换训练、话题词汇、拼写训练。

**触发词**：`背单词`、`同义替换训练`、`词汇`、`vocab`

### ielts-exam（模考系统）
考生自行用真题模考后，在 Dashboard 模考页录入剑桥真题编号、各科正确数/估分、错题号。自动换算 Band、计算总分、追踪历史。Dashboard 展示总分走势、四科雷达图、四科分数变化图。

**触发词**：`模考`、`录入模考`、`估分`、`模考评估`

### ielts-analysis（智能解读）
读取待解读模考记录，优先匹配本地答案库（`data/known-answers.json`），未收录则通过互联网公开资源检索真题答案，生成逐题错因分析 + 能力短板诊断 + 提分建议报告，通过 API 异步回填到 Dashboard。

**触发词**：`智能解读`、`模考解读`、`分析模考`、`模考报告`

### ielts-dashboard（Dashboard Skill）
触发可视化 Skill，生成包含雷达图/趋势图/柱状图/环形图/错题热力图的单文件 HTML Dashboard。

**触发词**：`看进度`、`Dashboard`、`我的数据`、`统计`、`趋势`

### ielts-data（数据层）
内部模块，负责数据读写、备份、恢复和迁移。

---

## 雅思评分对照

### 总分计算规则

```
总分 = 四科平均分，取最近的 0.5 档
.25 和 .75 向上取整（例：7.25 → 7.5，6.75 → 7.0）
```

### 听力 & 阅读分数换算（学术类）

| 分数 | 听力 (/40) | 阅读 (/40) |
|------|-----------|-----------|
| 9.0 | 39-40 | 39-40 |
| 8.5 | 37-38 | 37-38 |
| 8.0 | 35-36 | 35-36 |
| 7.5 | 32-34 | 33-34 |
| 7.0 | 30-31 | 30-32 |
| 6.5 | 26-29 | 27-29 |
| 6.0 | 23-25 | 23-26 |
| 5.5 | 18-22 | 19-22 |
| 5.0 | 16-17 | 15-18 |

### 写作评分维度

**Task 1**：TA（任务完成度）· CC · LR · GRA
**Task 2**：TR（任务回应）· CC · LR · GRA

### 备考策略

| 距考试时间 | 阶段 | 重点 |
|-----------|------|------|
| > 3 个月 | 基础阶段 | 词汇、语法、熟悉题型 |
| 1-3 个月 | 强化阶段 | 真题练习、技巧训练、错题分析 |
| 2-4 周 | 冲刺阶段 | 模考、薄弱项突破、时间管理 |
| < 2 周 | 最后阶段 | 保持状态、作文模板、高频口语 |

---

## 平台兼容性

| 平台 | 状态 | 说明 |
|------|------|------|
| **Windows** | ✅ 完全支持 | 在 Windows 10/11 + Python 3.8+ 上测试通过 |
| **macOS** | ✅ 完全支持 | 在 macOS 12+ + 系统自带 Python 3 上测试通过 |
| **Linux** | ✅ 完全支持 | 在 Ubuntu 20.04+ + Python 3.8+ 上测试通过 |

### 兼容性说明

- **Python**：仅使用标准库模块（`http.server`、`socketserver`、`os`、`json`、`urllib.parse`、`re`）。无需 pip 安装任何依赖。
- **路径处理**：所有文件路径使用 `os.path.join()` 和 `os.path.normpath()`，确保跨平台兼容。
- **编码**：所有 JSON 文件使用 UTF-8 编码，`ensure_ascii=False`。
- **服务器**：设置 `allow_reuse_address = True`，支持各平台快速重启。
- **浏览器**：兼容所有现代浏览器（Chrome、Firefox、Edge、Safari）。Chart.js 通过 CDN 加载。
- **换行符**：`.gitignore` 已处理跨平台换行符差异。

---

## 常见问题

### Q: 我的数据存在哪里？安全吗？
所有数据存储在 `data/` 目录中，以本地 JSON 文件形式保存。不会上传到任何云端服务。你可以随时复制、备份或删除整个目录。

### Q: 为什么不能直接双击 index.html？
Dashboard 使用 `fetch()` 加载 JSON 数据文件，这需要 HTTP 协议。请先运行 `python server.py`，然后通过 `http://localhost:8765/index.html` 访问。

### Q: 图表不显示怎么办？
Chart.js 通过 CDN 加载，首次使用需要联网。离线时数据卡片和列表仍然可用，仅图表部分会显示为空白。

### Q: 如何备份数据？
直接复制整个项目目录即可。所有数据、配置和 Dashboard 文件都是自包含的。

### Q: 如何迁移到另一台电脑？
将整个项目目录复制到新电脑。无需安装或配置。

### Q: 如何重置所有数据？
在对话中说 `重新摸底`，或者手动将 `data/` 目录中的 JSON 文件替换为仓库中的空模板。

### Q: 为什么 `materials/` 目录基本是空的？
备考资料（剑桥真题 PDF、词汇表、范文等）受版权保护，需要由用户自行提供。

### Q: 我可以参与贡献吗？
当然可以！欢迎提交 Pull Request。详情请参阅[许可证](#许可证)部分。

---

## 更新日志

### v1.0.0 (2026-06-21) — 首个稳定版本

**Bug 修复：**
- 统一所有分数计算函数中的雅思舍入逻辑
- 修复未录入科目以 0 分拉低总分的缺陷（现仅对有分数的科目求平均）
- 修复 `history.json` 幽灵数据问题（现启动时自动重建）
- 修复 `syncProgressFromExams` 使用过期 localStorage 缓存的问题（现改为 `forceReload=true`）
- 修复模考数组未排序导致"最新模考"选择错误
- 修复 `listening/index.json` 和 `reading/index.json` 字段名称不一致

**功能改进：**
- 所有代码路径统一写作评分格式为 `{tr, cc, lr, gra, overall}`
- 新增 `DELETE /api/analysis/delete` 端点，支持报告管理
- 新增 `allow_reuse_address`，支持各平台服务器快速重启
- 优化跨平台路径处理

---

## 许可证

[MIT License](https://opensource.org/licenses/MIT)

版权所有 (c) 2026 tjy678

特此授予任何人免费获取本软件及相关文档文件（"软件"）副本的权利，允许其不受限制地使用、复制、修改、合并、发布、分发、再许可和/或销售软件副本，并允许向其提供软件的人这样做，但须符合以下条件：

上述版权声明和本许可声明应包含在软件的所有副本或实质性部分中。

本软件按"原样"提供，不作任何明示或暗示的保证，包括但不限于对适销性、特定用途适用性和非侵权的保证。在任何情况下，作者或版权持有人均不对因软件或软件的使用或其他交易中产生的任何索赔、损害或其他责任承担责任，无论是合同、侵权还是其他行为。

---

<p align="center">
  <sub>为中国雅思考生而制作 ❤️</sub>
</p>
