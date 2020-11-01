import yaml

class Config:
    def __init__(self):
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)

            db_config = config['database']
            self.db_host = db_config['host']
            self.db_port = db_config['port']
            self.db_user = db_config['user']
            self.db_password = db_config['password']
            self.db_name = db_config['dbName']

            kafka_config = config['kafka']
            kafka_host = kafka_config['host']
            kafka_port = kafka_config['port']
            self.kafka_broker_url = f'{kafka_host}:{kafka_port}'
            self.taxi_position_tp = kafka_config['taxiPositionTopic']
            self.psgr_position_tp = kafka_config['passengerPositionTopic']
            self.search_result_tp = kafka_config['searchResultTopic']

            generator_config = config['generator']
            self.total_taxi = generator_config['totalTaxi']
            self.psgr_per_time_slot = generator_config['passengerPerTimeSlot']
            self.duration = generator_config['duration']