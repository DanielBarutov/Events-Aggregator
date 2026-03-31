class AppError(Exception):
    def __init__(self, message: str, code: int = 400, details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class NotFoundError(AppError):
    def __init__(self, message: str, code: int = 404, details: dict = None):
        super().__init__(message, code, details)


class ConflictError(AppError):
    def __init__(self, message: str, code: int = 409, details: dict = None):
        super().__init__(message, code, details)


class BusinessLogicError(AppError):
    def __init__(self, message: str, code: int = 400, details: dict = None):
        super().__init__(message, code, details)


class ExternalProviderError(AppError):
    def __init__(self, message: str, code: int = 502, details: dict = None):
        super().__init__(message, code, details)


class DatabaseError(AppError):
    def __init__(self, message: str, code: int = 500, details: dict = None):
        super().__init__(message, code, details)


class CacheError(AppError):
    def __init__(self, message: str, code: int = 500, details: dict = None):
        super().__init__(message, code, details)
