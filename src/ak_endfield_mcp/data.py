"""Static data for Arknights: Endfield daily tasks."""

DAILY_TASKS = [
    {"task": "完成1个每日任务", "points": 80},
    {"task": "组装装备1次", "points": 40},
    {"task": "赠送礼物给1名干员", "points": 40},
    {"task": "登录游戏", "points": 20},
    {"task": "升级1名干员1级", "points": 20},
    {"task": "升级1把武器1级", "points": 20},
    {"task": "进行1次制造", "points": 20},
    {"task": "采集5个可采集物品", "points": 20},
    {"task": "击败20个敌人", "points": 20},
    {"task": "消耗60点理智", "points": 10},
    {"task": "消耗120点理智", "points": 10},
]

FAST_ROUTE = {
    "description": "约2分钟完成100活跃点",
    "steps": [
        {"action": "登录游戏", "points": 20},
        {"action": "升级1名干员1级", "points": 20},
        {"action": "升级1把武器1级", "points": 20},
        {"action": "在PAC制造1件装备", "points": 40},
    ],
    "totalPoints": 100,
}

RESET_HOUR_UTC8 = 4
