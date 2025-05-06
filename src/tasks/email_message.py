from email.message import EmailMessage

from pydantic import EmailStr

from config import SMTP_EMAIL


def create_booking_confirmation(
    booking: dict,
    email_to: EmailStr,
):
    email = EmailMessage()
    email["Subject"] = "Booking confirmation"
    email["From"] = SMTP_EMAIL
    email["To"] = email_to

    email.set_content(
        """
            <h1>Booking confirmation</h1>
        """,
        subtype="html",
    )
    return email
