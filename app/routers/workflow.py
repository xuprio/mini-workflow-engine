from uuid import uuid4
from http import HTTPStatus
from fastapi import APIRouter, BackgroundTasks

from app.utils.tasks import run_task_group
from app.models.task_group import TaskGroup
from app.utils.status import get_task_status


router = APIRouter()

@router.post('/')
def start_workflow(task_group: TaskGroup, background_tasks: BackgroundTasks, status_code=HTTPStatus.ACCEPTED):
    workflow_id = str(uuid4())

    background_tasks.add_task(run_task_group, workflow_id, task_group)
    
    return {'id': workflow_id}


@router.get('/status/{workflow_id}/{task_id}')
def get_status(workflow_id: str, task_id: str):
    return {'status': get_task_status(workflow_id, task_id)}
