import json
import random
import time
from json.decoder import JSONDecodeError
from app.config import MAX_PACKAGE_LENGTH, ENCODING, ERRORS


class Chat:
    @staticmethod
    def get_message(sock):
        response = sock.recv(MAX_PACKAGE_LENGTH).decode(ENCODING)
        try:
            message = json.loads(response)
        except JSONDecodeError:
            message = "empty"
        return message

    @staticmethod
    def send_message(sock, message):
        message = json.dumps(message).encode(ENCODING)
        sock.send(message)

    @staticmethod
    def template_message(action="msg", **kwargs):
        message = {"action": action, "time": time.time()}
        for key, value in kwargs.items():
            message[key] = value
        return message

    @property
    def get_error(self):
        return random.choice(ERRORS)
