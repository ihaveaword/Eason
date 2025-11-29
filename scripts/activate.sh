#!/bin/bash

# 激活虚拟环境脚本
# Activate Virtual Environment Script

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    echo "❌ 虚拟环境不存在"
    echo ""
    echo "请先运行: ./install.sh"
    exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📧 邮件助手 - 虚拟环境"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "虚拟环境位置: .venv/"
echo ""
echo "激活虚拟环境："
echo "  source .venv/bin/activate"
echo ""
echo "退出虚拟环境："
echo "  deactivate"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 注意：这个脚本不能直接激活环境，需要用户手动执行 source 命令
echo "💡 请执行以下命令激活虚拟环境："
echo ""
echo "   source .venv/bin/activate"
echo ""
