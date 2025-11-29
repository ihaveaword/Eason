#!/bin/bash

# Eason 打包脚本
# Eason Build Script

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
VENV_DIR="$PROJECT_DIR/.venv"

cd "$PROJECT_DIR"

echo "📦 开始打包 Eason 应用..."
echo ""

# 检查虚拟环境
if [ ! -d "$VENV_DIR" ]; then
    echo "⚠️  未找到虚拟环境，正在创建..."
    "$PROJECT_DIR/scripts/install.sh"
    echo ""
fi

# 检查依赖
echo "📋 检查依赖..."
if ! "$VENV_DIR/bin/python" -c "import PyQt6" 2>/dev/null; then
    echo "⚠️  未找到 PyQt6，正在安装..."
    "$VENV_DIR/bin/pip" install PyQt6
fi

if ! "$VENV_DIR/bin/pip" show pyinstaller > /dev/null 2>&1; then
    echo "⚠️  未找到 PyInstaller，正在安装..."
    "$VENV_DIR/bin/pip" install pyinstaller
fi

echo "✅ 依赖检查完成"
echo ""

# 清理旧文件
echo "🧹 清理旧构建文件..."
rm -rf build dist *.spec

# 检查图标文件
if [ -f "Eason.icns" ]; then
    ICON_OPTION="--icon=Eason.icns"
    echo "✅ 使用自定义图标: Eason.icns"
else
    ICON_OPTION=""
    echo "⚠️  未找到图标文件，使用默认图标"
fi

# 打包应用
echo "🔨 开始打包..."
echo "   这可能需要几分钟，请耐心等待..."
echo ""

"$VENV_DIR/bin/pyinstaller" --noconsole \
            --onedir \
            --name="Eason" \
            --windowed \
            --osx-bundle-identifier=com.eason.emailassistant \
            ${ICON_OPTION} \
            email_assistant_gui.py

# 检查结果
if [ -d "dist/Eason.app" ]; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ✅ 打包成功！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📂 应用位置:"
    echo "   $PROJECT_DIR/dist/Eason.app"
    echo ""
    echo "📊 应用信息:"
    APP_SIZE=$(du -sh "dist/Eason.app" | awk '{print $1}')
    echo "   大小: $APP_SIZE"
    echo ""
    echo "🚀 测试运行:"
    echo "   open dist/Eason.app"
    echo ""
    echo "📦 分发方式:"
    echo "   1. 直接复制 Eason.app 到其他 Mac"
    echo "   2. 压缩: zip -r Eason.zip dist/Eason.app"
    echo "   3. 上传到 GitHub Release 供用户下载"
    echo ""
    echo "⚠️  注意事项:"
    echo "   • 首次运行可能需要在「系统偏好设置」→「安全性与隐私」中允许"
    echo "   • 建议进行代码签名以避免安全警告"
    echo ""
    
    # 询问是否立即运行应用
    read -p "是否立即运行应用测试？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在启动 Eason..."
        open "dist/Eason.app"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🎉 打包完成！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo ""
    echo "❌ 打包失败，请查看上面的错误信息"
    echo ""
    exit 1
fi
