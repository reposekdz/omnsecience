#!/usr/bin/env python3
"""
Omniscience Framework — Entry Point
Launches the interactive Command Center CLI.
"""
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from commandcenter import OmniShell
    
    # Launch the interactive shell
    shell = OmniShell()
    shell.run()
