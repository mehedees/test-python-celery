from contextlib import asynccontextmanager
from eventlet import monkey_patch
from fastapi import FastAPI
from loguru import logger

from .db_client import connect_to_db_async, shutdown_db_async
from .db_model import TestModel
from .tasks import test_chain_of_chords_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    monkey_patch()
    await connect_to_db_async()
    yield
    await shutdown_db_async()


app = FastAPI(lifespan=lifespan, debug=True)


@app.get(path='/start/{group_size}/{chain_size}')
async def start_task(group_size: int, chain_size: int):
    logger.info(f"Starting task with {chain_size} chained groups each containing {group_size} tasks and callback")
    test_chain_of_chords_task.delay(group_size, chain_size)

    return {'success': 'True'}


@app.get(path='/test_request')
async def test_request(serial: int):
    logger.info(f"Got request {serial}")
    TestModel(req_number=serial).update(req_rec=True)
    return {'success': True}
