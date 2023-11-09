import asyncio

from celery import shared_task

from config.celery import CustomTask
from services.send_email import send_email


class BaseTaskWithRetry(CustomTask):
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 5}
    retry_backoff = True
    retry_jitter = False
    task_acks_late = True
    task_time_limit = 60


@shared_task(base=BaseTaskWithRetry)
def send_email_task(email, random_number, action, _):
    async def async_func():
        await send_email([email], random_number, action)
    asyncio.run(async_func())
    return True


@shared_task(base=BaseTaskWithRetry)
def send_rss_update_notification_email_task(emails, channel_name, action, _):
    async def async_func():
        await send_email(emails, channel_name, action)
    asyncio.run(async_func())
    return True
