# 🤖 小智 · 全屋智能多工具 AI Agent 系统

> 一个基于 **LangChain + LangGraph + DeepSeek** 构建的全屋智能 AI Agent，
> 支持自然语言驱动的设备控制、天气查询与多语言翻译，
> 具备**多轮记忆、工具自主调用、异常降级**等生产级工程特性。

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.3+-green)
![LangGraph](https://img.shields.io/badge/LangGraph-0.2+-orange)
![DeepSeek](https://img.shields.io/badge/LLM-DeepSeek-purple)

---

## 📌 项目背景

传统智能家居依赖**硬编码 if-else 规则**响应指令，存在三个痛点：

| 痛点 | 说明 |
|---|---|
| 语义僵化 | 无法理解"我有点冷但别直吹"这类模糊、多约束指令 |
| 扩展困难 | 新增设备/场景需改主流程代码，牵一发动全身 |
| 缺乏记忆 | 每次对话独立，"再调低两度"无法识别上文 |

本项目通过引入 **LLM Agent 架构**，由大模型自主完成 **意图理解 → 工具选择 → 任务执行**，
将"设备接入"与"决策逻辑"解耦，实现自然语言到跨设备动作的端到端闭环。

---

## ✨ 核心特性

- **🧠 多工具自主调度**：内置 6 个 Tools，LLM 根据语义自主选型调用（Function Calling）
- **💬 多轮对话记忆**：基于 LangGraph `MemorySaver` + `thread_id`，支持上下文追问
- **🛡️ 异常降级兜底**：LLM/网络异常时自动切换关键词规则引擎，保证服务不中断
- **🔌 分层架构设计**：Tool 层 / Agent 层 / 设备层解耦，替换真实 IoT SDK 时上层无感知
- **🌐 真实 LLM 翻译**：主路径调用 LLM 翻译，异常时降级本地词典，兼顾质量与可用性

---

## 🏗️ 系统架构
┌─────────────────────────┐
│ 用户自然语言输入 │
└───────────┬─────────────┘
▼
┌─────────────────────────┐
│ Agent 编排层 (main.py) │
│ create_agent + Memory │
└───────────┬─────────────┘
▼
┌─────────────────┴─────────────────┐
▼ ▼
┌────────────────┐ ┌────────────────┐
│ LLM 决策引擎 │ │ 异常降级引擎 │
│ (DeepSeek) │◄──try/except───►│ rule_fallback │
└───────┬────────┘ └────────────────┘
▼ 自主选择工具
┌──────────┴──────────────────────────────────┐
▼ ▼ ▼ ▼
┌────────┐ ┌────────┐ ┌──────────────┐ ┌──────────────┐
│ 天气工具│ │ 翻译工具│ │ 设备控制工具 │ │ 设备状态查询 │
└───┬────┘ └───┬────┘ └──────┬───────┘ └──────┬───────┘
▼ ▼ ▼ ▼
┌──────────────────────────────────────────────────────┐
│ 数据/设备层（可替换真实IoT SDK） │
│ WEATHER_DB | LLM翻译/词典 | 设备状态机 _STATE │
└──────────────────────────────────────────────────────┘

text

**分层说明**：

| 层级 | 职责 | 文件 |
|---|---|---|
| 编排层 | Agent 构建、对话循环、异常降级 | `main.py` |
| 工具层 | 将能力标准化封装为 LLM 可调用的 Tool | `tools/*.py` |
| 设备层 | 设备状态与数据（可替换真实 API） | 各 Tool 内部 |

---

## 📁 项目结构
xiaozhi-agent/
├── main.py # 主入口：Agent 编排 + 对话循环 + 降级兜底
├── tools/
│ ├── init.py
│ ├── weather.py # 天气查询工具（城市归一化 + 本地数据）
│ ├── translation.py # 翻译工具（LLM 主路径 + 词典降级）
│ └── devices.py # 全屋设备控制工具（空调/灯光/窗帘/状态）
├── .env.example # 环境变量模板
├── requirements.txt # 依赖清单
└── README.md

text

---

## 🛠️ 技术栈

| 类别 | 技术 |
|---|---|
| 语言 | Python 3.10+ |
| Agent 框架 | LangChain `create_agent` |
| 状态记忆 | LangGraph `MemorySaver` |
| 大模型 | DeepSeek (`langchain-deepseek`) |
| 工具定义 | LangChain `@tool` 装饰器 |
| 环境管理 | python-dotenv |

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourname/xiaozhi-agent.git
cd xiaozhi-agent




