from __future__ import annotations

from enum import Enum
from typing import Annotated
from pydantic import AfterValidator, BaseModel

from app.config.tasks import TASK_SWITCHER

def validate_task(task: str):
    if task not in TASK_SWITCHER.keys():
        raise ValueError(f'Task #{task} not recognized')
    
    return task

class Mode(Enum):
    PARALLEL = 'parallel'
    SEQUENCE = 'sequence'

class TaskGroup(BaseModel):
    mode: Mode
    tasks: list[
        Annotated[str, AfterValidator(validate_task)] | 
        TaskGroup
    ]
