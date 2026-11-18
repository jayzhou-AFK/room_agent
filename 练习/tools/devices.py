from langchain_core.tools import tool
#内存设置
_STATE = {"ac_on": False, "ac_temp": 26, "light_on": False, "curtain_open": True}

@tool
def Air_conditioning(on:bool,temp:int=26)->str:
    """控制空调开关温度，仅限于在16度-30度之间
    Args:
        on：判断空调是否为打开状态
        temp：空调当前设置的温度
    """
    _STATE["ac_on"]=on
    if on:
        _STATE["ac_temp"]=max(16,min(30,temp))
        return f"空调已打开,当前温度为：{_STATE['ac_temp']}"
    return "空调已关闭"

@tool
def light_conditioning(on:bool)->str:
    """控制室内灯光开启
    Args:
        on：判断灯光是否打开-->True为打开，False为关闭
    """
    _STATE["light_on"]=on
    return f"室内灯光已开启" if on else f"室内灯光已关闭"

@tool
def curtain_conditioning(on:bool)->str:
    """控制室内窗帘打开开关
    Args:
        on：判断窗帘是否打开-->True为打开，False为关闭
    """
    _STATE["curtain_open"]=on
    return "窗帘已打开" if on else "窗帘已关闭"

@tool
def query_conditioning()->str:
    """查询室内设备的状态(判断是否正常运行)"""
    return (f"空调：{"开" if _STATE["ac_on"] else "关"}{_STATE["ac_temp"],}"
            f"灯光：{"开" if _STATE["light_on"] else "关"}"
            f"窗帘：{"开" if _STATE["curtain_open"] else "关"}")