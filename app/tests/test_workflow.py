from time import sleep
from fastapi import status
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_sequential(capsys):
    res = client.post('/workflow', json={
        "mode": "sequence",
        "tasks": [
            "task_c", 
            "task_b"
        ]
    })

    assert res.status_code == status.HTTP_202_ACCEPTED

    sleep(5) # sleep to give tasks time to complete

    tasks = capsys.readouterr()

    assert tasks.out == 'Running task C\nRunning task B\n'


def test_parallel(capsys):
    res = client.post('/workflow', json={
        "mode": "parallel",
        "tasks": [
            "task_a",
            "task_b"
        ]
    })

    assert res.status_code == status.HTTP_202_ACCEPTED

    sleep(5) # sleep to give tasks time to complete

    tasks = capsys.readouterr()

    assert tasks.out == 'Running task A\nRunning task B\n' or tasks.out == 'Running task B\nRunning task A\n'


def test_mixed(capsys):
    res = client.post('/workflow', json={
        "mode": "parallel",
        "tasks": [
            "task_a",
            {
                "mode": "sequence",
                "tasks": ["task_b", "task_c"]
            }, 
        ]
    })

    assert res.status_code == status.HTTP_202_ACCEPTED

    sleep(5) # sleep to give tasks time to complete

    tasks = capsys.readouterr()

    assert tasks.out == 'Running task A\nRunning task B\nRunning task C\n' or tasks.out == 'Running task B\nRunning task C\nRunning task A\n'
