# 明日方舟：终末地 MCP Server

提供终末地每日任务攻略 + 森空岛实时游戏数据查询。

## 安装

```bash
git clone https://github.com/Ankairis/ak-endfield-mcp.git
cd ak-endfield-mcp
pip install -e .
```

## Claude Desktop 配置

```json
{
  "mcpServers": {
    "ak-endfield": {
      "command": "uvx",
      "args": ["ak-endfield-mcp"]
    }
  }
}
```

或直接用 Python 运行：

```json
{
  "mcpServers": {
    "ak-endfield": {
      "command": "python",
      "args": ["-m", "ak_endfield_mcp.server"]
    }
  }
}
```

## 工具列表

### 每日攻略（无需登录）
| 工具 | 说明 |
|------|------|
| `get_daily_checklist` | 每日任务清单及活跃点数 |
| `get_daily_rewards` | 每日活跃奖励档位 |
| `get_reset_info` | 每日刷新时间及倒计时 |
| `get_fast_route` | 2分钟速通100活跃点路线 |
| `get_full_daily_guide` | 完整每日必做攻略 |

### 森空岛数据（需Token）
| 工具 | 说明 |
|------|------|
| `set_skland_token` | 设置森空岛Token |
| `get_game_bindings` | 获取绑定的终末地角色 |
| `get_character_card` | 角色卡片及任务进度 |
| `get_gacha_records` | 寻访/抽卡记录 |

## 获取森空岛Token

1. 登录 [森空岛](https://skland.com)
2. 访问 `https://web-api.skland.com/account/info/hg`
3. 复制返回的 `data.content` 字段
4. 通过 `set_skland_token` 工具设置或设置环境变量 `SKLAND_TOKEN`

⚠️ Token不可泄露，具有账户操作权限。
