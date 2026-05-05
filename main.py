import asyncio
import sys
import os
from commandcenter import OmniShell

def check_dependencies():
    """Verify core functional dependencies are installed."""
    deps = ['scapy', 'impacket', 'paramiko', 'requests', 'cryptography']
    missing = []
    for dep in deps:
        try:
            __import__(dep)
        except ImportError:
            missing.append(dep)
    
    if missing:
        print(f"[!] MISSING DEPENDENCIES: {', '.join(missing)}")
        print("[*] Install via: pip install -r requirements.txt")
        sys.exit(1)

async def main():
    # Ensure administrative privileges for Scapy and Raw Sockets
    if os.name == 'nt':
        import ctypes
        if not ctypes.windll.shell32.IsUserAnAdmin():
            print("[!] SYSTEM ALERT: Framework requires Administrative privileges for Raw Socket operations.")
    
    print("""
    =================================================  [STABLE]
    ||          OMNISCIENCE ULTRAMAX PRO v6.0      ||
    ||      ADVANCED CYBERSECURITY FRAMEWORK       ||
    =================================================
    [*] Initializing AMMO v2 Asynchronous Engine...
    [*] Loading Command Center...
    """)
    
    shell = OmniShell()
    try:
        await shell.cmdloop_async()
    except KeyboardInterrupt:
        print("\n[*] Shutting down C2 sessions...")
    except Exception as e:
        print(f"[CRITICAL] Kernel Panic: {e}")

if __name__ == "__main__":
    # Check dependencies before starting the event loop
    check_dependencies()
    
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main())