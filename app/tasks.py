from loguru import logger
import time
from .celery import app
from celery import chain, group, chord
import requests
from .constants import DATA


@app.task
def test_request_task(serial: int, data: dict, result_return: bool = False, *args):
    start_time = time.perf_counter()
    logger.info(f"{serial} : Started with data = {data}")
    try:
        _url = data.pop("url")
        # resp = requests.post(_url, data=data)
        logger.info(f"{serial} : Finished with data = {data}")
    except Exception as e:
        logger.error(f"{serial} : ERROR: {e.__str__()}")
    if result_return:
        return start_time


@app.task
def test_chord_callback_task(result):
    logger.info("######################################################################\nGroup tasks finished")
    now = time.perf_counter()
    time_since_first_invocation = now - result[0]
    if time_since_first_invocation < 1.0:
        logger.info(f"======================================SLEEPING {1.0 - time_since_first_invocation}")
        time.sleep(1.0 - time_since_first_invocation)
    return time.perf_counter()


@app.task
def test_chain_of_chord_callback_task(result):
    logger.info("######################################################################\nChain of chord finished")


@app.task
def test_chain_of_chords_with_chain_callback():
    group_size = 10
    chain_size = 30
    logger.info("Preparing chord of chords")
    chain_sig = chain(
        *(
            chord(
                (
                    test_request_task.si(serial, data, True)
                    for serial, data in zip(range(i + 1, i + group_size + 1), DATA[i:i + group_size])
                ),
                test_chord_callback_task.s()
            ) for i in range(0, len(DATA), group_size)
        ),
        test_chain_of_chord_callback_task.s()
    )
    logger.info("Firing chord of chords")
    chain_sig.delay()
