#!/usr/bin/env bash
# EvalScope Offline 一键部署（Linux / macOS）
# 用法: ./install.sh [数据集缓存绝对路径]
# 说明: pip 局域网源已配置在全局（pip.conf / 环境变量），无需在此指定
set -euo pipefail

ROOT="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)"
CACHE_DIR="${1:-$ROOT/datasets_cache/modelscope}"

echo "==> 创建虚拟环境"
python -m venv .venv
source .venv/bin/activate

echo "==> 安装 evalscope 本体（离线 wheel）"
pip install --no-deps "$ROOT"/dist/evalscope-1.11.1-py3-none-any.whl

echo "==> 安装依赖（走全局 pip 源）"
pip install -r "$ROOT/requirements.txt"

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