# EvalScope Offline —— 详细部署方案与使用教程

> 本文档适用于 **离线断网电脑** 上部署 EvalScope 离线版，并完成本地大模型评测、性能压测与 WebUI 看板的完整流程。
> 配套说明请见 [README.md](README.md)。

---

## 一、总体说明

本包是 ModelScope 开源评测框架 **EvalScope** 的离线封装，目标是在**全程不连外网**的电脑上，对本地大模型或局域网内 OpenAI 兼容服务进行评测。

**能力范围（均可离线使用）**
- 19 个评测基准、约 225 个子集的本地评测
- OpenAI 兼容协议服务的性能压测（含局域网内服务）
- WebUI 交互式可视化看板（多维对比、报告概览与详情）

**不包含（按你的取舍）**
- 外部搜索/检索类工具评测
- 依赖评测大模型的 LLM-as-Judge
- 需要 Docker 的沙箱类基准

**离线边界（唯一的非仓库可离线下发项）**
仓库内所有可事先打包的东西（evalscope 本体 wheel、19 个基准的数据缓存、WebUI 前端）均已离线就位且实测可用。唯一需要外部准备的是 **Python 3.12** 与一台 **局域网 pip 源**，用于安装 evalscope 的三方依赖（transformers / modelscope / torch 等）。这与仓库本身无关，无法随仓库提供。

---

## 二、仓库内容与目录

```
evalscope-offline/
├── evalscope/                     # 源码（含 React WebUI 构建产物 evalscope/web/dist）
│   └── web/dist/                  # WebUI 前端成品（已入库）
├── datasets_cache/                # 19 个基准的数据缓存（离线加载来源）
│   └── modelscope/datasets/datasets/
├── dist/
│   └── evalscope-1.11.1-py3-none-any.whl   # 免编译安装包
├── pyproject.toml                 # wheel 构建配置
├── requirements.txt               # 顶层依赖清单（evalscope==1.11.1 + langchain-community<0.4）
├── requirements-lock.txt          # 完整 pip freeze 快照（参考/兜底）
└── README.md
```

拷贝时需将**整个文件夹**复制到离线机，重点确保 `dist/`、`datasets_cache/`、`evalscope/web/dist/` 完整（后两者较大，切勿遗漏）。

---

## 三、部署前置条件

| 项 | 要求 | 说明 |
|---|---|---|
| Python | 3.12 | 建议 3.12.13+，已在本版上编译验证 |
| pip 源 | 一台局域网 pip 镜像地址 | 格式如 `http://192.168.x.x/simple/` |
| 本地模型 | （评测用）本地权重目录 | HF/Modelscope 格式，或局域网 OpenAI 兼容服务 |
| 磁盘 | ≥ 5 GB 可用 | datasets_cache 约 756 MB + 依赖 + 模型权重 |

---

## 四、详细部署步骤（离线机）

### 1. 确认 Python 版本
```bash
python --version        # 必须是 3.12.x
```

### 2. 创建虚拟环境
```bash
cd /path/to/evalscope-offline
python -m venv .venv
source .venv/bin/activate
```

### 3. 安装 evalscope 本体（离线、免编译）
```bash
pip install --no-deps dist/evalscope-1.11.1-py3-none-any.whl
```
> 这一步零联网、零编译。**切勿**改用 `PYTHONPATH=...` 顶层引入源码的方式装（会导致 `collections` 被遮蔽报错），见常见问题。

### 4. 安装其余依赖（走局域网源）
```bash
pip install -r requirements.txt \
    --index-url http://<局域网pip源>/simple/
```
- `requirements.txt` 中的 `evalscope==1.11.1` 已被第 3 步的 wheel 满足，pip 不会重复下载，只解析并安装 evalscope 的三方传递依赖。
- 若局域网源缺少个别版本，可参照 `requirements-lock.txt` 核对版本号（优先同版本，其次微调）。

### 5. 配置离线数据集缓存
将以下两行写入 `~/.bashrc`（或每次终端执行）：
```bash
export MODELSCOPE_CACHE=/绝对路径/evalscope-offline/datasets_cache/modelscope
export EVALSCOPE_CACHE=/绝对路径/evalscope-offline/datasets_cache/modelscope/datasets
```
```bash
source ~/.bashrc
```
> `RemoteDataLoader` 会按 `$EVALSCOPE_CACHE/datasets/<数据名>-<hash>` 落盘查找，命中即走 `load_from_disk`，**不再联网**。这两行必须正确设置，否则数据集加载会尝试联网并失败。

### 6. 冒烟验证（可选但建议）
```bash
evalscope --help                              # CLI 可用
evalscope benchmark-info --list               # 看到基准清单即注册成功
python -c "import evalscope; print(evalscope.__version__)"
```

---

## 五、使用教程

### 5.1 列出可用基准
```bash
evalscope benchmark-info --list
```
查看单个基准详情：
```bash
evalscope benchmark-info gsm8k
evalscope benchmark-info gsm8k --format json    # JSON 输出
```

