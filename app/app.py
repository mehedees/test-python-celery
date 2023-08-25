from fastapi import FastAPI, Body
from loguru import logger

from .tasks import send_newsletter_welcome_email_task


app = FastAPI(
    debug=True,
    title="Test Python Celery (Basic)",
    description="Test basics of Python Celery",
    openapi_url=f"/openapi.json",
)


@app.post(path='/newsletter/signup')
async def newsletter_signup(email: str = Body(embed=True)):
    logger.info(f"Received newsletter signup request from {email}")
    # Doing some processing bla bla bla
    logger.info("Initiating welcome email sending task")
    send_newsletter_welcome_email_task.delay(email)
    # Return response now, celery will take care of sending the welcome mail
    return {
        'success': 'True',
        'code': 200,
    }
