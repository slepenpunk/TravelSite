from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

SECRET_KEY = os.environ.get("SECRET_KEY")

REDIS_URL = os.environ.get("REDIS_URL")

SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASS = os.environ.get("SMTP_PASS")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_HOST = os.environ.get("SMTP_HOST")

ADMIN_EMAILS = os.environ.get("ADMIN_EMAILS")