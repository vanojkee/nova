import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nova.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from nova_bot.tg_bot import start_bot

if __name__ == "__main__":
    start_bot()
