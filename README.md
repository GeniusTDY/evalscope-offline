# EvalScope Offline（离线就绪）

基于 ModelScope 开源框架 **EvalScope**（一站式大模型评测）封装的**离线可用**部署包。

- 已剥离源码中所有中文 `#` 注释（不影响功能）。
- 内置 19 个评测基准的本地数据集缓存，可在**彻底断网**环境下直接执行本地大模型评测。
- 附完整冻结的环境依赖清单（`requirements.txt`）与前端 WebUI 构建产物。

## 目录结构

```
evalscope-offline/
├── evalscope/                     # EvalScope 项目源码（含 React WebUI 构建产物）
├── datasets_cache/                # 评测数据集缓存（离线加载来源）
│   └── modelscope/datasets/datasets/
├── requirements.txt               # 冻结的 Python 依赖（pip freeze）
└── README.md
```

## 支持（离线可用）的评测基准（19 个 / 约 225 个子集）

| 基准 | 子集数 | 基准 | 子集数 |
|---|---|---|---|
| gsm8k | 1 | bigcodebench_hard | 1 |
| competition_math | 5 | hellaswag | 1 |
| aime26 | 1 | winogrande | 1 |
| mmlu_redux | 57 | piqa | 1 |
| arc | 2 | ifeval | 1 |
| bbh | 27 | commonsense_qa | 1 |
| ceval | 52 | logi_qa | 1 |
| cmmlu | 67 | halueval | 3 |
| humaneval | 1 | bigcodebench | 1 |
| mbpp | 1 |  |  |

## 离线部署步骤（目标机需自带 Python 3.12 + 局域网 pip 源）

1. 安装依赖（走局域网 pip 源，全程不发外部网络）：

   ```bash
   python -m venv .venv
   .venv/bin/pip install -r requirements.txt \
       --index-url http://<局域网pip源>/simple/
   ```

   `requirements.txt` 为**顶层宽松清单**：锁定可离线复现的 `evalscope==1.11.1` 与 RAG 修复 `langchain-community<0.4`，其余依赖由 pip 从局域网源解析。完整解析结果另见 `requirements-lock.txt`（参考）。

2. 将本仓库的 `datasets_cache/` 放置到目标机，并导出缓存路径环境变量：

   ```bash
   export MODELSCOPE_CACHE=/绝对路径/datasets_cache/modelscope
   export EVALSCOPE_CACHE=/绝对路径/datasets_cache/modelscope/datasets
   ```

   > 说明：`RemoteDataLoader` 按 `$EVALSCOPE_CACHE/datasets/<数据名>-<hash>` 落盘查找，命中即走 `load_from_disk`，**不再联网**。

3. 开始评测（模型为你的本地模型，联网加载路径不参与）：

   ```bash
   evalscope eval --model /绝对路径/你的本地模型 ...
   ```

4. 启动 WebUI Dashboard（可选，离线可用）：

   ```bash
   evalscope service up
   ```

## 数据集

本仓库的 `datasets_cache/modelscope/datasets/datasets/` 内即包含上表全部 **19 个基准**的离线缓存，随仓库一起获取后放置到目标机即可，无需额外下载任何数据集。`trivia_qa`、`race` 两个基准及其数据已从本项目**彻底移除**（不提供、不部署）。

## 环境依赖

- `requirements.txt`：顶层、局域网源友好的可安装清单（`evalscope==1.11.1` + `langchain-community<0.4`）。
- `requirements-lock.txt`：本机已验证环境的完整 `pip freeze` 快照（约 273 个包），供局域网源缺失部分版本时核对/兜底。
- 需 3.12（本包在 3.12.13 上编译验证）。CPU 版 `torch` 及其 CUDA-free 依赖需存在于局域网源（transformers/modelscope 会传递依赖 torch）。