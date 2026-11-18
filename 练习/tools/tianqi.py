from langchain_core.tools import tool
from datetime import datetime

WEATHER_DB = {
    "北京": {"condition": "晴天", "temp": "15-25°C", "aqi": "优"},
    "浙江": {"condition": "阴天", "temp": "8-16°C", "aqi": "良"},
    "重庆": {"condition": "小雨转晴", "temp": "13-20°C", "aqi": "优"},
    "上海": {"condition": "大雨", "temp": "8-13°C", "aqi": "良"},
    "海南": {"condition": "晴天", "temp": "26-31°C", "aqi": "优"},
}

#去除后缀,容错变高
def weather_suffix(city:str)->str:
    """兼容用户输出的城市名称，北京市->北京"""
    for name in ["省","市","县","区"]:
        if city.endswith(name):
            return city[:-1]
    return city

@tool
def get_weather(city:str)->str:
    """获取到各地区的今日天气情况：天气情况、温度、空气质量
    Args:
        city：想要查询的地区名称
        """
    key=weather_suffix(city.strip())
    city_name=WEATHER_DB.get(key)
    if not city_name:
        return f"暂时查询不到{city}的天气情况,想要具体情况需要移步到app中查询"
    return (f"{city}的天气预报\n--------------\n"
            f"天气情况为：{city_name["condition"]}"
            f"天气温度为：{city_name["temp"]}"
            f"空气质量为：{city_name["aqi"]}"
            f"更新时间为{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")