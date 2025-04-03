# One clickable python file and running webserver and openable on browser

import subprocess
import sys
import os

def run_backend():
    backend_script = os.path.join("backend", "main.py")
    subprocess.Popen([sys.executable, backend_script], shell=True)

def run_frontend():
    frontend_dir = os.path.join("frontend")
    subprocess.Popen(["npm", "start"], cwd=frontend_dir, shell=True)

if __name__ == "__main__":
    run_backend()
    run_frontend()