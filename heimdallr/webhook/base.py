from typing import Any


class WebhookBase:
    message: Any

    def __init__(self, message: Any):
        self.message = message

    def parse(self) -> (str, str, str):
        """
        Parse the message to be sent.
        return: (title, body)
        """
        pass
