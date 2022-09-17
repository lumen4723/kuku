from typing import Any, Dict, Optional

from fastapi import HTTPException, status

class userAlreadyExists(HTTPException):
    def __init__(
        self,
        status_code: int = status.HTTP_409_CONFLICT,
        detail: Any = "User already exists",
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code, detail=detail, headers=headers)

