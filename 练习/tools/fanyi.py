import os
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek

_language_text={
    "你好": {"英文": "hello", "日文": "こんにちは"},
    "谢谢": {"英文": "thank you", "日文": "ありがとう"},
}
_LANG_MAP = {"英文": "English", "日文": "Japanese", "中文": "Chinese"}

@tool
def Translate_language(text:str,text_language:str)->str:
    """将用户问题翻译成目标语言（仅限支持中文、英文、日文）
    Args:
        text：用户传的语言
        text_language:翻译后的目标语言
        """
    target=_LANG_MAP.get(text_language)
    if not target:
        return f"我暂时无法将你这段文本按照{text_language}翻译,可选翻译为：英文/日文/中文"
    try:
        llm=ChatDeepSeek(
            model="deepseek-v4-pro",
            api_key="",
            temperature=0
        )
        res=llm.invoke(f"把下面的文本翻译成{target},原文为：{text}")
        return res.content.strip()
    except Exception as e:
        #降级,保底措施
        resp=_language_text.get(text,{}).get(text_language)
        return f"{text}的{text_language}翻译是{resp}" if resp else f"翻译服务暂不可用（已降级），无法翻译：{text}"