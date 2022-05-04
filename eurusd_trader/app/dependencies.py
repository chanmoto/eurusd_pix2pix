from fastapi import Header, HTTPException

async def get_token_header(x_token: str = Header(...)):
    if x_token != "moto":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def get_query_token(token: str):
    if token != "moto":
        raise HTTPException(status_code=400, detail="No Jessica token provided")