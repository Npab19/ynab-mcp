import secrets
from urllib.parse import parse_qs, urlparse

from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send


class BearerTokenMiddleware:
    def __init__(self, app: ASGIApp, token: str) -> None:
        self.app = app
        self._token = token

    def _extract_token(self, scope: Scope) -> str | None:
        """Extract token from Authorization header or api_key query parameter."""
        # Check Authorization: Bearer <token> header
        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b"authorization", b"").decode("latin-1")
        if auth_header.lower().startswith("bearer "):
            return auth_header[7:]

        # Check ?api_key=<token> query parameter
        query_string = scope.get("query_string", b"").decode("latin-1")
        params = parse_qs(query_string)
        if "api_key" in params:
            return params["api_key"][0]

        return None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        # Pass lifespan and websocket scopes through untouched to preserve
        # the StreamableHTTPSessionManager lifespan handler
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        provided_token = self._extract_token(scope)

        if provided_token is None or not secrets.compare_digest(provided_token, self._token):
            response = Response(
                "Unauthorized",
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
            await response(scope, receive, send)
            return

        await self.app(scope, receive, send)
