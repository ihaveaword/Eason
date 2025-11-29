#!/bin/bash

# 邮件助手打包脚本
# Email Assistant Build Script

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

cd "$PROJECT_DIR"

echo "📦 开始打包邮件助手应用..."
echo ""

# 检查虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "⚠️  未找到虚拟环境，正在创建..."
    ./install.sh
    echo ""
fi

# 检查依赖
echo "📋 检查依赖..."
if ! "$VENV_DIR/bin/python" -c "import PyQt6" 2>/dev/null; then
    echo "⚠️  未找到 PyQt6，正在安装..."
    "$VENV_DIR/bin/pip" install PyQt6
fi

if ! "$VENV_DIR/bin/python" -c "import Pyinstaller" 2>/dev/null; then
    echo "⚠️  未找到 PyInstaller，正在安装..."
    "$VENV_DIR/bin/pip" install pyinstaller
fi

echo "✅ 依赖检查完成"
echo ""

# 清理旧文件
echo "🧹 清理旧构建文件..."
rm -rf build dist *.spec

# 打包应用
echo "🔨 开始打包..."
"$VENV_DIR/bin/pyinstaller" --noconsole \
            --onefile \
            --name="邮件助手" \
            --windowed \
            --osx-bundle-identifier=com.emailassistant.batchsender \
            email_assistant_gui.py

# 检查结果
if [ -f "dist/邮件助手.app/Contents/MacOS/邮件助手" ]; then
    echo ""
    echo "✅ 打包成功！"
    echo ""
    echo "📂 应用位置: dist/邮件助手.app"
    echo ""
    echo "🚀 运行应用:"
    echo "   open dist/邮件助手.app"
    echo ""
    echo "📦 分发应用:"
    echo "   将 dist/邮件助手.app 复制到其他 Mac 即可使用"
    echo ""
    
    # 询问是否打开应用
    read -p "是否立即运行应用？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open "dist/邮件助手.app"
    fi
else
    echo "❌ 打包失败，请查看错误信息"
    exit 1
fi
