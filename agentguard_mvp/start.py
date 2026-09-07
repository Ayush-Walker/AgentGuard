import subprocess
import sys
import time

backend = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend:app", "--host", "127.0.0.1", "--port", "8000"])
time.sleep(1.5)
dashboard = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
try:
    dashboard.wait()
finally:
    backend.terminate()
    backend.wait()
