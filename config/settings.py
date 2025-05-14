import os

TOKEN = str(os.environ.get("TOKEN"))
DOMAIN = str(os.environ.get("DOMAIN"))
WEBHOOK_PATH = "/bot"
WEBHOOK_URL = DOMAIN + WEBHOOK_PATH
