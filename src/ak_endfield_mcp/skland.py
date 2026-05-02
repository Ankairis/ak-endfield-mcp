"""Skland (森空岛) API client for Arknights: Endfield game data.

Base URL: zonai.skland.com (NOT web-api.skland.com)
Auth header: Cred (NOT Credential)
"""

import os
import httpx

SKLAND_BASE = "https://zonai.skland.com/api/v1"


class SklandClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("SKLAND_TOKEN")

    def set_token(self, token: str):
        self.token = token

    async def _request(self, endpoint: str, **kwargs) -> dict:
        if not self.token:
            raise ValueError("未设置Skland Token")

        headers = kwargs.pop("headers", {})
        headers["User-Agent"] = "AkEndfieldMCP/1.0"
        headers["Cred"] = self.token

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{SKLAND_BASE}{endpoint}",
                headers=headers,
                **kwargs,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise RuntimeError(f"Skland API error: {data.get('code')} {data.get('message')}")
            return data["data"]

    async def get_game_list(self):
        """Get list of all bound games and their character bindings.
        Returns list of {appCode, appName, bindingList}.
        """
        data = await self._request("/game/player/binding")
        return data.get("list", [])

    async def get_game_data(self, uid: str):
        """Get full player game data (routine, status/ap, etc.)."""
        return await self._request(f"/game/player/gameData?uid={uid}")
