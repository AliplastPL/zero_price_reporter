import time
import os
import sys

# Get the directory where the script or .exe is located
if getattr(sys, 'frozen', False):
    # If running as a PyInstaller bundle
    application_path = os.path.dirname(sys.executable)
else:
    # If running as a script
    application_path = os.path.dirname(os.path.abspath(__file__))

# Create 'logs' directory if it doesn't exist
logs_dir = os.path.join(application_path, "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

current_dateTime = time.strftime("%d.%m.%Y_%H-%M-%S", time.localtime())
log_file_path = os.path.join(logs_dir, f"{current_dateTime}.log")

def printandlog(message):
    print(message)

    try:
        with open(log_file_path, "a", encoding='utf-8') as f:
            f.write(f"{message}\n")
    except Exception as e:
        print(f"Błąd podczas zapisu do loga: {str(e)}")
