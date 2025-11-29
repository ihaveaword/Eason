#!/bin/bash

# 快速修复安装问题
# Quick Fix Installation Issues

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🔧 邮件助手 - 安装问题修复工具"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 删除旧的虚拟环境
if [ -d "$VENV_DIR" ]; then
    echo "🗑️  删除旧的虚拟环境..."
    rm -rf "$VENV_DIR"
    echo "✅ 已删除"
else
    echo "ℹ️  虚拟环境不存在"
fi
echo ""

# 2. 清理缓存
echo "🧹 清理 pip 缓存..."
python3 -m pip cache purge 2>/dev/null || echo "   缓存已清理或不存在"
echo ""

# 3. 重新创建虚拟环境
echo "📦 重新创建虚拟环境..."
python3 -m venv "$VENV_DIR"
echo "✅ 虚拟环境创建成功"
echo ""

# 4. 使用镜像源安装
echo "📥 使用清华镜像源安装 PyQt6..."
echo "   这将花费 1-2 分钟..."
echo ""

"$VENV_DIR/bin/pip" install --upgrade pip setuptools wheel \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --timeout 60

echo ""
echo "📥 安装 PyQt6..."
"$VENV_DIR/bin/pip" install PyQt6 \
    -i https://pypi.tuna.tsinghua.edu.cn/simple \
    --timeout 120 \
    --no-cache-dir

echo ""

# 5. 验证
echo "🔍 验证安装..."
if "$VENV_DIR/bin/python" -c "import PyQt6; print('PyQt6 版本:', PyQt6.__version__)" 2>/dev/null; then
    echo "✅ 安装成功！"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🎉 修复完成！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "现在可以运行: ./run.sh"
    echo ""
else
    echo "❌ 安装仍然失败"
    echo ""
    echo "可能的原因："
    echo "  1. 网络问题 - 请检查网络连接"
    echo "  2. Python 版本太低 - 需要 Python 3.8+"
    echo "  3. 防火墙阻止 - 检查防火墙设置"
    echo ""
    echo "手动安装步骤："
    echo "  1. source .venv/bin/activate"
    echo "  2. pip install PyQt6 -i https://mirrors.aliyun.com/pypi/simple/"
    echo "  3. 或尝试其他镜像源（见 pip.conf）"
    echo ""
    exit 1
fi
