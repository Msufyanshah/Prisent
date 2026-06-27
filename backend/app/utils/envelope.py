import json
from datetime import datetime
from typing import Callable, Coroutine, Any
from fastapi import Request, Response, status
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException

class EnvelopedRoute(APIRoute):
    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response = await original_route_handler(request)
            
            # Skip health, docs, and openapi.json
            if request.url.path in ("/health", "/docs", "/openapi.json") or request.url.path.startswith("/docs"):
                return response
                
            if response.headers.get("content-type") == "application/json":
                # Read the response body
                body = response.body
                try:
                    data = json.loads(body.decode("utf-8"))
                    # If it already has the envelope keys, don't double wrap
                    if isinstance(data, dict) and all(k in data for k in ("success", "data", "error", "timestamp")):
                        wrapped = data
                    else:
                        wrapped = {
                            "success": True,
                            "data": data,
                            "error": None,
                            "timestamp": datetime.utcnow().isoformat()
                        }
                    headers = dict(response.headers)
                    headers.pop("content-length", None)
                    headers.pop("Content-Length", None)
                    return Response(
                        content=json.dumps(wrapped).encode("utf-8"),
                        status_code=response.status_code,
                        media_type="application/json",
                        headers=headers
                    )
                except Exception:
                    # If parsing fails, return original response
                    headers = dict(response.headers)
                    headers.pop("content-length", None)
                    headers.pop("Content-Length", None)
                    return Response(
                        content=body,
                        status_code=response.status_code,
                        media_type=response.media_type,
                        headers=headers
                    )
            return response

        return custom_route_handler

async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    detail = exc.detail
    code = "ERROR"
    message = str(detail)
    if isinstance(detail, dict):
        code = detail.get("code", "ERROR")
        message = detail.get("message", str(detail))
        
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": code,
                "message": message
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "data": None,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": exc.errors()
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    )
