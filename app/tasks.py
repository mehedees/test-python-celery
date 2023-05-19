from celery import chain, group, chord
from loguru import logger
import requests
import time

from .db_model import TestModel
from .worker import celery_app


@celery_app.task(ignore_result=False)
def test_request_task(serial: int):
    """
    The unit task.
    :param serial: int
    :return: starting time of this task
    """
    logger.info(f"Task {serial} started")
    start_time = time.time()
    TestModel.objects.create(req_number=serial, req_exec=True)
    try:
        resp = requests.get(f"http://mock_app:10034/test_request?serial={serial}")
        TestModel(req_number=serial).update(rec_ack=True)
    except Exception as e:
        logger.error(f"Task {serial} - ERROR: {e.__str__()}")
    return start_time


@celery_app.task
def test_chord_callback_task(start_times: list[float]):
    """
    Task to ensure I don't execute more than n test_request_task in 1 sec.
    If all test_request_task complete under 1 sec then sleep for the remainder of that sec,
    Otherwise do nothing.
    :param start_times: list[float]
    """
    now = time.time()
    logger.info(f"Group tasks finished")
    time_since_first_task_in_grp = now - start_times[0] if len(start_times) > 0 else 0
    if time_since_first_task_in_grp < 1.0:
        sleep_time_sec = 1.0 - time_since_first_task_in_grp
        logger.info(f"SLEEPING {sleep_time_sec}")
        time.sleep(sleep_time_sec)


@celery_app.task
def test_chain_of_chord_callback_task():
    """
    Just another task that runs after all tasks have finished executing
    :return:
    """
    logger.info("Chain of chord finished")


@celery_app.task
def test_chain_of_chords_task(group_size: int, chain_size: int):
    """
    Make chord with a group of group_size test_request_task to run in parallel and ensure 1 sec completion,
    with callback test_chord_callback_task.
    Make chain_size numbers of above chords and chain them with additional test_chain_of_chord_callback_task.
    :param group_size:
    :param chain_size:
    """
    total_size = group_size * chain_size
    chords = (
        chord(
            group(
                test_request_task.si(serial)
                for serial in range(i, i + group_size)
            ),
            test_chord_callback_task.s()
        ) for i in range(0, total_size, group_size)
    )
    chain_of_chords_with_callback = chain(
        *chords,
        test_chain_of_chord_callback_task.si()
    )
    logger.info("Firing chain of chords")
    chain_of_chords_with_callback.delay()


@celery_app.task
def test_chunk(size: int):
    global DATA
    dataset = DATA[0:size]
    del DATA[0:size]
    logger.info(f"starting [{dataset[0]}-{dataset[-1]}] at {time.time()}")
    start = time.time()
    group_sig = group(test_request_task.si(i) for i in dataset)
    res = group_sig.apply_async()
    # res = test_request_task.map(dataset).apply_async()
    # while not res.ready():
    #     time_since_first_invocation = time.time() - start
    #     if time_since_first_invocation < 1.0:
    #         logger.info(f"=========sleeping 0.1")
    #         time.sleep(0.1)
    #     else:
    #         break
    now = time.time()
    time_since_first_invocation = now - start
    if 1 > time_since_first_invocation > 0:
        sleep_time = 1 - time_since_first_invocation
        logger.info(f"================================SLEEPING {sleep_time}")
        time.sleep(sleep_time)
    logger.info(f"Finishing {dataset[0]}-{dataset[-1]}")
    return
    # chord(group_sig)(test_chord_callback_task.si(start, dataset[0], dataset[-1]))
    # group_sig.apply_async((), link=test_chord_callback_task.si(start, dataset[0], dataset[-1]))
