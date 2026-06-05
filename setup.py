#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DevContext-CLI Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent.resolve()
readme = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="devcontext-cli",
    version="1.0.0",
    description="🧠 Intelligent developer context extraction engine for AI assistants",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Lobster Automation",
    author_email="dev@lobster.automation",
    url="https://github.com/lobster-automation/DevContext-CLI",
    py_modules=["devcontext"],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "devcontext=devcontext:main",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="ai developer context extraction cli tool cursor claude copilot",
    license="MIT",
)
