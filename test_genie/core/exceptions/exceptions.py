from fastapi import status

from test_genie.core.exceptions.base import CustomException


class BadRequestException(CustomException):
    def __init__(self, message='Bad Request'):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message)


class UnauthorizedException(CustomException):
    def __init__(self, message='Unauthorized'):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message)


class ForbiddenException(CustomException):
    def __init__(self, message='Forbidden'):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message)


class NotFoundException(CustomException):
    def __init__(self, message='Not Found'):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message)


class ConflictException(CustomException):
    def __init__(self, message='Conflict'):
        super().__init__(status_code=status.HTTP_409_CONFLICT, message=message)


class TooManyRequestsException(CustomException):
    def __init__(self, message='Too Many Requests'):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, message=message)


class InternalException(CustomException):
    def __init__(self, message='Internal Server Error'):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=message)
