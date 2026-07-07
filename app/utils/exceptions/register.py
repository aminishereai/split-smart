from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils.exceptions.base import APIException
from app.utils.exceptions.problems import ProblemDetails


async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    problem = ProblemDetails(
        title=exc.title,
        status=exc.status,
        detail=exc.detail,
        type=exc.type,
        instance=request.url.path,
    )
    return JSONResponse(
        status_code=exc.status,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
    problem = ProblemDetails(
        title="HTTP Error",
        status=exc.status_code,
        detail=detail,
        type="about:blank",
        instance=request.url.path,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    detail = ", ".join(
        f"{'.'.join(str(loc) for loc in err['loc'])}: {err['msg']}" for err in errors
    )
    problem = ProblemDetails(
        title="Invalid request",
        status=422,
        detail=detail,
        type="/error/invalid-request",
        instance=request.url.path,
    )
    return JSONResponse(
        status_code=422,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    problem = ProblemDetails(
        title="Internal Server Error",
        status=500,
        detail=str(exc) or "Internal server error",
        type="about:blank",
        instance=request.url.path,
    )
    return JSONResponse(
        status_code=500,
        content=problem.model_dump(),
        media_type="application/problem+json",
    )





def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(APIException, api_exception_handler) # type: ignore
    app.add_exception_handler(HTTPException, http_exception_handler) # type: ignore
    app.add_exception_handler(RequestValidationError, validation_exception_handler) # type: ignore
    app.add_exception_handler(Exception, generic_exception_handler)
    