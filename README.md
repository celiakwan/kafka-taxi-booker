# kafka-taxi-booker
An application built with Python and Kafka connecting to MySQL to simulate how to find taxis nearby based on passengers' positions.

### Version
- [Python](https://www.python.org/): 3.8.5
- [Apache Kafka](https://kafka.apache.org/): 2.13-2.6.0
- [MySQL](https://www.mysql.com/): 8.0.21

### Installation
Install the required Python packages in this project.
```
pip3 install -r requirements.txt
```

### Database
Connect to MySQL and run the SQL commands in `sql_script/init.sql` to create the database `taxi_booker` and the table `taxi_position`.

### Kafka Environment
Start a ZooKeeper server.
```
./bin/zookeeper-server-start.sh config/zookeeper.properties
```

Start a Kafka broker.
```
./bin/kafka-server-start.sh config/server.properties
```

Create topics.

1. Taxi positions will be continuously sent to `taxi-position` and stored in database so that we can track the real-time locations of the taxis.
    ```
    ./bin/kafka-topics.sh --create --topic taxi-position --bootstrap-server localhost:9092
    ```

2. Passenger requests that include their current positions will be sent to `passenger-position`. Once the application receives the requests, it will search for taxis within a certain range from the latest position records in database.
    ```
    ./bin/kafka-topics.sh --create --topic passenger-position --bootstrap-server localhost:9092
    ```

3. Lastly, the search result will be sent to `search-result`.
    ```
    ./bin/kafka-topics.sh --create --topic search-result --bootstrap-server localhost:9092
    ```

Start a consumer to see the search result.
```
./bin/kafka-console-consumer.sh --topic search-result --bootstrap-server localhost:9092
```

### Configuration
Environment configuration for this project is available in `config.yaml`.

### Get Started
Run the application.
```
/usr/local/bin/python3 -m src.main
```

Run the message generator to simulate messages sent from client devices.
```
/usr/local/bin/python3 -m src.mock.generator
```