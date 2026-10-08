import hashlib
import hmac
import json
import os
import time
from urllib.parse import parse_qsl
from fastapi import HTTPException

def validate_init_data(init_data: str) -> dict:
    bot_token = os.getenv("BOT_TOKEN")
    if not init_data or not bot_token:
        raise HTTPException(401, "Telegram authorization data is missing")
    try:
        pairs = parse_qsl(init_data, keep_blank_values=True)
        data = dict(pairs)
    except Exception as exc:
        raise HTTPException(401, "Invalid Telegram initData") from exc
    received_hash = data.pop("hash", None)
    if not received_hash:
        raise HTTPException(401, "Telegram hash is missing")
    check = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    calculated = hmac.new(secret, check.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated, received_hash):
        raise HTTPException(401, "Invalid Telegram initData signature")
    try:
        auth_date = int(data.get("auth_date", "0"))
    except ValueError as exc:
        raise HTTPException(401, "Invalid Telegram auth_date") from exc
    max_age = int(os.getenv("INIT_DATA_MAX_AGE", "86400"))
    now = int(time.time())
    if auth_date > now + 60 or now - auth_date > max_age:
        raise HTTPException(401, "Telegram initData has expired")
    try:
        user = json.loads(data["user"])
    except (KeyError, json.JSONDecodeError) as exc:
        raise HTTPException(401, "Invalid Telegram user data") from exc
    if not isinstance(user.get("id"), int) or user["id"] <= 0:
        raise HTTPException(401, "Invalid Telegram user id")
    return user
