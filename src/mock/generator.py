import uuid
import json
from .position import mock_latitude, mock_longitude
from ..config import Config
from ..util import util
from kafka import KafkaProducer
from threading import Thread
from random import randint
from time import sleep

KAFKA_BROKER_URL = Config().kafka_broker_url
KAFKA_TAXI_POSITION_TOPIC = Config().taxi_position_tp
KAFKA_PASSENGER_POSITION_TOPIC = Config().psgr_position_tp
TOTAL_TAXI = Config().total_taxi
PASSENGER_PER_TIME_SlOT = Config().psgr_per_time_slot
DURATION = Config().duration

finish = False
taxi_pos_producer = KafkaProducer(
    bootstrap_servers = [KAFKA_BROKER_URL],
    value_serializer = lambda m: json.dumps(m).encode('ascii')
)
psgr_pos_producer = KafkaProducer(
    bootstrap_servers = [KAFKA_BROKER_URL],
    value_serializer = lambda m: json.dumps(m).encode('ascii')
)

def _mock_taxi_message(i):
    return {
        'taxi_id': util.mock_taxi_id(i),
        'position': {
            'latitude': mock_latitude(),
            'longitude': mock_longitude()
        }
    }

def _mock_passenger_message():
    return {
        'passenger_id': str(uuid.uuid4()),
        'position': {
            'latitude': mock_latitude(),
            'longitude': mock_longitude()
        }
    }    

def _send_taxi_message():
    while True:
        if finish:
            break
        else:
            for i in range(TOTAL_TAXI):
                # Send messages in JSON format
                taxi_pos_producer.send(KAFKA_TAXI_POSITION_TOPIC, _mock_taxi_message(i))
            # Update taxi position every 10s
            sleep(10)

def _send_passenger_message():
    while True:
        if finish:
            break
        else:
            for _ in range(PASSENGER_PER_TIME_SlOT):
                # Send messages in JSON format
                psgr_pos_producer.send(KAFKA_PASSENGER_POSITION_TOPIC, _mock_passenger_message())
            # Random number of requests per second
            sleep_time = randint(0, 5)
            sleep(sleep_time)

if __name__ == '__main__':
    thread1 = Thread(target = _send_taxi_message)
    thread2 = Thread(target = _send_passenger_message)

    # The threads will be killed if the main thread exits
    # Do this in case we want to terminate the program suddenly like Ctrl+C
    thread1.daemon = True
    thread2.daemon = True

    thread1.start()
    thread2.start()

    sleep(DURATION)
    finish = True

    thread1.join()
    thread2.join()