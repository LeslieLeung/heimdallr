from heimdallr.channel.factory import build_message
from heimdallr.response import Response, success
from heimdallr.shared.config import Config


def serve(key: str, title: str = "", body: str = "", **kwargs):
    config = Config()
    group = config.get_group(key)
    if group is None:
        return Response(code=-1, message="key not authorized").render()
    errors = {}
    for chan in group.channels:
        message = build_message(chan.get_name(), title, body, **kwargs)
        rs, msg = chan.send(message)
        if not rs:
            errors[chan.get_name()] = msg

    if len(errors) == 0:
        return success()
    err_msg = ""
    for err in errors.items():
        err_msg += f"{err[0]} return: {err[1]}."
    return Response(code=1, message=err_msg).render()
