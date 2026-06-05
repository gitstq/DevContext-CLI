#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevContext-CLI Unit Tests
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from devcontext import estimate_tokens, FileFilter, MarkdownFormatter, XMLFormatter, JSONFormatter


class TestTokenEstimation(unittest.TestCase):
    """Test token estimation logic."""

    def test_empty_string(self):
        self.assertEqual(estimate_tokens(""), 0)

    def test_ascii_text(self):
        # ~4 chars per token for ASCII
        text = "hello world"
        result = estimate_tokens(text)
        # 11 chars * 0.25 = 2.75 -> int() = 2
        self.assertEqual(result, 2)

    def test_cjk_text(self):
        # 1 char per token for CJK
        text = "你好世界"
        self.assertEqual(estimate_tokens(text), 4)

    def test_mixed_text(self):
        text = "hello 你好"
        result = estimate_tokens(text)
        # hello = 5 * 0.25 = 1.25, space = 0.25, 你好 = 2
        self.assertAlmostEqual(result, 3, places=0)


class TestFileFilter(unittest.TestCase):
    """Test file discovery and filtering."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.root = Path(self.temp_dir)

        # Create test file structure
        (self.root / "src").mkdir()
        (self.root / "tests").mkdir()
        (self.root / "node_modules").mkdir()
        (self.root / ".git").mkdir()

        (self.root / "README.md").write_text("# Test Project")
        (self.root / "src" / "main.py").write_text("print('hello')")
        (self.root / "src" / "utils.py").write_text("def helper(): pass")
        (self.root / "tests" / "test_main.py").write_text("def test(): pass")
        (self.root / "node_modules" / "package.js").write_text("// ignore")
        (self.root / ".git" / "config").write_text("[core]")
        (self.root / "large_file.bin").write_bytes(b"x" * (2 * 1024 * 1024))  # 2MB

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_discover_excludes_ignored(self):
        filter_engine = FileFilter(self.root)
        files = filter_engine.discover()
        paths = [str(f.relative_to(self.root)) for f in files]

        # Should NOT include ignored directories
        self.assertNotInAny("node_modules", paths)
        self.assertNotInAny(".git", paths)

        # Should NOT include oversized files
        self.assertNotIn("large_file.bin", paths)

        # Should include source files
        self.assertIn("src/main.py", paths)
        self.assertIn("src/utils.py", paths)
        self.assertIn("tests/test_main.py", paths)
        self.assertIn("README.md", paths)

    def test_discover_priority_order(self):
        filter_engine = FileFilter(self.root)
        files = filter_engine.discover()

        # README should come before source files (priority ordering)
        readme_idx = next(i for i, f in enumerate(files) if f.name == "README.md")
        main_idx = next(i for i, f in enumerate(files) if f.name == "main.py")
        self.assertLess(readme_idx, main_idx)

    def test_include_patterns(self):
        filter_engine = FileFilter(self.root, include_patterns=["*.py"])
        files = filter_engine.discover()
        paths = [str(f.relative_to(self.root)) for f in files]

        self.assertIn("src/main.py", paths)
        self.assertIn("src/utils.py", paths)
        self.assertNotIn("README.md", paths)

    def test_custom_ignore(self):
        filter_engine = FileFilter(self.root, ignore_patterns=["tests/*"])
        files = filter_engine.discover()
        paths = [str(f.relative_to(self.root)) for f in files]

        self.assertNotIn("tests/test_main.py", paths)
        self.assertIn("src/main.py", paths)

    def assertNotInAny(self, substring, collection):
        """Assert no item in collection contains substring."""
        for item in collection:
            self.assertNotIn(substring, item)


class TestFormatters(unittest.TestCase):
    """Test output formatters."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.root = Path(self.temp_dir)

        (self.root / "README.md").write_text("# Project\n\nDescription here.")
        (self.root / "main.py").write_text("def main():\n    print('hi')")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_markdown_formatter(self):
        files = [self.root / "README.md", self.root / "main.py"]
        formatter = MarkdownFormatter(self.root, files)
        output = formatter.generate()

        self.assertIn("# 📁 Project Context", output)
        self.assertIn("## 🌲 Directory Structure", output)
        self.assertIn("## 📄 File Contents", output)
        self.assertIn("```python", output)
        self.assertIn("def main():", output)
        self.assertIn("## 📊 Summary", output)

    def test_xml_formatter(self):
        files = [self.root / "README.md", self.root / "main.py"]
        formatter = XMLFormatter(self.root, files)
        output = formatter.generate()

        self.assertIn('<?xml version="1.0"', output)
        self.assertIn("<project-context>", output)
        self.assertIn("<files>", output)
        self.assertIn("<path>", output)
        self.assertIn("<content>", output)

    def test_json_formatter(self):
        files = [self.root / "README.md", self.root / "main.py"]
        formatter = JSONFormatter(self.root, files)
        output = formatter.generate()

        import json
        data = json.loads(output)
        self.assertEqual(data["project"], self.root.name)
        self.assertEqual(len(data["files"]), 2)
        self.assertIn("summary", data)

    def test_budget_limit(self):
        files = [self.root / "README.md", self.root / "main.py"]
        # Very small budget - should skip second file
        formatter = MarkdownFormatter(self.root, files, budget=100)
        output = formatter.generate()

        # Should still generate but may skip some content
        self.assertIn("📁 Project Context", output)
        self.assertIn("📊 Summary", output)


class TestCLI(unittest.TestCase):
    """Test CLI argument parsing."""

    def test_parser_creation(self):
        from devcontext import create_parser
        parser = create_parser()
        self.assertIsNotNone(parser)

    def test_default_args(self):
        from devcontext import create_parser
        parser = create_parser()
        args = parser.parse_args([])
        self.assertEqual(args.path, ".")
        self.assertEqual(args.format, "markdown")
        self.assertIsNone(args.budget)

    def test_custom_args(self):
        from devcontext import create_parser
        parser = create_parser()
        args = parser.parse_args(["/some/path", "-f", "xml", "-b", "5000", "-o", "out.md"])
        self.assertEqual(args.path, "/some/path")
        self.assertEqual(args.format, "xml")
        self.assertEqual(args.budget, 5000)
        self.assertEqual(args.output, "out.md")


if __name__ == "__main__":
    unittest.main(verbosity=2)
