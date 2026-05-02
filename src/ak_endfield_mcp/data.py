"""Static data for Arknights: Endfield daily tasks, rewards, and guides."""

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
    {"task": "消耗60点醚质", "points": 10},
    {"task": "消耗120点醚质", "points": 10},
]

DAILY_REWARDS = [
    {"points": 20, "rewards": [{"name": "行动经验", "amount": 400}]},
    {"points": 40, "rewards": [{"name": "龙门币", "amount": 2000}]},
    {"points": 60, "rewards": [{"name": "作战记录·进阶", "amount": 1}]},
    {"points": 80, "rewards": [{"name": "应急醚质补给", "amount": 1}]},
    {"points": 100, "rewards": [{"name": "原石碱", "amount": 200}]},
]

TOTAL_DAILY_REWARDS = [
    {"name": "原石碱 (合成玉)", "amount": 200},
    {"name": "通行证经验", "amount": 2000},
    {"name": "行动经验", "amount": 1150},
    {"name": "龙门币", "amount": 9000},
    {"name": "应急醚质补给", "amount": 1},
    {"name": "作战记录·进阶", "amount": 1},
    {"name": "素子原件", "amount": 5},
    {"name": "武具INSP套组", "amount": 2},
]

FAST_ROUTE = {
    "description": "约2分钟完成100活跃点",
    "steps": [
        {"action": "登录游戏", "points": 20, "time": "自动"},
        {"action": "升级1名干员1级", "points": 20, "time": "~30秒"},
        {"action": "升级1把武器1级", "points": 20, "time": "~30秒"},
        {"action": "在PAC制造1件装备", "points": 40, "time": "~1分钟"},
    ],
    "totalTime": "约2分钟",
    "totalPoints": 100,
}

EXTRA_DAILY_ACTIVITIES = [
    {
        "category": "醚质消费",
        "activities": ["清空所有醚质刷材料本", "不要溢出"],
        "rewards": "经验、龙门币、升级材料",
    },
    {
        "category": "据点管理",
        "activities": ["向据点出售制造品", "收获制造站产出"],
        "rewards": "储备票据、繁荣度",
    },
    {
        "category": "OMV帝江号",
        "activities": ["收取舱室产出", "重新派驻干员", "重新种植作物"],
        "rewards": "信用点、免费材料",
    },
    {
        "category": "干员赠礼",
        "activities": ["每日在舰船上赠礼给干员"],
        "rewards": "信赖/同步等级",
    },
    {
        "category": "仓储节点",
        "activities": ["完成配送订单", "或让好友代送"],
        "rewards": "储备票据、材料",
    },
    {
        "category": "回收站",
        "activities": ["地图上收集猫头鹰图标"],
        "rewards": "航空材料 I、II",
    },
    {
        "category": "稀有采集",
        "activities": ["采集地图上的进阶材料", "每天刷新"],
        "rewards": "干员/武器晋升材料",
    },
    {
        "category": "弹性商品",
        "activities": ["在己方舰船低买", "在好友舰船高卖"],
        "rewards": "额外储备票据",
    },
    {
        "category": "信用商店",
        "activities": ["消费信用点", "上限300，超出作废"],
        "rewards": "升级/精进材料",
    },
    {
        "category": "AIC/PAC检查",
        "activities": ["确认电力、电池、机器未堵塞"],
        "rewards": "防止过夜停产",
    },
    {
        "category": "好友互助",
        "activities": ["访问好友舰船", "协助生产"],
        "rewards": "信用点",
    },
]

RESET_HOUR_UTC8 = 4
RESET_TIMEZONE = "Asia/Shanghai"

RESET_TIMEZONES = {
    "UTC-5 (美东)": "下午3:00",
    "UTC+8 (北京)": "凌晨4:00",
    "UTC+1 (欧洲中部)": "晚上9:00",
    "UTC+9 (日本)": "凌晨5:00",
    "UTC+0 (英国)": "晚上8:00",
}
