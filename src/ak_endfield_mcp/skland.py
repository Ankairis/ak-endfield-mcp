"""Skland (森空岛) API client for Arknights: Endfield game data."""

import os
import httpx

SKLAND_BASE = "https://web-api.skland.com"
GAME_CODE = "endfield"  # "arknights" for original, "endfield" for 终末地


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
        headers["Credential"] = self.token

        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.get(
                f"{SKLAND_BASE}{endpoint}",
                headers=headers,
                **kwargs,
            )
            resp.raise_for_status()
            data = resp.json()
            if data.get("code") != 0:
                raise RuntimeError(f"Skland API error: {data.get('code')} {data.get('msg')}")
            return data["data"]

    async def get_binding_list(self):
        """Get list of bound game characters."""
        data = await self._request(f"/game/binding/list?gameCode={GAME_CODE}")
        return data.get("bindingList", [])

    async def get_game_data(self, uid: str):
        """Get full game status including routine (daily tasks) and status (sanity)."""
        return await self._request(f"/game/player/gameData?uid={uid}")
