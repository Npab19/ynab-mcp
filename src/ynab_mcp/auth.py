import secrets

from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send


class BearerTokenMiddleware:
    def __init__(self, app: ASGIApp, token: str) -> None:
        self.app = app
        self._token = token

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Pass lifespan and websocket scopes through untouched to preserve
        # the StreamableHTTPSessionManager lifespan handler
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode("latin-1")

        if not auth_header.lower().startswith("bearer "):
            response = Response(
                "Unauthorized",
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
            await response(scope, receive, send)
            return

        provided_token = auth_header[7:]
        if not secrets.compare_digest(provided_token, self._token):
            response = Response(
                "Unauthorized",
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
