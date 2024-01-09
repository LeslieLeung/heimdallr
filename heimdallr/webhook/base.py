from typing import Any, Tuple


class WebhookBase:
    message: Any

    def __init__(self, message: Any):
        self.message = message

    def parse(self) -> Tuple[str, str, str]:
        """
        Parse the message to be sent.
        :return: title, content, url
        """
        return "", "", ""
