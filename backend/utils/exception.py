from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class NotFound(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_404_NOT_FOUND,
        detail: str = "Not found",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)

class AlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_403_FORBIDDEN,
        detail: str = "Already exists",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)

class NotAuthorized(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Not authorized",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)

class TokenProblem(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_401_UNAUTHORIZED,
        detail: str = "Token problem",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)

class DefaultException(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Internal Server Error",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)


def throwMsg(msg):
    if isinstance(msg, HTTPException):
        print('error ->', msg)
        raise msg
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

