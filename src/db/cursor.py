from .connection import Connection
from ..config import Config
from ..util import util

db = Connection(Config())
POSITION_TABLE = 'taxi_position'

def get_row_count():
    return db.fetch(
        f'SELECT * FROM {POSITION_TABLE}'
    )

def create_account(num):
    args = []
    for i in range(num):
        # Simply use sequential number to generate fixed-length taxi_id so that they could be reproduced in mock.generator
        # In real cases, it could be UUID
        taxi_id = util.mock_taxi_id(i)
        args.append((taxi_id, None, None))
    db.execute_many(
        f'INSERT INTO {POSITION_TABLE} (taxi_id, latitude, longitude) VALUES (%s, %s, %s)',
        args
    )

def update_taxi_position(latitude, longitude, taxi_id):
    db.execute_one(
        f'UPDATE {POSITION_TABLE} SET latitude = %s, longitude = %s WHERE taxi_id = %s',
        (latitude, longitude, taxi_id)
    )

def get_nearby_taxi(min_latitude, max_latitude, min_longitude, max_longitude):
    return db.fetch(
        f'SELECT * FROM {POSITION_TABLE} WHERE (latitude BETWEEN %s AND %s) AND (longitude BETWEEN %s AND %s)',
        (min_latitude, max_latitude, min_longitude, max_longitude),
        True
    )