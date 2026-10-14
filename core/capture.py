import json, os
from datetime import datetime
from core.config import Config

class Capture:
    @staticmethod
    def save(ip, data):
        os.makedirs(Config.LOG_DIR, exist_ok=True)
        entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": ip,
            "data": data
        }
        try:
            with open(Config.LOG_FILE, "r") as f:
                logs = json.load(f)
        except:
            logs = []
        logs.append(entry)
        with open(Config.LOG_FILE, "w") as f:
            json.dump(logs, f, indent=2)
        return entry

    @staticmethod
    def view():
        try:
            with open(Config.LOG_FILE, "r") as f:
                return json.load(f)
        except:
            return []

    @staticmethod
    def clear():
        with open(Config.LOG_FILE, "w") as f:
            f.write("[]")
