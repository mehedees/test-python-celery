from loguru import logger
from smtplib import SMTP

from .worker import celery_app


@celery_app.task()
def send_newsletter_welcome_email_task(email: str):
    logger.info(f"Send welcome email task received")
    with SMTP(
            host="smtp.freesmtpservers.com",
            port=25,
            timeout=60,
    ) as smtp:
        from_addr = "newsletter@mehedees.dev"
        smtp.sendmail(
            from_addr=from_addr,
            to_addrs=email,
            msg=f"To:{email}\nFrom: {from_addr}\r\nSubject: Welcome\n\nWelcome to the newsletter!",
        )
        logger.info("Email successfully sent")
    logger.info(f"Send welcome email task finished")
    return email
