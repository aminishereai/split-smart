import datetime
from uuid import uuid4


from fastapi import Request
from h11 import Data
from passlib import hosts
from starlette.middleware.base import BaseHTTPMiddleware
from logging import Formatter, Logger, StreamHandler , getLogger, INFO, DEBUG, WARNING, ERROR, CRITICAL
from typing import Literal

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

LEVELS = {
    "DEBUG": DEBUG,
    "INFO": INFO,
    "WARNING": WARNING,
    "ERROR": ERROR,
    "CRITICAL": CRITICAL,
}


def get_logger(log_level: LogLevel = "INFO") -> Logger:
    """Create or return a module logger configured to the given level.

    Default level is INFO to allow calling get_logger() without arguments.
    """
    logger = getLogger("split-smart")
    logger.setLevel(LEVELS[log_level])

    if not logger.handlers:
        handler = StreamHandler()
        handler.setLevel(LEVELS[log_level])
        handler.setFormatter(
            Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        logger.addHandler(handler)

    if not isinstance(logger, Logger):
        raise NotImplementedError("logger was not created")

    return logger




logger = get_logger()

#logger middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch (self , request : Request , call_next):
        id = uuid4()
        t1 =  datetime.datetime.now()
        client =  request.client
        client_ip = client.host if  client else None
        method = request.method
        url = request.url.path
        
        req_info = {
            "client_ip" : client_ip,
            "method" : method,
            "url" : url,
            "id" : id
        }
        logger.info("Request : {method} {url} from {client_ip}" , extra ={"type" : "Request","info" : req_info})

        response = await call_next(request)

        status_code = response.status_code


        time_taken = datetime.datetime.now() - t1

        resp_info = {
            "id" : id,
            "status_code" : status_code,
            "time_taken" : time_taken,
            **req_info

        }

        logger.info(f"Response : {method} {url} returnrd {status_code} to {client_ip} in {time_taken}s"  , extra={"type" : "Response" , "info"  : resp_info})

        return response 




    
