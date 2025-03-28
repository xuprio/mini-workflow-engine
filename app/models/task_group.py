from enum import Enum
from typing import Annotated
from __future__ import annotations
from pydantic import AfterValidator, BaseModel

from app.config.tasks import TASK_SWITCHER

class Mode(Enum):
    PARALLEL = 'parallel'
    SEQUENCE = 'sequence'

class TaskGroup(BaseModel):
    mode: Mode
    tasks: list[
        Annotated[str, AfterValidator(lambda task: task in TASK_SWITCHER.keys())] | 
        TaskGroup
    ]
