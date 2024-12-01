class NewsError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class NewsAlreadyInDBError(Exception):
    def __init__(self, message: str = "News is already in database"):
        super().__init__(message)
