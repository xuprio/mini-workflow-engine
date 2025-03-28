from fastapi import FastAPI

from .routers import workflow

app = FastAPI()

app.include_router(workflow.router, prefix='/workflow')

@app.get('/status')
def status():
    return {'status': 'alive'}
