from .config import Config
from .db import cursor
from .app import taxi_search
from threading import Thread

TOTAL_TAXI = Config().total_taxi

def _handle_taxi_messages():
    taxi_search.track_taxi_position()

def _handle_passenger_messages():
    taxi_search.handle_passenger_request()

if __name__ == '__main__':
    # Initialize taxi position entries in database
    if cursor.get_row_count() == 0:
        cursor.create_account(TOTAL_TAXI)

    thread1 = Thread(target = _handle_taxi_messages)
    thread2 = Thread(target = _handle_passenger_messages)

    # The threads will be killed if the main thread exits
    # Do this in case we want to terminate the program suddenly like Ctrl+C
    thread1.daemon = True
    thread2.daemon = True

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()