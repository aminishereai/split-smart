from pydantic import BaseModel


class ProblemDetails(BaseModel):
    title : str
    detail : str
    status : int
    type : str
    instance : str