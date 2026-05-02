"""MCP Server: Arknights: Endfield daily data + Skland API integration."""

from datetime import datetime, timedelta, timezone
from mcp.server.fastmcp import FastMCP

from .data import (
    DAILY_TASKS,
    DAILY_REWARDS,
    TOTAL_DAILY_REWARDS,
    FAST_ROUTE,
    RESET_HOUR_UTC8,
    RESET_TIMEZONES,
    EXTRA_DAILY_ACTIVITIES,
)
from .skland import SklandClient

mcp = FastMCP("ak-endfield")
skland = SklandClient()

UTC8 = timezone(timedelta(hours=8))


def _get_reset_countdown() -> dict:
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


# ===== Static daily guide tools =====

@mcp.tool()
def get_daily_checklist() -> str:
    """获取终末地每日任务清单及活跃点数。"""
    lines = [f"{i+1}. {t['task']} — **{t['points']}点**" for i, t in enumerate(DAILY_TASKS)]
    total = sum(t["points"] for t in DAILY_TASKS)
    return "\n".join([
        "# 明日方舟：终末地 每日任务清单",
        "",
        *lines,
        "",
        f"---",
        f"**每日满活跃需要100点**，全部任务共{total}点。只需选做100点即可。",
    ])


@mcp.tool()
def get_daily_rewards() -> str:
    """获取终末地每日活跃奖励档位。"""
    lines = []
    for r in DAILY_REWARDS:
        rewards_str = " / ".join(f"{rw['name']} ×{rw['amount']}" for rw in r["rewards"])
        lines.append(f"- **{r['points']}点:** {rewards_str}")

    total_lines = [f"- {r['name']}: ×{r['amount']}" for r in TOTAL_DAILY_REWARDS]

    return "\n".join([
        "# 每日活跃奖励档位",
        "",
        *lines,
        "",
        "---",
        "## 全档位总奖励",
        *total_lines,
    ])


@mcp.tool()
def get_reset_info() -> str:
    """获取终末地每日刷新时间及倒计时。"""
    cd = _get_reset_countdown()
    tz_lines = [f"- {k}: {v}" for k, v in RESET_TIMEZONES.items()]

    return "\n".join([
        "# 终末地每日刷新",
        "",
        f"**服务器时间 (UTC+8):** {cd['now_utc8']}",
        f"**下次刷新:** {cd['reset_utc8']}",
        f"**距离刷新还剩:** {cd['hours_left']}小时{cd['minutes_left']}分钟",
        "",
        "## 各时区刷新时间",
        *tz_lines,
    ])


@mcp.tool()
def get_fast_route() -> str:
    """获取终末地2分钟速通100活跃点的最快路线。"""
    steps = [f"{i+1}. **{s['action']}** → {s['points']}点 ({s['time']})" for i, s in enumerate(FAST_ROUTE["steps"])]

    return "\n".join([
        f"# ⚡ 速通路线 — {FAST_ROUTE['description']}",
        "",
        *steps,
        "",
        f"---",
        f"**总计: {FAST_ROUTE['totalPoints']}点 / {FAST_ROUTE['totalTime']}**",
    ])


@mcp.tool()
def get_full_daily_guide() -> str:
    """获取终末地完整每日必做攻略（含任务、据点、帝江号等全部内容）。"""
    fast_steps = [f"{i+1}. **{s['action']}** → {s['points']}点" for i, s in enumerate(FAST_ROUTE["steps"])]

    sections = []
    for cat in EXTRA_DAILY_ACTIVITIES:
        activities = "\n".join(f"- {a}" for a in cat["activities"])
        sections.append(f"## {cat['category']}\n{activities}\n> 产出: {cat['rewards']}")

    return "\n\n".join([
        "# 终末地每日完全攻略",
        "",
        f"## ⚡ 速刷100活跃 ({FAST_ROUTE['totalTime']})",
        *fast_steps,
        "",
        "---",
        "",
        *sections,
    ])


