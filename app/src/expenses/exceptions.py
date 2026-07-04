from app.utils.exceptions.base import APIException


class SplitsRequiredError(APIException):
    title = "Splits are Missing in the input."
    status = 422
    type = "/error/splits-required-disproportionate"

    def __init__(self):
        super().__init__("Splits are required for a disproportionate split.")

class SplitsInputConflict(APIException):
    title = "Splits aren't in required amount."
    status = 422
    type = "/error/splits-input-conflict"

    def __init__(self):
        super().__init__("Number of split entries must match group members.")
