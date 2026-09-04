#!/usr/bin/env bash
# EvalScope Offline 一键部署（Linux / macOS）
# 用法: ./install.sh <局域网pip源URL> [数据集缓存绝对路径]
#   <URL> 必填，形如 http://192.168.1.10/simple/
#   [路径] 可选，默认取仓库内置 datasets_cache/modelscope
set -euo pipefail

INDEX_URL="${1:?用法: ./install.sh <局域网pip源URL> [数据集缓存绝对路径]}"
ROOT="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
CACHE_DIR="${2:-$ROOT/datasets_cache/modelscope}"

echo "==> 创建虚拟环境"
python -m venv .venv
source .venv/bin/activate

echo "==> 安装 evalscope 本体（离线 wheel）"
pip install --no-deps "$ROOT"/dist/evalscope-1.11.1-py3-none-any.whl

echo "==> 安装依赖（局域网源: $INDEX_URL）"
pip install -r "$ROOT/requirements.txt" --index-url "$INDEX_URL"

echo
echo "============================================="
echo "  部署完成。下一步配置数据集缓存环境变量："
echo "============================================="
echo "  在 ~/.bashrc 追加："
echo "  export MODELSCOPE_CACHE=$CACHE_DIR"
echo "  export EVALSCOPE_CACHE=$CACHE_DIR/datasets"
echo "  然后执行: source ~/.bashrc"
echo
echo "  可用命令验证:"
echo "  evalscope --help"
echo "  evalscope benchmark-info --list"
echo "============================================="