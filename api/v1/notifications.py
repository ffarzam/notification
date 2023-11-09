import random

import httpx
from fastapi import APIRouter, Depends, status, Request
from redis import Redis

from config.config import settings
from services.celery_tasks import send_email_task, send_rss_update_notification_email_task
from db.redisdb import get_redis

from schemas.user import BaseNotification

routers = APIRouter(prefix="/v1")


@routers.post("/code_sender", status_code=status.HTTP_201_CREATED)
async def code_sender(request: Request, notification_info: BaseNotification, redis: Redis = Depends(get_redis)):
    random_number = str(random.randint(1000, 9999))
    await redis.set(random_number, notification_info.email, ex=120)

    unique_id = request.state.unique_id
    send_email_task.delay(notification_info.email, random_number, notification_info.action, unique_id)

    return {"A code was sent to the email"}


@routers.get("/rss_update_notif/{channel_id}/", status_code=status.HTTP_200_OK)
async def rss_update_notif(request: Request, channel_id: str,):

    channel_title = request.headers.get("channel_title")
    headers = {"unique_id": request.state.unique_id}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(f"{settings.PODCAST_USER_BOOKMARKED_CHANNEL_URL}{channel_id}/", headers=headers)
    if response.status_code == 200:
        data = response.json()
        if len(data) != 0:
            async with httpx.AsyncClient(headers=headers) as client:
                response = await client.post(settings.ACCOUNT_GET_USER_EMAIL_URL, json={"data": data})
            email_list = response.json()
            send_rss_update_notification_email_task.delay(email_list, channel_title, "rss_update_notification",
                                                          request.state.unique_id)