# ===== Skland API tools =====

@mcp.tool()
async def set_skland_token(token: str) -> str:
    """设置森空岛Token以查询实时游戏数据。
    在 https://web-api.skland.com/account/info/hg 登录后，返回的 data.content 即为Token。
    参数: token (str) 森空岛通行证Token
    """
    skland.set_token(token)
    try:
        info = await skland.get_account_info()
        return f"Token设置成功！账号UID: {info.get('uid')}, 昵称: {info.get('nickname')}"
    except Exception as e:
        return f"Token验证失败: {e}"


@mcp.tool()
async def get_game_bindings() -> str:
    """获取森空岛绑定的终末地游戏角色列表。需先设置 Skland Token。"""
    try:
        bindings = await skland.get_endfield_binding()
        if not bindings:
            return "未找到绑定的终末地角色。"
        lines = [f"{i+1}. UID: {b.get('uid')} | 昵称: {b.get('nickname')} | 渠道: {b.get('channelName')}" for i, b in enumerate(bindings)]
        return "\n".join(["# 绑定的终末地角色", "", *lines])
    except Exception as e:
        return f"获取绑定角色失败: {e}"


@mcp.tool()
async def get_character_card(uid: str) -> str:
    """获取终末地角色卡片信息（需先设置Skland Token）。
    参数: uid (str) 游戏UID，可通过 get_game_bindings 获取
    """
    try:
        data = await skland.get_endfield_full_data(uid)
        chars = data.get("characters", [])
        char_lines = []
        for c in chars:
            char_lines.append(
                f"- **{c.get('charId', '未知')}** | Lv{c.get('level', '?')} | "
                f"精英{c.get('elite', '?')} | 潜能{c.get('potential', '?')} | "
                f"信赖{c.get('trust', '?')}"
            )

        gacha_records = data.get("gacha", [])
        gacha_lines = []
        for r in gacha_records[:10]:
            ts = datetime.fromtimestamp(r.get("ts", 0)).strftime("%Y-%m-%d")
            chars_str = ", ".join(
                f"{c.get('name')} ({'★' * c.get('rarity', 1)}{' NEW' if c.get('isNew') else ''})"
                for c in r.get("chars", [])
            )
            gacha_lines.append(f"- [{ts}] {r.get('pool', '?')} — {chars_str}")

        parts = [
            f"# {data.get('nickname', '未知')} (UID: {data.get('uid', uid)})",
            "",
            "## 角色列表",
            "\n".join(char_lines) if char_lines else "无角色数据",
        ]

        if gacha_lines:
            parts.extend(["", "## 最近寻访记录", "\n".join(gacha_lines)])

        return "\n".join(parts)

    except Exception as e:
        return f"获取角色卡片失败: {e}"


@mcp.tool()
async def get_gacha_records(uid: str, page: int = 1) -> str:
    """获取终末地寻访记录（需先设置Skland Token）。
    参数: uid (str) 游戏UID, page (int) 页码，默认1
    """
    try:
        data = await skland.get_endfield_gacha(uid, page)
        records = data.get("records", [])
        rec_lines = []
        for i, r in enumerate(records):
            ts = datetime.fromtimestamp(r.get("ts", 0)).strftime("%Y-%m-%d")
            chars_str = ", ".join(
                f"{c.get('name')} ({'★' * c.get('rarity', 1)}{' NEW' if c.get('isNew') else ''})"
                for c in r.get("chars", [])
            )
            rec_lines.append(f"{i+1}. [{ts}] {r.get('pool', '?')} — {chars_str}")

        return "\n".join([
            f"# 寻访记录 (第{page}页)",
            f"总计: {data.get('total', 0)}条",
            "",
            "\n".join(rec_lines) if rec_lines else "无寻访记录",
        ])
    except Exception as e:
        return f"获取寻访记录失败: {e}"


def main():
    mcp.run()


if __name__ == "__main__":
    main()
