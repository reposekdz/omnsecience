#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Robust Omniscience Installer with Virtualenv + Network Retry"""

import os
import sys
import subprocess
import venv
import shutil
from pathlib import Path

VENV_DIR = Path('venv')
REQUIREMENTS = [
    'colorama>=0.4.6',
    'scapy>=2.5.0,<2.6.0',  # Stable version matching requirements.txt
    'impacket>=0.10.0,<0.11.0',  # Stable, avoids download issues
    'paramiko>=3.4.0,<4.0.0',
    'netifaces2>=1.0.0',
    'PyQt6>=6.5.0',
    'Pillow>=10.0.0',
    'pywin32>=306',
    'pycryptodome>=3.20.0',
    'requests>=2.31.0',
    'pyyaml>=6.0.1',
    'dnspython>=2.4.0',
    'pymysql>=1.1.0',
    'psycopg2-binary>=2.9.9',
    'pymongo>=4.10.0',
    'redis>=5.0.0',
    'ldap3>=2.9.1'
]

def print_step(msg):
    print(f'\n{"="*50}')
    print(f'[{msg.upper()}]')
    print('='*50)

def create_venv():
    print_step('Creating Virtual Environment')
    if VENV_DIR.exists():
        shutil.rmtree(VENV_DIR)
    venv.create(VENV_DIR, with_pip=True)
    print(f'[+] Virtualenv created: {VENV_DIR}')

def get_pip():
    if sys.platform == 'win32':
        return VENV_DIR / 'Scripts' / 'pip.exe'
    return VENV_DIR / 'bin' / 'pip'

def pip_install(package, max_retries=5):
    pip = get_pip()
    cmd = [str(pip), 'install', '--no-cache-dir', '--retries', '5', '--timeout', '100', package]
    
    for attempt in range(max_retries):
        try:
            print(f'Installing {package} (attempt {attempt+1}/{max_retries})...')
            subprocess.check_call(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f'[+] {package} installed successfully')
            return True
        except subprocess.CalledProcessError as e:
            print(f'[!] Attempt {attempt+1} failed: {e}')
            if attempt < max_retries - 1:
                print('Retrying in 5 seconds...')
                import time
                time.sleep(5)
    print(f'[!] {package} failed after {max_retries} attempts')
    return False

def install_all():
    create_venv()
    
    print_step('Installing Dependencies')
    success_count = 0
    for pkg in REQUIREMENTS:
        if pip_install(pkg):
            success_count += 1
    
    print(f'\n[+] {success_count}/{len(REQUIREMENTS)} packages installed successfully')
    
    if success_count == len(REQUIREMENTS):
        print_step('SUCCESS')
        print('To activate and run:')
        if sys.platform == 'win32':
            print(f'{VENV_DIR}\\Scripts\\activate')
        else:
            print(f'source {VENV_DIR}/bin/activate')
        print('python main.py')
        return True
    else:
        print('[!] Some packages failed. Check network connection.')
        return False

if __name__ == '__main__':
    if install_all():
        print('\n🎉 Installation Complete!')
    else:
        sys.exit(1)
