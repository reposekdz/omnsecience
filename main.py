#!/usr/bin/env python3
import asyncio
import sys
from commandcenter import main_loop

def check_dependencies():
    # Basic sanity check for critical libraries
    try:
        import scapy
        import impacket
    except ImportError as e:
        print(f"Missing dependency: {e}. Run 'pip install -r requirements.txt'")
        sys.exit(1)

if __name__ == "__main__":
    check_dependencies()
    asyncio.run(main_loop())