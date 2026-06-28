class AppBaseError(Exception):
    message = "An unexpected error occurred"

    def __init__(self, message: str = None):
        self.message = message or self.message
        super().__init__(self.message)


class DBError(AppBaseError):
    message = "Internal Database Error"

    def __init__(self, message: str = None):
        super().__init__(message)


class CodeAlreadyExistsError(AppBaseError):
    message = "Code already exists"

    def __init__(self, code: str, message: str = None):
        self.code = code
        super().__init__(message or f"Code '{code}' already exists")


class CodeNotFoundError(AppBaseError):
    message = "Code not found"

    def __init__(self, code: str, message: str = None):
        self.code = code
        super().__init__(message or f"Code '{code}' not found")


class CouldNotGenerateCodeError(AppBaseError):
    message = "Couldn't generate a unique code, please retry"

    def __init__(self, message: str = None):
        super().__init__(message)
