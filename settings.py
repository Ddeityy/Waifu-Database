import os
import dotenv

dotenv.load_dotenv()
KEY = os.getenv("KEY")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite"),
    }
}
INSTALLED_APPS = ("db",)
SECRET_KEY = KEY
