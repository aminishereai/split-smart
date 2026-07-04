from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.utils.exceptions.base import APIException
from app.utils.exceptions.problems import ProblemDetails


async def api_exception_handler(request : Request , exc : Exception) -> JSONResponse:
    assert isinstance(exc, APIException)
    problem = ProblemDetails(
        title=exc.title,
        status=exc.status,
        detail=exc.detail,
        type=exc.type,
        instance=request.url.path
    )

    return JSONResponse(
        status_code=exc.status,
        content=problem.model_dump(),
        media_type="application/problem+json",

    )







def register_exception_handlers(app : FastAPI):
    app.add_exception_handler(
        APIException,
        api_exception_handler 
    )
    