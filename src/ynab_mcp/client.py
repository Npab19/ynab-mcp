from __future__ import annotations

import json
import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)

YNAB_BASE_URL = "https://api.ynab.com/v1"


class YNABError(Exception):
    """Raised when the YNAB API returns an error response."""

    def __init__(self, status_code: int, error_id: str, name: str, detail: str):
        self.status_code = status_code
        self.error_id = error_id
        self.name = name
        self.detail = detail
        super().__init__(f"YNAB API error ({name}): {detail}")


class YNABClient:
    """Async HTTP client for the YNAB API."""

    def __init__(self, api_key: str | None = None):
        key = api_key or os.environ.get("YNAB_API_KEY")
        if not key:
            raise ValueError(
                "YNAB API key is required. Set YNAB_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self._client = httpx.AsyncClient(
            base_url=YNAB_BASE_URL,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Parse response, raising YNABError on non-2xx status."""
        if response.status_code >= 400:
            try:
                body = response.json()
                err = body.get("error", {})
                raise YNABError(
                    status_code=response.status_code,
                    error_id=err.get("id", "unknown"),
                    name=err.get("name", "unknown"),
                    detail=err.get("detail", response.text),
                )
            except (json.JSONDecodeError, KeyError):
                raise YNABError(
                    status_code=response.status_code,
                    error_id="unknown",
                    name="unknown",
                    detail=response.text,
                )

        body = response.json()
        # Strip outer {"data": ...} wrapper that YNAB uses on all responses
        return body.get("data", body)

    async def get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        params = {k: v for k, v in (params or {}).items() if v is not None}
        response = await self._client.get(path, params=params or None)
        return await self._handle_response(response)

    async def post(
        self, path: str, json_body: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        response = await self._client.post(path, json=json_body)
        return await self._handle_response(response)

    async def put(
        self, path: str, json_body: dict[str, Any]
    ) -> dict[str, Any]:
        response = await self._client.put(path, json=json_body)
        return await self._handle_response(response)

    async def patch(
        self, path: str, json_body: dict[str, Any]
    ) -> dict[str, Any]:
        response = await self._client.patch(path, json=json_body)
        return await self._handle_response(response)

    async def delete(self, path: str) -> dict[str, Any]:
        response = await self._client.delete(path)
        return await self._handle_response(response)

    async def close(self) -> None:
        await self._client.aclose()
