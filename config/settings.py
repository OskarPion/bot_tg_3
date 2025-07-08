import os

TOKEN = str(os.environ.get("TOKEN"))
DOMAIN = str(os.environ.get("DOMAIN"))
GOOGLE_API_KEY = str(os.environ.get("GOOGLE_API_KEY"))
GOOGLE_CSE_ID = str(os.environ.get("GOOGLE_CSE_ID"))
POSTGRES_USER = str(os.environ.get("POSTGRES_USER"))
POSTGRES_PASSWORD = str(os.environ.get("POSTGRES_PASSWORD"))
POSTGRES_DB = str(os.environ.get("POSTGRES_DB"))
DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
WEBHOOK_PATH = "/bot"
WEBHOOK_URL = DOMAIN + WEBHOOK_PATH
