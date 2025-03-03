import signal
import sys
import time

# def signal_handler(sig, frame):
#     sys.exit(0)

# signal.signal(signal.SIGINT, signal_handler)

for i in range(100):
    time.sleep(0.1)
    print(i)
