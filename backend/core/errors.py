from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


def serialize_detail(value):
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, list):
        return [serialize_detail(item) for item in value]
    if isinstance(value, tuple):
        return [serialize_detail(item) for item in value]
    if isinstance(value, dict):
        return {key: serialize_detail(item) for key, item in value.items()}
    return str(value)


def error_response(status_code: int, message: str, details=None) -> JSONResponse:
    content = {
        "error": {
            "status_code": status_code,
            "message": message,
        }
    }
    if details is not None:
        content["error"]["details"] = serialize_detail(details)
    return JSONResponse(status_code=status_code, content=content)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return error_response(exc.status_code, str(exc.detail))


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return error_response(422, "Dados invalidos.", exc.errors())


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
