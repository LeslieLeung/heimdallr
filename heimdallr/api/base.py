from env import get_env
from heimdallr.channel import (
    Bark,
    BarkMessage,
    Chanify,
    ChanifyMessage,
    Channel,
    Email,
    EmailMessage,
    Message,
    PushDeer,
    PushDeerMessage,
    Pushover,
    PushoverMessage,
    WecomApp,
    WecomMessage,
    WecomWebhook,
)
from heimdallr.response import Response, success


def serve(
    channel: str, title: str = "", body: str = "", key: str = "", jump_url: str = ""
):
    env = get_env()
    if env.key != "" and key != env.key:
        return {"code": -1, "message": "key not authorized"}
    channels = channel.split("+")
    senders = []
    for chan in channels:
        message: Message
        sender: Channel
        match chan:
            case "bark":
                message = BarkMessage(title, body, jump_url)
                sender = Bark(message)
            case "wecom-webhook":
                message = WecomMessage(title, body)
                sender = WecomWebhook(message)
            case "wecom-app":
                message = WecomMessage(title, body)
                sender = WecomApp(message)
            case "pushdeer":
                message = PushDeerMessage(title, body)
                sender = PushDeer(message)
            case "pushover":
                message = PushoverMessage(title, body)
                sender = Pushover(message)
            case "chanify":
                message = ChanifyMessage(title, body)
                sender = Chanify(message)
            case "email":
                message = EmailMessage(title, body)
                sender = Email(message)
            case _:
                return {"code": 2, "message": f"{chan} is not supported"}
        senders.append(sender)

    errors = {}
    for sender in senders:
        rs, msg = sender.send()
        if not rs:
            errors[sender.get_name()] = msg

    if len(errors) == 0:
        return success()
    err_msg = ""
    for err in errors.items():
        err_msg += f"{err[0]} return: {err[1]}."
    return Response(1, err_msg).render()
