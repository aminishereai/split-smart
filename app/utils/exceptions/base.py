class APIException (Exception):
    title : str = "Internal Server Error"
    status : int = 500
    type : str = "about:blank"

    
    def __init__(self , detail : str):
        self.detail = detail