from enum import Enum
from redis import Redis

from ..config.redis import redis_pool


class Status(Enum):
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'
    PENDING = 'PENDING'
    RUNNING = 'RUNNING'


def update_task_status(uuid: str, task_name: str, status: Status):
    with Redis(connection_pool=redis_pool) as conn:
        conn.set(f'{uuid}:{task_name}', status.value)


def create_task_status(uuid: str, task_name: str):
    update_task_status(uuid, task_name, Status.PENDING)
