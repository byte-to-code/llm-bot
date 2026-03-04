class BotError(Exception):
    def __init__(self, message: str, code: int = 500) -> None:
        self.message = message
        self.code = code

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


class UserNotFoundError(BotError):
    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message, 404)


class ModelNotFoundError(BotError):
    def __init__(self, message: str = "Model not found") -> None:
        super().__init__(message, 404)
