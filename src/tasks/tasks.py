import smtplib

from pydantic import EmailStr

from tasks.celery import celery
from PIL import Image
from pathlib import Path
from config import SMTP_EMAIL, SMTP_HOST, SMTP_PASS, SMTP_PORT

from tasks.email_message import create_booking_confirmation


@celery.task
def process_pic(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized = image.resize((500, 500))
    image_resized.save(f"static/images/resized_1000_500_{image_path.name}")


@celery.task
def send_booking_confirmation(booking: dict, email_to: EmailStr):
    message_to = email_to
    message_content = create_booking_confirmation(booking, message_to)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_EMAIL, SMTP_PASS)
        server.send_message(message_content)
