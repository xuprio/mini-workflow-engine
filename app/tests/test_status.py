from time import sleep
from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_status():
    res = client.post('/workflow', json={
        "mode": "sequence",
        "tasks": [
            "task_a",
            "task_c", 
            "task_b"
        ]
    })

    sleep(5) # sleep to give tasks time to complete

    uuid = res.json()['id']

    status_a = client.get(f'/workflow/status/{uuid}/task_a')
    status_b = client.get(f'/workflow/status/{uuid}/task_b')
    status_c = client.get(f'/workflow/status/{uuid}/task_c')

    assert status_a.json()['status'] == 'SUCCESS'
    assert status_b.json()['status'] == 'SUCCESS'
    assert status_c.json()['status'] == 'FAILURE'
