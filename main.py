from app.tasks import test_task
import time


if __name__ == "__main__":
    for i in range(20):
        send_test_request.delay(i)
        time.sleep(5)
