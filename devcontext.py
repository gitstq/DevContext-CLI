#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevContext-CLI 🧠
Developer Context Intelligent Extraction Engine
智能开发者上下文提取引擎

A zero-dependency CLI tool that intelligently extracts project context
for AI coding assistants. Automatically filters key files, manages token budgets,
and generates structured output in multiple formats.

Author: Lobster Automation
License: MIT
"""

import os
import sys
import argparse
import fnmatch
import json
from pathlib import Path
from datetime import datetime


__version__ = "1.0.0"
__author__ = "Lobster Automation"


# ═══════════════════════════════════════════════════════════════
# Default Configuration
# ═══════════════════════════════════════════════════════════════

DEFAULT_IGNORE_PATTERNS = [
    # Version Control
    ".git", ".gitignore", ".gitattributes",
    # Python
    "__pycache__", "*.pyc", "*.pyo", "*.pyd", ".pytest_cache",
    "*.egg-info", "dist", "build", "*.egg", ".tox", ".venv",
    "venv", "env", ".env", "*.whl",
    # Node.js
    "node_modules", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "*.min.js", "*.min.css", ".next", ".nuxt", "dist",
    # Java
    "target", "*.class", "*.jar", "*.war", ".gradle", "build",
    # Go
    "vendor", "go.sum",
    # Rust
    "target", "Cargo.lock",
    # IDE & Editors
    ".idea", ".vscode", "*.swp", "*.swo", "*~", ".DS_Store",
    # Images & Media
    "*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.ico",
    "*.mp4", "*.mp3", "*.wav", "*.pdf", "*.zip", "*.tar.gz",
    # Logs & Data
    "*.log", "*.db", "*.sqlite", "*.sqlite3", ".coverage",
    # Lock files
    "*.lock", "Gemfile.lock", "composer.lock",
]

DEFAULT_PRIORITY_PATTERNS = [
    "README*", "readme*", "CHANGELOG*", "changelog*",
    "CONTRIBUTING*", "LICENSE*", "license*",
    "setup.py", "pyproject.toml", "package.json",
    "Cargo.toml", "go.mod", "pom.xml", "build.gradle",
    "Makefile", "Dockerfile", "docker-compose*",
    "*.md", "*.txt", "*.yaml", "*.yml", "*.json",
    "*.py", "*.js", "*.ts", "*.go", "*.rs", "*.java",
    "*.c", "*.cpp", "*.h", "*.hpp",
    "*.sh", "*.bash", "*.zsh",
]

# File extension to language mapping for code blocks
EXT_TO_LANG = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".jsx": "jsx", ".tsx": "tsx", ".go": "go", ".rs": "rust",
    ".java": "java", ".c": "c", ".cpp": "cpp", ".h": "c",
    ".hpp": "cpp", ".cs": "csharp", ".rb": "ruby", ".php": "php",
    ".swift": "swift", ".kt": "kotlin", ".scala": "scala",
    ".r": "r", ".m": "matlab", ".sh": "bash", ".bash": "bash",
    ".zsh": "zsh", ".ps1": "powershell", ".sql": "sql",
    ".html": "html", ".css": "css", ".scss": "scss", ".sass": "sass",
    ".less": "less", ".xml": "xml", ".yaml": "yaml", ".yml": "yaml",
    ".json": "json", ".toml": "toml", ".ini": "ini", ".cfg": "ini",
    ".md": "markdown", ".rst": "rst", ".tex": "latex",
    ".dockerfile": "dockerfile", "makefile": "makefile",
}


# ═══════════════════════════════════════════════════════════════
# Token Estimation
# ═══════════════════════════════════════════════════════════════

def estimate_tokens(text: str) -> int:
    """
    Estimate token count using a hybrid approach:
    - For ASCII text: ~4 characters per token (GPT-style)
    - For CJK text: ~1 character per token
    """
    if not text:
        return 0
    total = 0
    for char in text:
        if ord(char) > 127:  # Non-ASCII (CJK, emoji, etc.)
            total += 1
        else:
            total += 0.25
    return int(total)


# ═══════════════════════════════════════════════════════════════
# File Discovery & Filtering
# ═══════════════════════════════════════════════════════════════

class FileFilter:
    """Intelligent file filtering engine."""

    def __init__(self, root: Path, ignore_patterns=None, include_patterns=None,
                 max_file_size: int = 1024 * 1024, respect_gitignore: bool = True):
        self.root = root.resolve()
        self.ignore_patterns = set(DEFAULT_IGNORE_PATTERNS + (ignore_patterns or []))
        self.include_patterns = include_patterns
        self.max_file_size = max_file_size
        self.respect_gitignore = respect_gitignore
        self.gitignore_patterns = self._load_gitignore() if respect_gitignore else []

    def _load_gitignore(self) -> list:
        """Load .gitignore patterns if present."""
        gitignore_path = self.root / ".gitignore"
        if not gitignore_path.exists():
            return []
        patterns = []
        try:
            with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        except Exception:
            pass
        return patterns

    def _is_ignored(self, path: Path) -> bool:
        """Check if a path should be ignored."""
        rel_path = path.relative_to(self.root)
        rel_str = str(rel_path).replace("\\", "/")
        name = path.name

        # Check default and custom ignore patterns
        for pattern in self.ignore_patterns:
            # Match against file/directory name
            if fnmatch.fnmatch(name, pattern):
                return True
            # Match against relative path
            if fnmatch.fnmatch(rel_str, pattern):
                return True
            # Match parent directory components for patterns like "node_modules"
            if "/" not in pattern:
                for part in rel_path.parts:
                    if fnmatch.fnmatch(part, pattern):
                        return True
            # Directory pattern matching (pattern ending with /)
            if pattern.endswith("/"):
                dir_pattern = pattern.rstrip("/")
                if any(fnmatch.fnmatch(part, dir_pattern) for part in rel_path.parts):
                    return True

        # Check .gitignore patterns
        for pattern in self.gitignore_patterns:
            if pattern.endswith("/"):
                dir_pattern = pattern.rstrip("/")
                if any(fnmatch.fnmatch(part, dir_pattern) for part in rel_path.parts):
                    return True
            else:
                if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_str, pattern):
                    return True

        # Check file size
        if path.is_file() and path.stat().st_size > self.max_file_size:
            return True

        return False

    def _is_included(self, path: Path) -> bool:
        """Check if file matches include patterns."""
        if not self.include_patterns:
            return True
        rel_str = str(path.relative_to(self.root)).replace("\\", "/")
        name = path.name
        for pattern in self.include_patterns:
            if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(rel_str, pattern):
                return True
        return False

    def discover(self) -> list:
        """
        Discover all relevant files in the project.
        Returns sorted list of Path objects (priority files first).
        """
        files = []
        priority_files = []
        normal_files = []

        for item in self.root.rglob("*"):
            if item.is_file() and not self._is_ignored(item):
                if not self._is_included(item):
                    continue
                rel_str = str(item.relative_to(self.root)).replace("\\", "/")
                # Check if it's a priority file
                is_priority = any(
                    fnmatch.fnmatch(item.name, p) or fnmatch.fnmatch(rel_str, p)
                    for p in DEFAULT_PRIORITY_PATTERNS
                )
                if is_priority:
                    priority_files.append(item)
                else:
                    normal_files.append(item)

        # Sort within each group
        priority_files.sort(key=lambda p: str(p.relative_to(self.root)))
        normal_files.sort(key=lambda p: str(p.relative_to(self.root)))

        return priority_files + normal_files


# ═══════════════════════════════════════════════════════════════
# Content Formatters
# ═══════════════════════════════════════════════════════════════

class BaseFormatter:
    """Base class for output formatters."""

    def __init__(self, root: Path, files: list, budget: int = None):
        self.root = root
        self.files = files
        self.budget = budget
        self.used_tokens = 0
        self.included_files = []
        self.skipped_files = []

    def _get_lang(self, path: Path) -> str:
        """Get language identifier for code blocks."""
        ext = path.suffix.lower()
        name = path.name.lower()
        if name == "dockerfile":
            return "dockerfile"
        if name == "makefile":
            return "makefile"
        return EXT_TO_LANG.get(ext, "")

    def _read_file(self, path: Path) -> str:
        """Safely read file content."""
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception as e:
            return f"[Error reading file: {e}]"

    def _check_budget(self, text: str) -> bool:
        """Check if adding text would exceed token budget."""
        if self.budget is None:
            return True
        tokens = estimate_tokens(text)
        if self.used_tokens + tokens > self.budget:
            return False
        self.used_tokens += tokens
        return True

    def _add_file_tokens(self, text: str):
        """Add token count for a file that was included."""
        self.used_tokens += estimate_tokens(text)

    def generate(self) -> str:
        raise NotImplementedError


class MarkdownFormatter(BaseFormatter):
    """Generate Markdown-formatted context."""

    def generate(self) -> str:
        lines = []
        lines.append("# 📁 Project Context")
        lines.append("")
        lines.append(f"**Project:** `{self.root.name}`  ")
        lines.append(f"**Path:** `{self.root}`  ")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ")
        lines.append(f"**Files:** {len(self.files)}  ")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Directory tree
        lines.append("## 🌲 Directory Structure")
        lines.append("")
        lines.append("```")
        tree = self._generate_tree()
        lines.append(tree)
        lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")

        # File contents
        lines.append("## 📄 File Contents")
        lines.append("")

        for file_path in self.files:
            rel_path = file_path.relative_to(self.root)
            content = self._read_file(file_path)
            lang = self._get_lang(file_path)

            section_lines = [
                f"### `{rel_path}`",
                "",
                f"```{lang}",
                content,
                "```",
                "",
                "---",
                "",
            ]
            section_text = "\n".join(section_lines)

            if self._check_budget(section_text):
                lines.extend(section_lines[:-1])  # Exclude trailing ---
                lines.append("")
                self.included_files.append(rel_path)
            else:
                self.skipped_files.append(rel_path)
                # Add a note about skipped file
                skip_lines = [
                    f"### `{rel_path}`",
                    "",
                    "> ⚠️ **Skipped:** Exceeds token budget",
                    "",
                    "---",
                    "",
                ]
                lines.extend(skip_lines)

        # Summary
        lines.append("## 📊 Summary")
        lines.append("")
        lines.append(f"- **Total files discovered:** {len(self.files)}")
        lines.append(f"- **Files included:** {len(self.included_files)}")
        lines.append(f"- **Files skipped:** {len(self.skipped_files)}")
        lines.append(f"- **Estimated tokens:** {self.used_tokens:,}")
        if self.budget:
            lines.append(f"- **Token budget:** {self.budget:,}")
            lines.append(f"- **Budget usage:** {self.used_tokens / self.budget * 100:.1f}%")
        lines.append("")

        return "\n".join(lines)

    def _generate_tree(self) -> str:
        """Generate ASCII directory tree."""
        lines = [self.root.name + "/"]

        def add_tree(dir_path: Path, prefix: str = ""):
            try:
                items = sorted(dir_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
            except PermissionError:
                return

            # Filter out ignored items
            filtered = []
            for item in items:
                rel = item.relative_to(self.root)
                # Quick check - skip obvious ignores
                if item.name.startswith(".") and item.name in {".git", ".venv", "venv", ".env", ".idea", ".vscode", "__pycache__", "node_modules"}:
                    continue
                if item.name in {"target", "dist", "build"} and item.is_dir():
                    continue
                filtered.append(item)

            for i, item in enumerate(filtered):
                is_last = i == len(filtered) - 1
                connector = "└── " if is_last else "├── "
                lines.append(f"{prefix}{connector}{item.name}{'/' if item.is_dir() else ''}")
                if item.is_dir():
                    extension = "    " if is_last else "│   "
                    add_tree(item, prefix + extension)

        add_tree(self.root)
        return "\n".join(lines)


class XMLFormatter(BaseFormatter):
    """Generate XML-formatted context."""

    def generate(self) -> str:
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<project-context>',
            f'  <name>{self._escape(self.root.name)}</name>',
            f'  <path>{self._escape(str(self.root))}</path>',
            f'  <generated>{datetime.now().isoformat()}</generated>',
            '  <files>',
        ]

        for file_path in self.files:
            rel_path = file_path.relative_to(self.root)
            content = self._read_file(file_path)
            lang = self._get_lang(file_path)

            file_xml = [
                '    <file>',
                f'      <path>{self._escape(str(rel_path))}</path>',
                f'      <language>{lang}</language>',
                '      <content><![CDATA[',
                content,
                '      ]]></content>',
                '    </file>',
            ]
            file_text = "\n".join(file_xml)

            if self._check_budget(file_text):
                lines.extend(file_xml)
                self.included_files.append(rel_path)
            else:
                self.skipped_files.append(rel_path)
                lines.extend([
                    '    <file>',
                    f'      <path>{self._escape(str(rel_path))}</path>',
                    '      <skipped>true</skipped>',
                    '    </file>',
                ])

        lines.extend([
            '  </files>',
            '  <summary>',
            f'    <total>{len(self.files)}</total>',
            f'    <included>{len(self.included_files)}</included>',
            f'    <skipped>{len(self.skipped_files)}</skipped>',
            f'    <tokens>{self.used_tokens}</tokens>',
            '  </summary>',
            '</project-context>',
        ])

        return "\n".join(lines)

    def _escape(self, text: str) -> str:
        """Escape XML special characters."""
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class JSONFormatter(BaseFormatter):
    """Generate JSON-formatted context."""

    def generate(self) -> str:
        data = {
            "project": self.root.name,
            "path": str(self.root),
            "generated": datetime.now().isoformat(),
            "files": [],
            "summary": {
                "total": len(self.files),
                "included": 0,
                "skipped": 0,
                "tokens": 0,
            }
        }

        for file_path in self.files:
            rel_path = file_path.relative_to(self.root)
            content = self._read_file(file_path)
            lang = self._get_lang(file_path)

            file_data = {
                "path": str(rel_path),
                "language": lang,
                "content": content,
            }
            file_text = json.dumps(file_data, ensure_ascii=False)

            if self._check_budget(file_text):
                data["files"].append(file_data)
                self.included_files.append(rel_path)
            else:
                self.skipped_files.append(rel_path)
                data["files"].append({
                    "path": str(rel_path),
                    "skipped": True,
                })

        data["summary"]["included"] = len(self.included_files)
        data["summary"]["skipped"] = len(self.skipped_files)
        data["summary"]["tokens"] = self.used_tokens

        return json.dumps(data, indent=2, ensure_ascii=False)


# ═══════════════════════════════════════════════════════════════
# CLI Interface
# ═══════════════════════════════════════════════════════════════

def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="devcontext",
        description="🧠 DevContext-CLI — Intelligent developer context extraction for AI assistants",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Extract current directory context
  %(prog)s /path/to/project         # Extract specific project
  %(prog)s -o context.md            # Save to file
  %(prog)s -f xml                   # Output as XML
  %(prog)s -b 8000                  # Limit to ~8000 tokens
  %(prog)s -i "*.test.js" -i "docs" # Ignore additional patterns
  %(prog)s --include "*.py"         # Only include Python files
        """
    )

    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project path to analyze (default: current directory)",
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        help="Output file path (default: stdout)",
    )
    parser.add_argument(
        "-f", "--format",
        choices=["markdown", "xml", "json"],
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "-b", "--budget",
        type=int,
        metavar="TOKENS",
        help="Token budget limit (approximate)",
    )
    parser.add_argument(
        "-i", "--ignore",
        action="append",
        metavar="PATTERN",
        help="Additional ignore patterns (can be used multiple times)",
    )
    parser.add_argument(
        "--include",
        action="append",
        metavar="PATTERN",
        help="Only include files matching these patterns",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=1024 * 1024,
        metavar="BYTES",
        help="Maximum file size in bytes (default: 1MB)",
    )
    parser.add_argument(
        "--no-gitignore",
        action="store_true",
        help="Do not respect .gitignore rules",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--tree-only",
        action="store_true",
        help="Only output directory tree (no file contents)",
    )

    return parser


