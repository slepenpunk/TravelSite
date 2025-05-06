import os

from dotenv import load_dotenv

load_dotenv()
MODE = os.environ.get("MODE")
LOG_LEVEL = os.environ.get("LOG_LEVEL")

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

TEST_DB_HOST = os.environ.get("TEST_DB_HOST")
TEST_DB_PORT = os.environ.get("TEST_DB_PORT")
TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
TEST_DB_USER = os.environ.get("TEST_DB_USER")
TEST_DB_PASS = os.environ.get("TEST_DB_PASS")

SECRET_KEY = os.environ.get("SECRET_KEY")

REDIS_URL = os.environ.get("REDIS_URL")

SMTP_EMAIL = os.environ.get("SMTP_EMAIL")
SMTP_PASS = os.environ.get("SMTP_PASS")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_HOST = os.environ.get("SMTP_HOST")

ADMIN_EMAILS = os.environ.get("ADMIN_EMAILS")

EMAIL_USER_FOR_TESTS = os.environ.get("EMAIL_USER_FOR_TESTS")
PASSWORD_USER_FOR_TESTS = os.environ.get("PASSWORD_USER_FOR_TESTS")
