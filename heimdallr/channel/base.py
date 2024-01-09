from typing import Tuple


class Message:
    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body


class Channel:
    """
    Base class for all channels.
    """

    def __init__(self, message: Message, name: str) -> None:
        self.name = name
        self.message = message

    def compose_message(self) -> str:
        """
        Compose the message to be sent.
        """
        return ""

    def send(self) -> Tuple[bool, str]:
        """
        Send a message to the channel.
        """
        return False, ""

    def get_name(self) -> str:
        """
        Get the name of the channel.
        """
        return self.name

    def get_credential(self) -> None:
        """
        Get the credential of the channel.
        """
        pass
