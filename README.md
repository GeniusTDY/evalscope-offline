# EvalScope Offline

EvalScope 的离线封装：**断网**环境下对本地大模型做评测、压测与 WebUI 看板。已剔除源码中文注释，内置 19 个基准的数据缓存，`race`/`trivia_qa` 已彻底移除。

## 目录

```
evalscope/           源码（含 web/dist WebUI 前端）
datasets_cache/      19 个基准的数据缓存（离线加载）
dist/*.whl           免编译 wheel 安装包
pyproject.toml       wheel 构建配置
requirements.txt     依赖清单（局域网 pip 源用）
requirements-lock.txt  pip freeze 快照（兜底参考）
```

## 部署（离线机）

前置：Python 3.12 + 局域网 pip 源。

```bash
python -m venv .venv && source .venv/bin/activate
pip install --no-deps dist/evalscope-1.11.1-py3-none-any.whl      # 装本体（离线）
pip install -r requirements.txt --index-url http://<局域网pip源>/simple/   # 装依赖
```

配置数据集缓存（写入 `~/.bashrc`）：

```bash
export MODELSCOPE_CACHE=/绝对路径/datasets_cache/modelscope
export EVALSCOPE_CACHE=/绝对路径/datasets_cache/modelscope/datasets
```

> 勿用 PYTHONPATH 引入源码装（会报 `collections` 遮蔽）。

## 常用命令

```bash
evalscope benchmark-info --list                        # 列出基准
evalscope eval --model /本地模型权重 --datasets gsm8k  # 评测本地模型
evalscope eval --model M --api-url http://host:port/v1/chat/completions --datasets gsm8k  # 测 OpenAI 兼容服务
evalscope perf --api openai --url http://host:8000/v1/chat/completions -n 500 --parallel 16  # 压测
evalscope service --host 0.0.0.0 --port 9000           # WebUI（/dashboard）
```

评测与压测结果在 `outputs/`。常用 `--limit N` 限制样本量。

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

## FAQ

- `collections` 报错：改用 `pip install dist/*.whl` 装，勿用 PYTHONPATH。
- 数据集联网/403：`$EVALSCOPE_CACHE` 未设置或指向不对。
- 压测连不上：目标须为 OpenAI 兼容协议，`--url` 带 `/v1/chat/completions`，有鉴权加 `--api-key`。
- 局域网源缺包：按 `requirements-lock.txt` 对照版本。
- WebUI 启动命令是 `service`（无 `up`）。