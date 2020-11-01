import json
from ..config import Config
from ..db import cursor
from kafka import KafkaProducer, KafkaConsumer

KAFKA_BROKER_URL = Config().kafka_broker_url
KAFKA_TAXI_POSITION_TOPIC = Config().taxi_position_tp
KAFKA_PASSENGER_POSITION_TOPIC = Config().psgr_position_tp
KAFKA_SEARCH_RESULT_TOPIC = Config().search_result_tp
LATITUDE_OFFSET = 0.5
LONGITUDE_OFFSET = 0.3

producer = KafkaProducer(
    bootstrap_servers = [KAFKA_BROKER_URL],
    value_serializer = lambda m: json.dumps(m).encode('ascii')
)
taxi_pos_consumer = KafkaConsumer(
    KAFKA_TAXI_POSITION_TOPIC,
    bootstrap_servers = [KAFKA_BROKER_URL],
    value_deserializer = lambda m: json.loads(m.decode('ascii'))
)
psgr_pos_consumer = KafkaConsumer(
    KAFKA_PASSENGER_POSITION_TOPIC,
    bootstrap_servers = [KAFKA_BROKER_URL],
    value_deserializer = lambda m: json.loads(m.decode('ascii'))
)

def _json_result_of(passenger_id, rows):
    result = []
    for row in rows:
        result.append(
            {
                'taxi_id': row[1]
            }
        )
    return {
        'passenger_id': passenger_id,
        'result': result
    }

def track_taxi_position():
    for message in taxi_pos_consumer:
        value = message.value
        cursor.update_taxi_position(value['position']['latitude'], value['position']['longitude'], value['taxi_id'])

def handle_passenger_request():
    for message in psgr_pos_consumer:
        value = message.value
        passenger_id = value['passenger_id']
        latitude = value['position']['latitude']
        longitude = value['position']['longitude']
        rows = cursor.get_nearby_taxi(
            latitude - LATITUDE_OFFSET,
            latitude + LATITUDE_OFFSET,
            longitude - LONGITUDE_OFFSET,
            longitude + LONGITUDE_OFFSET
        )
        # We can check the result in consumer
        producer.send(KAFKA_SEARCH_RESULT_TOPIC, _json_result_of(passenger_id, rows))