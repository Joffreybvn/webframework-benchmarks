from datetime import datetime
from functools import wraps

import fastjsonschema
from blacksheep import Request, Response
from blacksheep.server import Application
from blacksheep.server.responses import json
from fastjsonschema import JsonSchemaValueException

app = Application()

profile = fastjsonschema.compile({
        'type': 'object',
        'properties': {
            'name': {'type': 'string', 'default': 'Jean'},
            'age': {'type': 'number', 'default': 42},
        },
    })


def validate_schema(validator):
    def wrapper(func):
        @wraps(func)
        async def wrapped(request: Request, *args, **kwargs):
            body: dict = validator(await request.json())
            return await func(request, body, **kwargs)
        return wrapped
    return wrapper


async def exception_handler(_, request, exception: JsonSchemaValueException):
    return json({'message': str(exception)}, 400)


# Register the exception handler for the CustomException type:
app.exceptions_handlers[JsonSchemaValueException] = exception_handler


@app.router.post("/")
@validate_schema(profile)
async def home(request: Request, body: dict) -> Response:
    body |= {'time': datetime.utcnow().isoformat()}
    return json(body, status=200)
