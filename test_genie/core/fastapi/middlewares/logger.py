import time
import json

from fastapi import Request
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        body = ""
        if request.method in ["POST", "PUT"]:
            body = await request.body()
            await request.body()  # reset body

        logger.info(
            f"Path: {request.url.path} | Method: {request.method} | Headers: {request.headers}")

        body_str = ""
        if body:
            try:
                if request.headers.get("Content-Type") != "multipart/form-data":
                    body_str = body.decode()
                    json_body = json.loads(body_str)
                    body_str = json.dumps(json_body, separators=(',', ':'))
            except Exception:
                pass
            finally:
                logger.info(f" request body: {body_str}")

        response = await call_next(request)

        process_time = (time.time() - start_time) * 1000
        logger.info(
            f"Path: {request.url.path} | Method: {request.method} | Status Code: {response.status_code} | Cost: {process_time:.2f}ms")

        return response
