import socket
import time


class ClientError(Exception):
    """ Main class exception client"""
    pass


class ClientSocketError(ClientError):
    """ The exception thrown by the client in case of a network error """
    pass


class ClientProtocolError(ClientError):
    """ The exception thrown by the client in case of a protocol error"""
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.host = host
        self.port = port
        try:
            self.connection = socket.create_connection((host, port), timeout)
        except socket.error as err:
            raise ClientSocketError("error create connection", err)

    def _read(self):
        """Метод для чтения ответа сервера"""
        data = b""
        
        while not data.endswith(b"\n\n"):
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientSocketError("error recv data", err)

        decoded_data = data.decode()

        status, payload = decoded_data.split("\n", 1)
        payload = payload.strip()

        if status == "error":
            raise ClientProtocolError(payload)

        return payload

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or int(time.time())

        try:
            self.connection.sendall(
                f"put {key} {value} {timestamp}\n".encode()
            )
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        self._read()

    def get(self, key):
        try:
            self.connection.sendall(
                f"get {key}\n".encode()
            )
        except socket.error as err:
            raise ClientSocketError("error send data", err)

        # read answer
        payload = self._read()
        # print(payload)

        data = {}
        if payload == "":
            return data

        for row in payload.split("\n"):
            key, value, timestamp = row.split()
            if key not in data:
                data[key] = []
            data[key].append((int(timestamp), float(value)))

        return data

    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientSocketError("error close connection", err)


def main():
    client = Client("127.0.0.1", 10001, timeout=5)
    # client.put("test", 0.5, timestamp=1)
    # client.put("test", 2.0, timestamp=2)
    # client.put("test", 0.5, timestamp=3)
    # client.put("load", 3, timestamp=4)
    # client.put("load", 4, timestamp=5)
    print(client.get("*"))

    client.close()


if __name__ == "__main__":
    main()
