import smtplib
from email.message import EmailMessage
from pathlib import Path

from app.email_config import (
    SMTP_SERVER,
    SMTP_PORT,
    SENDER_EMAIL,
    SENDER_PASSWORD,
    RECIPIENT_EMAIL
)


def send_daily_report(report_path: str):
    msg = EmailMessage()
    msg["Subject"] = "Daily Investment Report"
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL

    msg.set_content("Your daily investment report is attached.")

    path = Path(report_path)
    with open(path, "rb") as f:
        file_data = f.read()
        file_name = path.name

    msg.add_attachment(
        file_data,
        maintype="text",
        subtype="plain",
        filename=file_name
    )

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return {"status": "sent"}

    except Exception as e:
        return {"status": "error", "message": str(e)}
