import structlog
from celery import Celery, Task
import asyncio

from config.config import get_settings
from config.log_config import configure_logging

settings = get_settings()
celery = Celery(__name__, include=["services.celery_tasks"])
celery.conf.broker_url = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/3'
celery.conf.result_backend = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/4'


configure_logging()
logger = structlog.get_logger("elastic_logger")


class CustomTask(Task):

    def retry(self, args=None, kwargs=None, exc=None, throw=True,
              eta=None, countdown=None, max_retries=None, **options):
        retry_count = self.request.retries
        log_data = {
            "task_name": self.name.split(".")[-1],
            "unique_id": self.request.args[-1],
            "exe": str(exc),
            'correlation_id': self.request.correlation_id,
            "attempt_on": retry_count + 1,
            'status': "retry"
        }
        if retry_count != max_retries:
            logger.error(f"notification.celery.{self.name}", **log_data)
        else:
            log_data['status'] = "fail"
            log_data['exception'] = True
            del log_data["attempt_on"]

            async def asyncfunc():
                await logger.critical(f"exception.notification.celery", **log_data)

            asyncio.run(asyncfunc())

        super().retry(args, kwargs, exc, throw, eta, countdown, max_retries, **options)

    def on_success(self, retval, task_id, args, kwargs):
        retry_count = self.request.retries

        log_data = {
            "task_name": self.name.split(".")[-1],
            "unique_id": self.request.args[-1],
            'correlation_id': self.request.correlation_id,
            "attempt_on": retry_count + 1,
            'status': "success"
        }

        async def asyncfunc():
            await logger.info(f"notification.celery", **log_data)

        asyncio.run(asyncfunc())
