from datetime import date

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


@celery_app.task()
def send_weekly_newsletter_email_task():
    logger.info(f"Send weekly newsletter email task received")
    email: str = 'test.celery@mehedees.dev'  # let's assume we collected it from DB
    with SMTP(
            host="smtp.freesmtpservers.com",
            port=25,
            timeout=60,
    ) as smtp:
        from_addr = "newsletter@mehedees.dev"
        smtp.sendmail(
            from_addr=from_addr,
            to_addrs=email,
            msg=f"To:{email}\nFrom: {from_addr}\r\nSubject: Weekly Newsletter\n\nNo new news this week!",
        )
        logger.info("Email successfully sent")
    logger.info(f"Send weekly newsletter email task finished")
    return email


@celery_app.task()
def collect_daily_news_for_newsletter_task():
    news_date = date.today()
    logger.info(f"Collect daily news of {news_date.isoformat()} for newsletter task received")
    # Collecting news of news_date
    logger.info(f"Collect daily news for newsletter task finished")
