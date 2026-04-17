#!/usr/bin/env python3
"""
Omniscience Framework — Entry Point
Launches the interactive Command Center CLI.
"""
import os
import sys
import importlib.util

if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location(
        "commandcenter",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "commandcenter.py")
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
