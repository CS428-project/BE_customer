from fastapi import HTTPException, Response, Request

async def verify_cookie(request: Request):
    cookie = request.cookies.get("Authentication")
    if not cookie or not await get_user_by_token(cookie):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return request
