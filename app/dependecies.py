from typing import Annotated

from fastapi import Header, HTTPException

from .repository import auth_repo


async def get_token_header(authorization: Annotated[str, Header()]):
    if not authorization:
        raise HTTPException(status_code=400, detail="X-Token header invalid")