### 5.2 评测本地模型（`evalscope eval`）
```bash
# 单基准
evalscope eval \
  --model /绝对路径/你的本地模型 \
  --datasets gsm8k

# 多基准（空格分隔）
evalscope eval \
  --model /绝对路径/你的本地模型 \
  --datasets gsm8k mmlu_redux arc \
  --limit 200 \
  --repeats 2
```
**常用参数**

| 参数 | 作用 |
|---|---|
| `--model` | 本地模型目录路径（或 Modelscope 模型 id） |
| `--datasets` | 基准名列表，空格分隔（见第六节） |
| `--limit` | 每个子集最多取 N 条样本，快速验证/省时 |
| `--repeats` | 重复次数，用于 k-metrics |
| `--generation-config` | 解码参数 JSON，如 `'{"max_tokens":1024,"temperature":0.0,"stream":true}'` |
| `--model-id` | 报告中显示的模型名（可自定义） |
| `--use-cache` | 复用历史结果目录继续评测 |
| `--work-dir` | 输出缓存根目录（默认 `outputs/`） |

评测结果写入 `outputs/` 下带时间戳的目录，含各基准指标与报告。

### 5.3 评测 OpenAI 兼容 API（本地或局域网）
```bash
evalscope eval \
  --model 你的模型名 \
  --api-url http://192.168.1.10:8000/v1/chat/completions \
  --api-key EMPTY \
  --datasets gsm8k
```
- 该 `--api-url` 指向**任意** OpenAI 兼容服务（包括局域网内的推理服务），无需在离线机上加载模型。
- `--api-key` 服务有鉴权就给 token，否则给 `EMPTY`。

### 5.4 性能压测（`evalscope perf`）
对 **OpenAI 兼容** 的模型服务做负载压测，产出 TTFT、TPOT、吞吐量等指标。
```bash
# 压测局域网内模型服务（OpenAI 协议）
evalscope perf \
  --model 你的模型名 \
  --api openai \
  --url http://192.168.1.20:8000/v1/chat/completions \
  --api-key EMPTY \
  --number 500 \
  --parallel 16 \
  --max-prompt-length 2048
```
**关键参数**

| 参数 | 作用 |
|---|---|
| `--api` | 服务协议，默认 `openai`（局域网 OpenAI 兼容用这个） |
| `--url` | 服务完整端点（OpenAI 兼容地址） |
| `--number` / `-n` | 压测请求数 |
| `--parallel` | 并发请求数 |
| `--dataset` | 压测数据源（默认 `openqa` 通用问答），也支持 `--dataset-path` 传自定义文件 |
| `--max-prompt-length` / `--min-prompt-length` | 输入长度上下限 |
| `--stream` | 是否流式（采集 TTFT 需 `--stream`） |
| `--api-key` | 鉴权 key，无则 `EMPTY` |

结果写入 `outputs/`，含响应时延分布、吞吐、并发成功率等。

### 5.5 WebUI 可视化看板（`evalscope service`）
```bash
evalscope service --host 0.0.0.0 --port 9000
```
- 浏览器访问 `http://<离线机IP>:9000/`，默认看板页在 `/dashboard`。
- 支持：多模型多维对比、评测报告概览与详情、任务查看。前端资源已打包在 wheel/仓库内，**离线可用**。
- 局域网其他机器只需能访问该 IP 即可打开看板。

### 5.6 评测结果解读
- 所有任务与压测结果统一落在 `outputs/` 的时间戳目录。
- 文本基准输出 Accuracy/EM 等指标；压测输出吞吐、时延分位与并发统计。
- 在 WebUI `/dashboard` 中可直观对比。

---

## 六、内置评测基准（19 个 / 约 225 个子集）

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

> `race`、`trivia_qa` 已按要求**彻底移出**（源码、注册表、数据缓存、WebUI 均不含）。

---

## 七、常见问题与排查

| 现象 | 原因 / 解决 |
|---|---|
| `ImportError: import collections ...` | 用了 PYTHONPATH 顶层引入源码。必须 `pip install dist/*.whl` 正常安装 |
| 数据集加载时联网/报 403 | `$EVALSCOPE_CACHE` 未设置或路径不对。确认第 5 步两行环境变量指向仓库内 `datasets_cache/` |
| 提示找不到某个数据子集 | 该基准不在 19 个内置范围内（如已移除的 race/trivia_qa） |
| 局域网 pip 源缺某版本 | 参照 `requirements-lock.txt` 调整版本号，或确认源已同步所需包 |
| 评测太慢 / 内存吃紧 | 加 `--limit`（如 `--limit 200`）先行小规模验证 |
| 压测连接失败 | 确认目标服务是 **OpenAI 兼容协议**、网络可达、`--url` 含 `/v1/chat/completions`、有鉴权时提供 `--api-key` |
| 执行 `evalscope service up` 报错 | 本版正确命令为 `evalscope service --host ... --port ...`（`up` 为旧写法已废弃） |

---

## 八、（可选）从源码重新构建 wheel

若需在联网/可编译机器上重新生成 wheel（例如后续改动源码）：
```bash
pip install --upgrade build setuptools wheel
cd evalscope-offline
pip wheel -w dist . --no-deps
```
产物为 `dist/evalscope-1.11.1-py3-none-any.whl`，拷贝到离线机后按第四节第 3 步安装即可。