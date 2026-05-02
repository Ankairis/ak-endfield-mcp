"""Skland (森空岛) API client for Arknights: Endfield game data."""

import os
import httpx

SKLAND_BASE = "https://web-api.skland.com"


class SklandClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("SKLAND_TOKEN")

    def set_token(self, token: str):
        self.token = token

    async def _request(self, endpoint: str, **kwargs) -> dict:
        if not self.token:
            raise ValueError(
                "未设置Skland Token。请在森空岛登录后访问 "
                "https://web-api.skland.com/account/info/hg 获取token，"
                "然后通过环境变量 SKLAND_TOKEN 或 set_skland_token 工具设置。"
            )

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

    async def get_account_info(self):
        return await self._request("/account/info/hg")

    async def get_endfield_binding(self):
        data = await self._request("/game/binding/list?gameCode=endfield")
        return data.get("bindingList", [])

    async def get_endfield_character_card(self, uid: str):
        return await self._request(f"/game/endfield/character/list?uid={uid}")

    async def get_endfield_gacha(self, uid: str, page: int = 1, page_size: int = 20):
        return await self._request(
            f"/game/endfield/gacha/records?uid={uid}&page={page}&pageSize={page_size}"
        )

    async def get_endfield_full_data(self, uid: str) -> dict:
        results = {}
        endpoints = [
            ("characters", self.get_endfield_character_card),
            ("gacha", self.get_endfield_gacha),
        ]
        for key, fn in endpoints:
            try:
                results[key] = await fn(uid)
            except Exception:
                results[key] = None

        try:
            bindings = await self.get_endfield_binding()
            binding = next((b for b in bindings if b.get("uid") == uid), None) or (
                bindings[0] if bindings else None
            )
        except Exception:
            binding = None

        return {
            "uid": uid,
            "nickname": binding.get("nickname", "未知") if binding else "未知",
            "characters": (results.get("characters") or {}).get("chars", []),
            "gacha": (results.get("gacha") or {}).get("records", []),
        }
