from fastapi import APIRouter, Depends
from dependencies import get_token_header

router = APIRouter(
    dependencies=[Depends(get_token_header)],
    responses={
        418: {"description": "I'm a admin"}
    },
)

@ router.post("/")
async def update_admin():
    return {"message": "Admin getting schwifty"}
