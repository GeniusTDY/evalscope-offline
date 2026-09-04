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

## 离线部署步骤

1. 安装依赖：

   ```bash
   python -m venv .venv
   .venv/bin/pip install -r requirements.txt
   ```

2. 将本仓库的 `datasets_cache/` 放置到目标机，并导出缓存路径环境变量：

   ```bash
   export MODELSCOPE_CACHE=/绝对路径/datasets_cache/modelscope
   export EVALSCOPE_CACHE=/绝对路径/datasets_cache/modelscope/datasets
   ```

   > 说明：`RemoteDataLoader` 按 `$EVALSCOPE_CACHE/datasets/<数据名>-<hash>` 落盘查找，命中即走 `load_from_disk`，**不再联网**。

3. 导入本仓库的 `evalscope` 源码包，或将其置于 `sys.path`，即可开始评测：

   ```bash
   evalscope eval --model <你的本地模型> ...
   ```

4. 启动 WebUI Dashboard（可选，离线可用）：

   ```bash
   evalscope service up
   ```

## 排除的数据集（重要）

以下两个基准因**单文件超过 GitHub 100MB 硬上限**（trivia_qa ≈ 410MB、race ≈ 120MB）未包含在本仓库中。断网使用前，请另行放置其缓存到

```
datasets_cache/modelscope/datasets/datasets/
```

目录，或提前联网预热使其落盘：

- **trivia_qa**（精简版，仅 `rc.wikipedia` validation）
- **race**（high / middle）

## 环境依赖

`requirements.txt` 由安装环境的 `pip freeze` 生成，共计约 273 个包，覆盖评测、WebUI、远端 API 压测等全部启用功能所依赖的第三方库。