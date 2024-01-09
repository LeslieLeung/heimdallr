from typing import Any, Dict


class Response:
    code: int
    message: str

    def __init__(self, code: int = 0, message: str = "success"):
        self.code = code
        self.message = message

    def render(self) -> Dict[str, Any]:
        return {"code": self.code, "message": self.message}


def success() -> Dict[str, Any]:
    response = Response()
    return response.render()
