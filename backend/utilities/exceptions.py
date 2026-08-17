from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse


class AppException(HTTPException):
    def __init__(self, status_code : int, detail : str):
        super().__init__(status_code=status_code, detail=detail)


class AlreadyExistsException(HTTPException):
    def __init__(self, resource : str):
        super().__init__(status.HTTP_409_CONFLICT, detail=f'{resource} Already Exists')


class NotFoundException(AppException):
    def __init__(self, resource : str = "Resource"):
        super().__init__(status.HTTP_404_NOT_FOUND, f"{resource} not found")


class UnauthorizedException(AppException):
    def __init__(self, detail : str = "Unauthorized"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class ForbiddenException(AppException):
    def __init__(self, detail : str = "Forbidden"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class ConflictException(AppException):
    def __init__(self, detail : str = "Conflict"):
        super().__init__(status.HTTP_409_CONFLICT, detail)


class BadRequestException(AppException):
    def __init__(self, detail : str = "Bad request"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class InvalidTicketTransitionException(BadRequestException):
    def __init__(self, from_status: str, to_status : str):
        super().__init__(f"Cannot transition ticket from {from_status} to {to_status}")

class DatabaseError(AppException):
    def __init__(self, message : str):
        super().__init__(f"{message}, Error While Interacting with the Database", status.HTTP_500_INTERNAL_SERVER_ERROR)