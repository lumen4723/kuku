from typing import Any, Dict, Optional

from fastapi import HTTPException, status

class userAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: str = "User already exists",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)
        
class defaultHttpException(HTTPException):
    def __init__(
        self,
        detail: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Dict[str, Any] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)

    def raise_err(self):
        raise self