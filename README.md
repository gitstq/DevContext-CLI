# 🧠 DevContext-CLI

<div align="center">

**Intelligent Developer Context Extraction Engine for AI Assistants**

[English](#english) | [简体中文](#simplified-chinese) | [繁體中文](#traditional-chinese)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)](requirements.txt)
[![Tests](https://img.shields.io/badge/Tests-15%2F15%20Passing-success)](tests/)

</div>

---

## <a name="english"></a> 🇺🇸 English

### 🎉 Introduction

**DevContext-CLI** is a zero-dependency command-line tool that intelligently extracts your project's context for AI coding assistants like **Claude Code**, **Cursor**, **GitHub Copilot**, and **Windsurf**.

**Problem it solves:** When asking AI assistants to help with your code, you often need to copy-paste multiple files manually — which is tedious, error-prone, and frequently exceeds the AI's token limit. DevContext-CLI automates this entire process.

**Key differentiators:**
- 🧠 **Smart filtering** — Automatically identifies key files, excludes build artifacts and dependencies
- 💰 **Token budget management** — Real-time token estimation with automatic truncation
- 📋 **Multiple output formats** — Markdown, XML, and JSON to match different AI assistants' preferences
- 🌳 **Directory tree generation** — Complete project structure at a glance
- ⚡ **Zero dependencies** — Pure Python standard library, works everywhere

**Inspiration:** Born from the daily frustration of manually preparing project context for AI assistants, combined with insights from trending projects like `microsoft/markitdown` (document conversion) and the growing need for efficient AI context management.

---

### ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Intelligent File Discovery** | Auto-detects important files (README, configs, source code) while ignoring build artifacts, dependencies, and media files |
| 💰 **Token Budget Control** | Set a token limit (`-b 8000`) and the tool automatically includes files until the budget is reached |
| 📋 **Multi-Format Output** | **Markdown** (default), **XML**, and **JSON** formats for different AI assistant workflows |
| 🌳 **ASCII Directory Tree** | Beautiful tree view of your project structure, automatically filtered |
| 🔧 **.gitignore Respect** | Automatically follows `.gitignore` rules (can be disabled with `--no-gitignore`) |
| 🎯 **Include/Exclude Patterns** | Fine-grained control with glob patterns (`-i "*.test.js" --include "*.py"`) |
| 📦 **File Size Limits** | Skip oversized files automatically (default: 1MB, configurable) |
| 🌍 **CJK Token Estimation** | Accurate token counting for both ASCII (~4 chars/token) and CJK text (1 char/token) |

---

### 🚀 Quick Start

#### Requirements
- Python **3.8** or higher
- No external dependencies required

#### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/DevContext-CLI.git
cd DevContext-CLI

# Option 1: Run directly
python3 devcontext.py /path/to/your/project

# Option 2: Install as a command
pip install -e .
devcontext /path/to/your/project
```

#### Basic Usage

```bash
# Extract current directory context
devcontext

# Extract specific project
devcontext /path/to/project

# Save to file
devcontext -o context.md

# Limit to ~8000 tokens (e.g., for Claude's context window)
devcontext -b 8000 -o context.md

# Output as XML (great for structured parsing)
devcontext -f xml -o context.xml

# Only include Python files
devcontext --include "*.py" -o python_context.md

# Ignore test files and docs
devcontext -i "*test*" -i "docs/*" -o context.md
```

---

### 📖 Detailed Usage Guide

#### Command-Line Options

```
usage: devcontext [-h] [-o FILE] [-f {markdown,xml,json}] [-b TOKENS]
                  [-i PATTERN] [--include PATTERN] [--max-size BYTES]
                  [--no-gitignore] [-v] [--tree-only]
                  [path]

positional arguments:
  path                  Project path to analyze (default: current directory)

options:
  -h, --help            Show help message
  -o FILE, --output FILE
                        Output file path (default: stdout)
  -f {markdown,xml,json}, --format {markdown,xml,json}
                        Output format (default: markdown)
  -b TOKENS, --budget TOKENS
                        Token budget limit (approximate)
  -i PATTERN, --ignore PATTERN
                        Additional ignore patterns (repeatable)
  --include PATTERN     Only include matching patterns (repeatable)
  --max-size BYTES      Max file size in bytes (default: 1MB)
  --no-gitignore        Ignore .gitignore rules
  -v, --version         Show version
  --tree-only           Only output directory tree
```

#### Typical Workflows

**For Claude Code / Claude Desktop:**
```bash
# Claude works great with Markdown
devcontext -b 100000 -o context.md
# Then copy-paste the content into your Claude conversation
```

**For Cursor AI:**
```bash
# Cursor also prefers Markdown
devcontext --include "*.py" --include "*.js" -b 8000 -o cursor_context.md
```

**For API-based workflows:**
```bash
# JSON format for programmatic processing
devcontext -f json -b 4000 -o context.json
```

**For CI/CD pipelines:**
```bash
# XML format for structured parsing
devcontext -f xml --no-gitignore -o project_context.xml
```

---

### 💡 Design Philosophy & Roadmap

**Design Principles:**
1. **Zero dependencies** — Should work on any Python installation without `pip install`
2. **Batteries included** — Smart defaults that work out of the box for 90% of projects
3. **AI-first** — Every feature is designed with AI assistant workflows in mind
4. **Transparent** — Clear token counts, file inclusion/exclusion visibility

**Technology Choices:**
- **Python 3.8+**: Maximum compatibility across systems
- **Standard library only**: No dependency hell, instant execution
- **Pathlib**: Modern, cross-platform path handling
- **fnmatch**: Unix shell-style wildcards for familiar pattern matching

**Future Roadmap:**
- [ ] Interactive TUI mode with file selection
- [ ] Git diff integration (only changed files)
- [ ] Custom template system for output formatting
- [ ] Configuration file support (`.devcontextrc`)
- [ ] Watch mode for real-time context updates
- [ ] Integration with popular AI assistant APIs

---

### 📦 Packaging & Deployment

This is a **CLI tool/library** — no executable packaging required.

**Distribution:**
```bash
# Install from source
pip install -e .

# Or run directly without installation
python3 devcontext.py [options]
```

**Compatibility:**
- ✅ Linux (all distributions)
- ✅ macOS (Intel & Apple Silicon)
- ✅ Windows (via Python)
- ✅ WSL

---

### 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. Create a **feature branch** (`git checkout -b feat/amazing-feature`)
3. **Commit** with clear messages following [Conventional Commits](https://conventionalcommits.org/)
4. **Push** to your fork
5. Open a **Pull Request**

**Commit message format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test additions/changes

**Issue reporting:**
- Use GitHub Issues for bug reports and feature requests
- Include Python version, OS, and reproduction steps

---

### 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## <a name="simplified-chinese"></a> 🇨🇳 简体中文

### 🎉 项目介绍

**DevContext-CLI** 是一款零依赖的命令行工具，专为 **Claude Code**、**Cursor**、**GitHub Copilot**、**Windsurf** 等 AI 编程助手智能提取项目上下文。

**解决的核心痛点：** 向 AI 助手求助时，手动复制粘贴多个文件既繁琐又容易出错，还常常超出 AI 的 token 限制。DevContext-CLI 将整个流程自动化。

**自研差异化亮点：**
- 🧠 **智能文件筛选** — 自动识别关键文件，排除构建产物和依赖
- 💰 **Token 预算管理** — 实时估算 token 数量，超预算自动截断
- 📋 **多格式输出** — Markdown、XML、JSON，适配不同 AI 助手偏好
- 🌳 **目录树生成** — 一目了然的项目结构视图
- ⚡ **完全零依赖** — 纯 Python 标准库，随处可用

**灵感来源：** 源于每日为 AI 助手准备项目上下文时的繁琐体验，结合 `microsoft/markitdown`（文档转换）等热门项目的趋势洞察，以及对高效 AI 上下文管理的迫切需求。

---

### ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🔍 **智能文件发现** | 自动检测重要文件（README、配置、源码），忽略构建产物、依赖和媒体文件 |
| 💰 **Token 预算控制** | 设置 token 上限（`-b 8000`），工具自动包含文件直到预算用完 |
| 📋 **多格式输出** | **Markdown**（默认）、**XML**、**JSON**，适配不同 AI 助手工作流 |
| 🌳 **ASCII 目录树** | 美观的项目结构树状图，自动过滤 |
| 🔧 **尊重 .gitignore** | 自动遵循 `.gitignore` 规则（可用 `--no-gitignore` 禁用） |
| 🎯 **包含/排除模式** | 通过 glob 模式精细控制（`-i "*.test.js" --include "*.py"`） |
| 📦 **文件大小限制** | 自动跳过大文件（默认 1MB，可配置） |
| 🌍 **CJK Token 估算** | 精准计算 ASCII（~4 字符/token）和中文（1 字符/token）的 token 数 |

---

### 🚀 快速开始

#### 环境要求
- Python **3.8** 或更高版本
- 无需任何外部依赖

#### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/DevContext-CLI.git
cd DevContext-CLI

# 方式一：直接运行
python3 devcontext.py /path/to/your/project

# 方式二：安装为命令
pip install -e .
devcontext /path/to/your/project
```

#### 基础用法

```bash
# 提取当前目录上下文
devcontext

# 提取指定项目
devcontext /path/to/project

# 保存到文件
devcontext -o context.md

# 限制约 8000 token（如 Claude 的上下文窗口）
devcontext -b 8000 -o context.md

# 输出 XML 格式（适合结构化解析）
devcontext -f xml -o context.xml

# 仅包含 Python 文件
devcontext --include "*.py" -o python_context.md

# 忽略测试文件和文档
devcontext -i "*test*" -i "docs/*" -o context.md
```

---

### 📖 详细使用指南

#### 命令行选项

```
usage: devcontext [-h] [-o FILE] [-f {markdown,xml,json}] [-b TOKENS]
                  [-i PATTERN] [--include PATTERN] [--max-size BYTES]
                  [--no-gitignore] [-v] [--tree-only]
                  [path]

位置参数:
  path                  要分析的项目路径（默认：当前目录）

选项:
  -h, --help            显示帮助信息
  -o FILE, --output FILE
                        输出文件路径（默认：标准输出）
  -f {markdown,xml,json}, --format {markdown,xml,json}
                        输出格式（默认：markdown）
  -b TOKENS, --budget TOKENS
                        Token 预算限制（近似值）
  -i PATTERN, --ignore PATTERN
                        额外的忽略模式（可重复）
  --include PATTERN     仅包含匹配的模式（可重复）
  --max-size BYTES      最大文件大小（默认：1MB）
  --no-gitignore        忽略 .gitignore 规则
  -v, --version         显示版本
  --tree-only           仅输出目录树
```

#### 典型工作流

**Claude Code / Claude Desktop 用户：**
```bash
# Claude 对 Markdown 支持很好
devcontext -b 100000 -o context.md
# 然后将内容复制粘贴到 Claude 对话中
```

**Cursor AI 用户：**
```bash
# Cursor 同样偏好 Markdown
devcontext --include "*.py" --include "*.js" -b 8000 -o cursor_context.md
```

**API 工作流：**
```bash
# JSON 格式便于程序化处理
devcontext -f json -b 4000 -o context.json
```

**CI/CD 流水线：**
```bash
# XML 格式适合结构化解析
devcontext -f xml --no-gitignore -o project_context.xml
```

---

### 💡 设计思路与迭代规划

**设计理念：**
1. **零依赖** — 无需 `pip install`，任何 Python 环境都能直接运行
2. **开箱即用** — 智能默认配置，覆盖 90% 项目的使用场景
3. **AI 优先** — 每个功能都围绕 AI 助手工作流设计
4. **透明可见** — 清晰的 token 统计、文件包含/排除状态

**技术选型原因：**
- **Python 3.8+**: 最大兼容性，覆盖主流系统
- **纯标准库**: 无依赖地狱，即开即用
- **Pathlib**: 现代化、跨平台的路径处理
- **fnmatch**: Unix shell 风格的通配符，模式匹配直观熟悉

**后续迭代计划：**
- [ ] 交互式 TUI 模式，支持文件选择
- [ ] Git diff 集成（仅提取变更文件）
- [ ] 自定义输出模板系统
- [ ] 配置文件支持（`.devcontextrc`）
- [ ] 监视模式，实时更新上下文
- [ ] 与主流 AI 助手 API 深度集成

---

### 📦 打包与部署

本项目为 **CLI 工具/库** — 无需打包为可执行文件。

**分发方式：**
```bash
# 从源码安装
pip install -e .

# 或不安装直接运行
python3 devcontext.py [选项]
```

**兼容环境：**
- ✅ Linux（所有发行版）
- ✅ macOS（Intel 和 Apple Silicon）
- ✅ Windows（通过 Python）
- ✅ WSL

---

### 🤝 贡献指南

欢迎贡献！请遵循以下规范：

1. **Fork** 本仓库
2. 创建 **功能分支**（`git checkout -b feat/amazing-feature`）
3. **提交** 清晰的 commit 信息，遵循 [Conventional Commits](https://conventionalcommits.org/)
4. **推送** 到你的 fork
5. 发起 **Pull Request**

**Commit 格式：**
- `feat:` 新功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关

**Issue 反馈：**
- 使用 GitHub Issues 提交 bug 和功能请求
- 请包含 Python 版本、操作系统和复现步骤

---

### 📄 开源协议

本项目采用 **MIT 协议** — 详见 [LICENSE](LICENSE)。

---

## <a name="traditional-chinese"></a> 繁體中文
### 🎉 專案介紹

**DevContext-CLI** 是一款零依賴的命令列工具，專為 **Claude Code**、**Cursor**、**GitHub Copilot**、**Windsurf** 等 AI 編程助手智慧提取專案上下文。

**解決的核心痛點：** 向 AI 助手求助時，手動複製貼上多個檔案既繁瑣又容易出錯，還常常超出 AI 的 token 限制。DevContext-CLI 將整個流程自動化。

**自研差異化亮點：**
- 🧠 **智慧檔案篩選** — 自動識別關鍵檔案，排除建構產物和依賴
- 💰 **Token 預算管理** — 即時估算 token 數量，超預算自動截斷
- 📋 **多格式輸出** — Markdown、XML、JSON，適配不同 AI 助手偏好
- 🌳 **目錄樹生成** — 一目瞭然的專案結構視圖
- ⚡ **完全零依賴** — 純 Python 標準庫，隨處可用

---

### ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🔍 **智慧檔案發現** | 自動檢測重要檔案（README、配置、原始碼），忽略建構產物、依賴和媒體檔案 |
| 💰 **Token 預算控制** | 設定 token 上限（`-b 8000`），工具自動包含檔案直到預算用完 |
| 📋 **多格式輸出** | **Markdown**（預設）、**XML**、**JSON**，適配不同 AI 助手工作流 |
| 🌳 **ASCII 目錄樹** | 美觀的專案結構樹狀圖，自動過濾 |
| 🔧 **尊重 .gitignore** | 自動遵循 `.gitignore` 規則（可用 `--no-gitignore` 停用） |
| 🎯 **包含/排除模式** | 透過 glob 模式精細控制（`-i "*.test.js" --include "*.py"`） |
| 📦 **檔案大小限制** | 自動跳過大檔案（預設 1MB，可配置） |
| 🌍 **CJK Token 估算** | 精準計算 ASCII（~4 字元/token）和中文（1 字元/token）的 token 數 |

---

### 🚀 快速開始

#### 環境要求
- Python **3.8** 或更高版本
- 無需任何外部依賴

#### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/DevContext-CLI.git
cd DevContext-CLI

# 方式一：直接執行
python3 devcontext.py /path/to/your/project

# 方式二：安裝為命令
pip install -e .
devcontext /path/to/your/project
```

#### 基礎用法

```bash
# 提取當前目錄上下文
devcontext

# 提取指定專案
devcontext /path/to/project

# 儲存到檔案
devcontext -o context.md

# 限制約 8000 token（如 Claude 的上下文視窗）
devcontext -b 8000 -o context.md

# 輸出 XML 格式（適合結構化解析）
devcontext -f xml -o context.xml

# 僅包含 Python 檔案
devcontext --include "*.py" -o python_context.md

# 忽略測試檔案和文件
devcontext -i "*test*" -i "docs/*" -o context.md
```

---

### 📖 詳細使用指南

#### 命令列選項

```
usage: devcontext [-h] [-o FILE] [-f {markdown,xml,json}] [-b TOKENS]
                  [-i PATTERN] [--include PATTERN] [--max-size BYTES]
                  [--no-gitignore] [-v] [--tree-only]
                  [path]

位置參數:
  path                  要分析的專案路徑（預設：當前目錄）

選項:
  -h, --help            顯示幫助資訊
  -o FILE, --output FILE
                        輸出檔案路徑（預設：標準輸出）
  -f {markdown,xml,json}, --format {markdown,xml,json}
                        輸出格式（預設：markdown）
  -b TOKENS, --budget TOKENS
                        Token 預算限制（近似值）
  -i PATTERN, --ignore PATTERN
                        額外的忽略模式（可重複）
  --include PATTERN     僅包含匹配的模式（可重複）
  --max-size BYTES      最大檔案大小（預設：1MB）
  --no-gitignore        忽略 .gitignore 規則
  -v, --version         顯示版本
  --tree-only           僅輸出目錄樹
```

#### 典型工作流

**Claude Code / Claude Desktop 使用者：**
```bash
# Claude 對 Markdown 支援很好
devcontext -b 100000 -o context.md
# 然後將內容複製貼上到 Claude 對話中
```

**Cursor AI 使用者：**
```bash
# Cursor 同樣偏好 Markdown
devcontext --include "*.py" --include "*.js" -b 8000 -o cursor_context.md
```

**API 工作流：**
```bash
# JSON 格式便於程式化處理
devcontext -f json -b 4000 -o context.json
```

**CI/CD 流水線：**
```bash
# XML 格式適合結構化解析
devcontext -f xml --no-gitignore -o project_context.xml
```

---

### 💡 設計思路與迭代規劃

**設計理念：**
1. **零依賴** — 無需 `pip install`，任何 Python 環境都能直接執行
2. **開箱即用** — 智慧預設配置，覆蓋 90% 專案的使用場景
3. **AI 優先** — 每個功能都圍繞 AI 助手工作流設計
4. **透明可見** — 清晰的 token 統計、檔案包含/排除狀態

**技術選型原因：**
- **Python 3.8+**: 最大相容性，覆蓋主流系統
- **純標準庫**: 無依賴地獄，即開即用
- **Pathlib**: 現代化、跨平台的路徑處理
- **fnmatch**: Unix shell 風格的萬用字元，模式匹配直觀熟悉

**後續迭代計畫：**
- [ ] 互動式 TUI 模式，支援檔案選擇
- [ ] Git diff 整合（僅提取變更檔案）
- [ ] 自訂輸出模板系統
- [ ] 配置檔案支援（`.devcontextrc`）
- [ ] 監視模式，即時更新上下文
- [ ] 與主流 AI 助手 API 深度整合

---

### 📦 打包與部署

本專案為 **CLI 工具/庫** — 無需打包為可執行檔。

**分發方式：**
```bash
# 從原始碼安裝
pip install -e .

# 或不安裝直接執行
python3 devcontext.py [選項]
```

**相容環境：**
- ✅ Linux（所有發行版）
- ✅ macOS（Intel 和 Apple Silicon）
- ✅ Windows（透過 Python）
- ✅ WSL

---

### 🤝 貢獻指南

歡迎貢獻！請遵循以下規範：

1. **Fork** 本倉庫
2. 建立 **功能分支**（`git checkout -b feat/amazing-feature`）
3. **提交** 清晰的 commit 資訊，遵循 [Conventional Commits](https://conventionalcommits.org/)
4. **推送** 到你的 fork
5. 發起 **Pull Request**

**Commit 格式：**
- `feat:` 新功能
- `fix:` 修復問題
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試相關

**Issue 回饋：**
- 使用 GitHub Issues 提交 bug 和功能請求
- 請包含 Python 版本、作業系統和復現步驟

---

### 📄 開源協議

本專案採用 **MIT 協議** — 詳見 [LICENSE](LICENSE)。
