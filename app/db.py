from abc import ABC, abstractmethod
import psycopg2
from psycopg2 import OperationalError
from datetime import datetime


class DatabaseManager(ABC):
    def __init__(self):
        self.is_connected = False
        self.last_error = None
        self.connect_time = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self, conn):
        pass

    def _handle_error(self, error):
        self.last_error = error
        print(f"Error: {error}")


class PostgreSQLManager(DatabaseManager):
    REQUIRED_CONFIG_KEYS = {'dbname', 'user', 'password', 'host', 'port'}

    def __init__(self, config):
        self._validate_config(config)
        self.config = config
        self.connection_str = self._build_connection_str()

    def _validate_config(self, config):
        """ Verify that the configuration contains all the required keys """
        missing_keys = self.REQUIRED_CONFIG_KEYS - config.keys()
        if missing_keys:
            raise ValueError(f"Missing configuration keys: {', '.join(missing_keys)}")

    def _build_connection_str(self):
        """ Build the connection string from the configuration """
        return f"dbname={self.config['dbname']} user={self.config['user']} password={self.config['password']} host={self.config['host']} port={self.config['port']}"

    def connect(self):
        try:
            print('Connecting to PostgreSQL Database...')
            conn = psycopg2.connect(self.connection_str)
            self.is_connected = True
            self.connect_time = datetime.now()
            return conn
        except OperationalError as e:
            self._handle_error(e)
            return None

    def disconnect(self, conn):
        if conn:
            print('Disconnecting from PostgreSQL Database...')
            conn.close()
            self.is_connected = False
