from typing import Any, Tuple


class Message:
    def __init__(self, title: str, body: str) -> None:
        self.title = title
        self.body = body

    def render_message(self) -> Any:
        """
        Render the message to the format that the channel can understand.
        """


class Channel:
    """
    Base class for all channels.
    """

    def __init__(self, name: str, type: str) -> None:
        self.name = name
        self.type = type

    def _build_channel(self) -> None:
        """
        Get the credential of the channel.
        """

    def send(self, message: Message) -> Tuple[bool, str]:
        """
        Send a message to the channel.
        """
        return False, ""

    def get_name(self) -> str:
        """
        Get the name of the channel.
        """
        return self.name

    def get_type(self) -> str:
        """
        Get the type of the channel.
        """
        return self.type

    def get_config_name(self) -> str:
        """
        Get the name of the channel in config.
        """
        return str.upper(self.name)
