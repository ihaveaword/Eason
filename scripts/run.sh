#!/bin/bash

# 快速启动脚本
# Quick Start Script

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

cd "$PROJECT_DIR"

# 检查虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "⚠️  未找到虚拟环境，正在安装..."
    echo ""
    "$PROJECT_DIR/scripts/install.sh"
    echo ""
fi

# 检查依赖
if ! "$VENV_DIR/bin/python" -c "import PyQt6" 2>/dev/null; then
    echo "⚠️  PyQt6 未安装，正在自动安装..."
    echo ""
    "$PROJECT_DIR/scripts/install.sh"
    echo ""
    
    # 再次验证
    if ! "$VENV_DIR/bin/python" -c "import PyQt6" 2>/dev/null; then
        echo "❌ 安装失败，请手动安装："
        echo ""
        echo "   source .venv/bin/activate"
        echo "   pip install PyQt6 -i https://pypi.tuna.tsinghua.edu.cn/simple"
        echo ""
        exit 1
    fi
fi

# 运行应用
echo "🚀 启动邮件助手..."
echo ""
"$VENV_DIR/bin/python" email_assistant_gui.py
