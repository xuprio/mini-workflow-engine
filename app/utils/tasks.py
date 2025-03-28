from threading import Thread
from functools import partial

from app.config.tasks import TASK_SWITCHER
from app.utils.status import Status, create_task_status, update_task_status

from ..models.task_group import Mode, TaskGroup


def create_single(parent_uuid: str, task: TaskGroup | str):
    return Thread(target=run_task if isinstance(task, str) else run_task_group, args=(parent_uuid, task))


def create_sequential(parent_uuid: str, task_group: list[TaskGroup | str]):
    def run_in_sequence(parent_uuid: str, task_group: list[TaskGroup | str]):
        return list(map(lambda task: run_task(parent_uuid, task) if isinstance(task, str) else run_task_group(parent_uuid, task), task_group))
    
    for task in task_group:
        if isinstance(task, str):
            create_task_status(parent_uuid, task)

    return [Thread(run_in_sequence, (parent_uuid, task_group))]


def run_task(parent_uuid: str, task_id: str):
    update_task_status(parent_uuid, task_id, Status.RUNNING)
    res = TASK_SWITCHER[task_id]()
    update_task_status(parent_uuid, task_id, Status.SUCCESS if res else Status.FAILURE)


def run_task_group(parent_uuid: str, group: TaskGroup):
    match group.mode:
        case Mode.PARALLEL:
            threads = list(map(
                partial(create_single, parent_uuid), 
                group.tasks
            ))

            for thread in threads:
                thread.start()
        case Mode.SEQUENCE:
            threads = create_sequential(parent_uuid, group.tasks)

    for thread in threads:
        thread.join()