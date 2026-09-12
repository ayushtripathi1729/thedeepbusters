"""Run with: python worker.py. Training/inference is never run in the web process."""
import time
from maayabreaker.database import init
from maayabreaker.jobs import process_one
init()
while True:
    if not process_one(): time.sleep(1)
