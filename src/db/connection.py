import pymysql

class Connection:
    def __init__(self, config):
        self.host = config.db_host
        self.port = config.db_port
        self.user = config.db_user
        self.password = config.db_password
        self.db = config.db_name
        self.connection = None

    def connect(self):
        try:
            if self.connection is None:
                self.connection = pymysql.connect(
                    host = self.host,
                    port = self.port,
                    user = self.user,
                    passwd = self.password,
                    db = self.db,
                    connect_timeout = 10
                )
                self.cursor = self.connection.cursor()
        except pymysql.MySQLError as e:
            print(e)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def fetch(self, sql, args = None, fetch_all = False):
        try:
            self.connect()
            result = self.cursor.execute(sql, args)
            return self.cursor.fetchall() if fetch_all else result
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconnect()

    def execute_one(self, sql, args = None):
        try:
            self.connect()
            self.cursor.execute(sql, args)
            self.connection.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconnect()

    def execute_many(self, sql, args):
        try:
            self.connect()
            self.cursor.executemany(sql, args)
            self.connection.commit()
        except pymysql.MySQLError as e:
            print(e)
        finally:
            self.disconnect()