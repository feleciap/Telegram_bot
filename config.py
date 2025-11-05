import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7323246474:AAGHhnVM5Ah9l3tDsU9D3HD9TGSArKwf6Fs")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot_data.db")
ADMIN_IDS = [
    int(x) for x in os.getenv("TELEGRAM_ADMIN_IDS", "").split(",") if x.strip().isdigit()
]
