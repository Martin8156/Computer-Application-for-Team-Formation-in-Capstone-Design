# coding: utf-8

import asyncio
import os
import signal
import sys
import time

solver_pid = None

async def test_solver():
    script_path = "CAP25/Backend/working/test_solver.py"
    
    # really important to add -u to allow real-time output
    proc = await asyncio.create_subprocess_shell(
        f"python -u {script_path}", 
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    
    global solver_pid
    solver_pid = proc.pid

    while True:
        line = await proc.stdout.readline()
        if not line:  # EOF
            break

        line = line.decode('utf-8').rstrip()
        print(line)

    solver_pid = None

# handle signal
def signal_handler(sig, frame):
    if solver_pid:
        os.kill(solver_pid, signal.SIGINT)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    asyncio.run(test_solver())