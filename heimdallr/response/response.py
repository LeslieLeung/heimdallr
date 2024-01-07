
class Response:
    code: int
    message: str

    def __init__(self, code: int = 0, message: str = "success"):
        self.code = code
        self.message = message

    def render(self):
        return {"code": self.code, "message": self.message}


def success():
    response = Response()
    return response.render()
