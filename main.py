import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from tools.tianqi import get_weather
from tools.fanyi import Translate_language
from tools.devices import Air_conditioning,light_conditioning,curtain_conditioning,query_conditioning

load_dotenv()
System_prompt = """
你是小智，一个全能智能助手，也是全屋智能管家。你可以：
• 查询天气：查询中国主要城市天气
• 文本翻译：中/英/日互译
• 全屋智能控制：空调开关调温、灯光开关、窗帘开关
• 查询设备状态

工作原则：
1. 先理解用户意图，选择合适工具
2. 涉及设备控制前，先调用 query_device_status 确认现状
3. 不确定时向用户追问，不要臆测
4. 回答简洁明了
"""

def get_agent()->str:
    """创建智能体api链接"""
    llm=ChatDeepSeek(
        model="deepseek-v4-pro",
        temperature=0.2,
        api_key=os.getenv("deepseek_api_key"),
    )
    return create_agent(
        model=llm,
        tools=[Air_conditioning,light_conditioning,curtain_conditioning,query_conditioning,get_weather,Translate_language],
        system_prompt=System_prompt,
        checkpointer=MemorySaver(),
    )

def rule_fallback(user_input: str) -> str:
    """llm异常时候关键词容错"""
    Fault_tolerance=user_input.lower()
    rules = {"开灯": "灯光已开启（降级）", "关灯": "灯光已关闭（降级）",
             "开空调": "空调已开启（降级）", "关空调": "空调已关闭（降级）",
             "开窗帘": "窗帘已打开（降级）", "关窗帘": "窗帘已关闭（降级）"}
    for k,v in rules.items():
        if k in Fault_tolerance:
            return v
    return f"抱歉,我无法处理这个问题"

def main():
    print("=" * 50)
    print(" 小智 - 全屋智能助手 v2.0")
    print("=" * 50)
    print("输入 'quit' 退出\n")
    agent=get_agent()
    config={"configurable":{"thread_id":"main"}}
    while True:
         user_input=input("你：").strip()
         if user_input.lower() in ["quit","exit","退出"]:
             print("再见,拜拜")
             break
         if not user_input:
             continue
         try:
             res=agent.invoke(
                 {"messages":[{"role":"user","content":user_input}]},
                 config)
             print(f"小智：{res["messages"][-1].content}")
         except Exception as e:
             print(f"小智: {rule_fallback(user_input)}  [降级:{type(e).__name__}]")
if __name__=="__main__":
    main()

