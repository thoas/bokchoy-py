import nsq
import threading
import os
import random
import time

from itertools import chain


class ConnectionError(Exception):
    pass


class SyncConn(nsq.SyncConn):
    def close(self):
        return self.s.close()


class ConnectionPool(object):
    def __init__(self, addresses,
                 connection_class=SyncConn,
                 heartbeat_interval=30,
                 max_connections=None):

        max_connections = max_connections or 2 ** 31
        if not isinstance(max_connections, int) or max_connections < 0:
            raise ValueError('"max_connections" must be a positive integer')

        self.connection_class = connection_class
        self.heartbeat_interval = heartbeat_interval * 1000
        self.addresses = addresses
        self.callback_queue = []
        self.max_connections = max_connections
        self.last_recv_timestamp = time.time()
        self.id = 'pool'

        self.reset()

    def reset(self):
        self.pid = os.getpid()
        self._created_connections = 0
        self._available_connections = []
        self._in_use_connections = set()
        self._check_lock = threading.Lock()

    def _checkpid(self):
        if self.pid != os.getpid():
            with self._check_lock:
                if self.pid == os.getpid():
                    # another thread already did the work while we waited
                    # on the lock.
                    return
                self.disconnect()
                self.reset()

    def get_connection(self):
        "Get a connection from the pool"
        self._checkpid()
        try:
            connection = self._available_connections.pop()
        except IndexError:
            connection = self.make_connection()
        self._in_use_connections.add(connection)
        return connection

    def make_connection(self):
        "Create a new connection"
        if self._created_connections >= self.max_connections:
            raise ConnectionError("Too many connections")

        self._created_connections += 1
        self.last_recv_timestamp = time.time()

        address = random.choice(self.addresses)

        host, port = address.split(':')

        conn = self.connection_class()
        conn.connect(host, int(port))

        return conn

    def release(self, connection):
        "Releases the connection back to the pool"
        self._checkpid()
        if connection.pid != self.pid:
            return
        self._in_use_connections.remove(connection)
        self._available_connections.append(connection)

    def close(self):
        "Disconnects all connections in the pool"
        all_conns = chain(self._available_connections,
                          self._in_use_connections)
        for connection in all_conns:
            connection.close()

    def send(self, data):
        return self.get_connection().send(data)
