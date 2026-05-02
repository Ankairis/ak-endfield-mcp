"""MCP Server: Arknights: Endfield daily tasks + sanity status."""

import os
import sys
from datetime import datetime, timedelta, timezone
from mcp.server.fastmcp import FastMCP

from .data import DAILY_TASKS, FAST_ROUTE, RESET_HOUR_UTC8
from .skland import SklandClient

mcp = FastMCP("ak-endfield")
skland = SklandClient()

UTC8 = timezone(timedelta(hours=8))


def _reset_countdown() -> dict:
    now = datetime.now(UTC8)
    reset = now.replace(hour=RESET_HOUR_UTC8, minute=0, second=0, microsecond=0)
    if now >= reset:
        reset += timedelta(days=1)
    diff = reset - now
    return {
        "now_utc8": now.strftime("%Y-%m-%d %H:%M:%S"),
        "reset_utc8": reset.strftime("%Y-%m-%d %H:%M:%S"),
        "hours_left": int(diff.total_seconds() // 3600),
        "minutes_left": int((diff.total_seconds() % 3600) // 60),
    }


def _find_endfield_bindings(game_list: list) -> list[dict]:
    """Extract Endfield bindings from the game list."""
    bindings = []
    for game in game_list:
        app_code = game.get("appCode", "")
        if "endfield" in app_code.lower():
            for b in game.get("bindingList", []):
                b["appName"] = game.get("appName", app_code)
                bindings.append(b)
    return bindings


# ===== Daily Tasks =====

@mcp.tool()
def get_daily_tasks() -> str:
    """获取终末地每日任务清单及活跃点数（含速通路线）。"""
    tasks = [f"{i+1}. {t['task']} — **{t['points']}点**" for i, t in enumerate(DAILY_TASKS)]
    total = sum(t["points"] for t in DAILY_TASKS)
    fast = FAST_ROUTE
    fast_steps = [f"{i+1}. {s['action']} → {s['points']}点" for i, s in enumerate(fast["steps"])]

    return "\n".join([
        "# 终末地每日任务",
        "",
        *tasks,
        "",
        f"满活跃需**100点**，全部共{total}点",
        "",
        "## ⚡ 速通路线",
        *fast_steps,
        f"总计 {fast['totalPoints']}点 / {fast['description']}",
    ])


# ===== Reset Countdown =====

@mcp.tool()
def get_reset_countdown() -> str:
    """获取终末地每日刷新倒计时。"""
    cd = _reset_countdown()
    return "\n".join([
        "# 每日刷新倒计时",
        "",
        f"服务器时间 (UTC+8): {cd['now_utc8']}",
        f"下次刷新: {cd['reset_utc8']}",
        f"距离刷新: {cd['hours_left']}小时{cd['minutes_left']}分钟",
    ])


# ===== Sanity Status (Skland) =====

@mcp.tool()
async def set_token(token: str) -> str:
    """设置森空岛Token以查询实时理智数据。
    登录森空岛后访问 https://web-api.skland.com/account/info/hg
    返回的 data.content 即为Token。
    """
    skland.set_token(token)
    try:
        game_list = await skland.get_game_list()
        if not game_list:
            return "Token有效，但未找到任何绑定的游戏角色。"

        all_games = "\n".join(
            f"- {g.get('appName', g.get('appCode'))}: {len(g.get('bindingList', []))}个角色"
            for g in game_list
        )

        endfield = _find_endfield_bindings(game_list)
        if not endfield:
            return f"Token有效！已绑定的游戏:\n{all_games}\n\n⚠️ 未找到终末地角色。如果你有终末地账号，请先在森空岛绑定。"

        chars = "\n".join(
            f"{i+1}. UID: {b.get('uid')} | 昵称: {b.get('nickName', b.get('nickname', '未知'))} | 渠道: {b.get('channelName', '?')}"
            for i, b in enumerate(endfield)
        )
        return f"Token设置成功！\n\n终末地角色:\n{chars}"

    except Exception as e:
        return f"Token验证失败: {e}"


@mcp.tool()
async def get_sanity() -> str:
    """获取终末地理智状态及每日任务进度（需先设置Token）。"""
    try:
        game_list = await skland.get_game_list()
        endfield = _find_endfield_bindings(game_list)

        if not endfield:
            return "未找到绑定的终末地角色。请先 set_token，并确认已在森空岛绑定终末地游戏账号。"

        results = []
        for b in endfield:
            uid = b.get("uid")
            nickname = b.get("nickName", b.get("nickname", "未知"))
            try:
                data = await skland.get_game_data(uid)
                routine = data.get("routine", {})
                status = data.get("status", {})
                ap = status.get("ap", {}) if status else {}

                parts = [f"## {nickname} (UID: {uid})"]

                if ap:
                    current = ap.get("current", "?")
                    max_ap = ap.get("max", "?")
                    recovery = ap.get("completeRecoveryTime", 0)
                    if recovery:
                        rec_time = datetime.fromtimestamp(recovery, tz=UTC8).strftime("%Y-%m-%d %H:%M:%S")
                        parts.append(f"理智: {current}/{max_ap} | 满恢复: {rec_time}")
                    else:
                        parts.append(f"理智: {current}/{max_ap}")

                daily = routine.get("daily", {}) if routine else {}
                weekly = routine.get("weekly", {}) if routine else {}
                if daily:
                    parts.append(f"每日任务: {daily.get('progress', '?')}/{daily.get('max', '?')}")
                if weekly:
                    parts.append(f"每周任务: {weekly.get('progress', '?')}/{weekly.get('max', '?')}")

                if not ap and not daily:
                    parts.append("暂无实时数据。该游戏的数据API可能尚未开放。")

                results.append("\n".join(parts))

            except Exception as e:
                results.append(f"## {nickname} (UID: {uid})\n获取失败: {e}")

        return "\n\n".join(results) if results else "无数据。"

    except Exception as e:
        return f"查询失败: {e}"


def main():
    port = int(os.environ.get("PORT", "8000"))
    host = os.environ.get("HOST", "0.0.0.0")

    mcp.settings.host = host
    mcp.settings.port = port

    if "--sse" in sys.argv or os.environ.get("MCP_TRANSPORT") == "sse":
        mcp.run(transport="sse")
    elif "--http" in sys.argv or os.environ.get("MCP_TRANSPORT") == "streamable-http":
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
