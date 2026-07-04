from app.utils.exceptions.base import APIException

class UserNotFound(APIException):
    title = "User doesn't exist."
    status = 404
    type = "/error/user-not-found"

    def __init__(self, username: str | None):
        super().__init__(f"User : {username} does not exist.")


class UserAlreadyExists(APIException):
    title = "User already exists."
    status = 409
    type = "/error/user-already-exists"
    
    def __init__(self , username : str):
        super().__init__(f"User : {username} already exists.")

class UserNotAuthorized(APIException):
    title = "User is not Authorized"
    status = 401
    type = "/error/user-not-authorized"

    def __init__(self, username: str , feature : str):
        super().__init__(f" User {username} is not authorized to {feature} ")


