import asyncio
import json
import httpx
import pika
import structlog

from config.config import get_settings
from config.log_config import configure_logging

settings = get_settings()

configure_logging()
logger = structlog.get_logger("elastic_logger")


def start_consumers(queue_name):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    ch = connection.channel()

    ch.queue_declare(queue=queue_name)
    callback_func = callback_mapper(queue_name)
    ch.basic_consume(queue=queue_name, on_message_callback=callback_func)

    ch.start_consuming()


def callback_mapper(arg):
    callback_select = {
        "notification_rss_feed_update": rss_feed_update,

    }
    return callback_select[arg]


def rss_feed_update(ch, method, properties, body):
    body = json.loads(body)

    headers = {"unique_id": body["unique_id"], "channel_title": body['channel_title']}

    async def async_func():
        async with httpx.AsyncClient(headers=headers) as client:
            await client.get(
                f"{settings.NOTIFICATION_RSS_UPDATE_NOTIF_URL}{body['channel_id']}/",
                headers=headers)

    asyncio.run(async_func())

    log_entry = {
        "unique_id": body["unique_id"],
        "channel_id": body['channel_id'],
        'delivery_tag': method.delivery_tag,
    }
    logger.info("notification.consumer.rss_feed", **log_entry)
    ch.basic_ack(delivery_tag=method.delivery_tag)
