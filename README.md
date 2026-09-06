# EvalScope Offline

EvalScope 的**断网可用**封装：对本地大模型做评测、压测与 WebUI 看板。
已剔除源码中文注释，内置 19 个基准的数据缓存；`race` / `trivia_qa` 已彻底移除。

---

## 目录

| 路径 | 说明 |
|---|---|
| `evalscope/` | 源码（含 `web/dist` 前端） |
| `datasets_cache/` | 19 个基准的数据缓存（离线加载） |
| `dist/*.whl` | 免编译 wheel 安装包 |
| `install.sh` | 一键部署脚本（Linux） |
| `pyproject.toml` | wheel 构建配置 |
| `requirements.txt` | 依赖清单（走局域网源） |
| `requirements-lock.txt` | pip freeze 快照（兜底参考） |

---

## 部署（离线机）

前置：**Python 3.12** + 局域网 pip 源已配置在 pip 全局配置中。

**一键部署**（自动建 venv → 装 wheel → 装依赖）
```bash
./install.sh
```

若走手动，步骤如下：

| 步骤 | 命令 |
|---|---|
| 建环境 | `python -m venv .venv` |
| 激活 | `source .venv/bin/activate` |
| 装本体 | `pip install --no-deps dist/evalscope-1.11.1-py3-none-any.whl` |
| 装依赖 | `pip install -r requirements.txt`（pip 源走全局配置） |
| 数据缓存 | `export MODELSCOPE_CACHE=...`；`export EVALSCOPE_CACHE=...` |

数据缓存环境变量（`MODELSCOPE_CACHE` 指到 `datasets_cache/modelscope`，`EVALSCOPE_CACHE` 为 `.../datasets`）写入 `~/.bashrc` 即可。

> 勿用 PYTHONPATH 引入源码安装，会报 `collections` 遮蔽错误。

---

## 使用

**列出可用基准**
```bash
evalscope benchmark-info --list
```

**评测本地模型**
```bash
evalscope eval --model /本地模型权重 --datasets gsm8k
```

**评测 OpenAI 兼容服务（含局域网）**
```bash
evalscope eval --model M \
    --api-url http://host:port/v1/chat/completions \
    --datasets gsm8k
```

**性能压测**
```bash
evalscope perf --api openai \
    --url http://host:8000/v1/chat/completions \
    -n 500 --parallel 16
```

**WebUI 看板**
```bash
evalscope service --host 0.0.0.0 --port 9000   # 访问 /dashboard
```

结果统一落在 `outputs/`；可用 `--limit N` 限制样本量。

---

## 评测基准（19 个 / 约 225 子集）

| 基准 | 子集 | 基准 | 子集 |
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

---

## FAQ

| 问题 | 处理 |
|---|---|
| `collections` 报错 | 改用 `pip install dist/*.whl`，勿用 PYTHONPATH |
| 数据联网 / 403 | `$EVALSCOPE_CACHE` 未设置或指向不对 |
| 压测连不上 | 目标须为 OpenAI 兼容，`--url` 带 `/v1/chat/completions`，有鉴权加 `--api-key` |
| 局域网源缺包 | 对照 `requirements-lock.txt` 核对版本 |
| WebUI 启动失败 | 命令是 `service`（无 `up`） |