def main():
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Resolve project path
    project_path = Path(args.path).resolve()
    if not project_path.exists():
        print(f"❌ Error: Path does not exist: {project_path}", file=sys.stderr)
        sys.exit(1)
    if not project_path.is_dir():
        print(f"❌ Error: Path is not a directory: {project_path}", file=sys.stderr)
        sys.exit(1)

    # Discover files
    print(f"🔍 Scanning: {project_path}", file=sys.stderr)
    file_filter = FileFilter(
        root=project_path,
        ignore_patterns=args.ignore,
        include_patterns=args.include,
        max_file_size=args.max_size,
        respect_gitignore=not args.no_gitignore,
    )
    files = file_filter.discover()
    print(f"📁 Found {len(files)} files", file=sys.stderr)

    if not files:
        print("⚠️ No files found matching criteria", file=sys.stderr)
        sys.exit(0)

    # Select formatter
    if args.format == "xml":
        formatter = XMLFormatter(project_path, files, args.budget)
    elif args.format == "json":
        formatter = JSONFormatter(project_path, files, args.budget)
    else:
        formatter = MarkdownFormatter(project_path, files, args.budget)

    # Generate output
    output = formatter.generate()

    # Output result
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(output, encoding="utf-8")
        print(f"✅ Saved to: {output_path}", file=sys.stderr)
        print(f"📊 Included: {len(formatter.included_files)} files", file=sys.stderr)
        print(f"📊 Skipped: {len(formatter.skipped_files)} files", file=sys.stderr)
        print(f"📊 Estimated tokens: {formatter.used_tokens:,}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
