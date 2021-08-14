from dataclasses import dataclass
from datetime import datetime
from blacksheep import Response
from blacksheep.server import Application
from blacksheep.server.bindings import FromJSON
from blacksheep.server.responses import json


app = Application()


class ValidateException(Exception):
    """Triggered when a dataclass fail to validate."""


@dataclass
class Profile:
    name: str = 'Jean'
    age: int = 42

    def __post_init__(self):
        """Validate dataclass."""
        if not isinstance(self.age, int):
            raise ValidateException("age is not a number")
        if not isinstance(self.name, str):
            raise ValidateException("name is not a string")


async def exception_handler(_, request, exception: ValidateException):
    return json({'message': str(exception)}, 400)


# Register the exception handler for the CustomException type:
app.exceptions_handlers[ValidateException] = exception_handler


@app.router.post("/")
async def home(body: FromJSON[Profile]) -> Response:
    data = body.value.__dict__
    data |= {'time': datetime.utcnow().isoformat()}
    return json(data, status=200)
