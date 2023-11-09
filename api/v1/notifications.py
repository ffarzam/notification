import random

from fastapi import APIRouter, Depends, status, Request
from redis import Redis

from services.celery_tasks import send_email_task
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
