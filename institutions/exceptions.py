from fastapi import HTTPException
from typing import Any, Dict, Optional


class NotFoundException(HTTPException):
    def __init__(
        self,
        detail: Any = None,
        status_code: int = 404,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers