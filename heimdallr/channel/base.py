class Message:
    def __init__(self, title: str, body: str):
        self.title = title
        self.body = body


class Channel:
    """
    Base class for all channels.
    """

    def __init__(self, message: Message, name: str):
        self.name = name
        self.message = message

    def compose_message(self):
        """
        Compose the message to be sent.
        """
        pass

    def send(self):
        """
        Send a message to the channel.
        """
        pass

    def get_name(self):
        """
        Get the name of the channel.
        """
        return self.name

    def get_credential(self):
        """
        Get the credential of the channel.
        """
        pass
