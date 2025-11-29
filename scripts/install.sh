#!/bin/bash

# 完整安装脚本 - 使用虚拟环境
# Complete Installation Script with Virtual Environment

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📧 邮件助手 - 自动安装程序"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 1. 检查 Python
echo "🔍 检查 Python 环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo ""
    echo "请先安装 Python 3.8 或更高版本："
    echo "  • 官方网站: https://python.org/downloads/macos/"
    echo "  • 使用 Homebrew: brew install python3"
    echo ""
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION"
echo ""

# 2. 创建虚拟环境
if [ -d "$VENV_DIR" ]; then
    echo "📦 虚拟环境已存在，跳过创建"
    echo "   位置: .venv/"
else
    echo "📦 创建虚拟环境..."
    python3 -m venv "$VENV_DIR"
    echo "✅ 虚拟环境创建成功"
    echo "   位置: .venv/"
fi
echo ""

# 2.5 配置 pip 使用国内镜像
if [ -f "$PROJECT_DIR/config/pip.conf" ]; then
    echo "⚙️  配置 pip 镜像源..."
    mkdir -p "$VENV_DIR/pip"
    cp "$PROJECT_DIR/config/pip.conf" "$VENV_DIR/pip.conf" 2>/dev/null || true
    export PIP_CONFIG_FILE="$PROJECT_DIR/config/pip.conf"
    echo "✅ 使用清华镜像源加速下载"
    echo ""
fi

# 3. 升级 pip（使用国内镜像加速）
echo "⬆️  升级 pip..."
CURRENT_PIP=$("$VENV_DIR/bin/pip" --version | awk '{print $2}')
echo "   当前版本: $CURRENT_PIP"

# 尝试升级 pip，如果失败则跳过
if "$VENV_DIR/bin/python" -m pip install --upgrade pip \
   -i https://pypi.tuna.tsinghua.edu.cn/simple \
   --timeout 30 --quiet 2>/dev/null; then
    NEW_PIP=$("$VENV_DIR/bin/pip" --version | awk '{print $2}')
    if [ "$CURRENT_PIP" != "$NEW_PIP" ]; then
        echo "✅ pip 已升级到 $NEW_PIP"
    else
        echo "✅ pip $CURRENT_PIP (已是最新)"
    fi
else
    echo "⚠️  pip 升级超时，使用当前版本 $CURRENT_PIP"
fi
echo ""

# 4. 安装依赖（使用国内镜像加速）
echo "📥 安装项目依赖..."

# 检查是否已安装 PyQt6
if "$VENV_DIR/bin/python" -c "import PyQt6" 2>/dev/null; then
    PYQT_VERSION=$("$VENV_DIR/bin/python" -c "import PyQt6; print(PyQt6.__version__)")
    echo "✅ PyQt6 $PYQT_VERSION 已安装"
else
    echo "   正在安装 PyQt6（使用清华镜像加速）..."
    echo "   这可能需要 1-2 分钟，请耐心等待..."
    
    if "$VENV_DIR/bin/pip" install PyQt6 \
       -i https://pypi.tuna.tsinghua.edu.cn/simple \
       --timeout 60 2>&1 | grep -v "^Collecting\|^Downloading\|^Installing"; then
        echo "✅ PyQt6 安装成功"
    else
        echo "⚠️  使用清华镜像失败，尝试官方源..."
        if "$VENV_DIR/bin/pip" install PyQt6 --timeout 60; then
            echo "✅ PyQt6 安装成功"
        else
            echo "❌ PyQt6 安装失败"
            exit 1
        fi
    fi
fi
echo ""

# 5. 验证安装
echo "🔍 验证安装..."
if "$VENV_DIR/bin/python" -c "import PyQt6" 2>/dev/null; then
    PYQT_VERSION=$("$VENV_DIR/bin/python" -c "import PyQt6; print(PyQt6.__version__)")
    echo "✅ PyQt6 $PYQT_VERSION"
    
    # 显示已安装的包
    echo ""
    echo "📦 已安装的包："
    "$VENV_DIR/bin/pip" list | grep -E "PyQt6|pip|setuptools" | sed 's/^/   /'
else
    echo "❌ PyQt6 验证失败"
    echo ""
    echo "请手动安装："
    echo "   source .venv/bin/activate"
    echo "   pip install PyQt6 -i https://pypi.tuna.tsinghua.edu.cn/simple"
    exit 1
fi
echo ""

# 6. 设置脚本权限
echo "🔧 设置脚本权限..."
chmod +x run.sh build_app.sh check_install.sh 2>/dev/null || true
echo "✅ 权限设置完成"
echo ""

# 7. 创建 .gitignore
if [ ! -f ".gitignore" ]; then
    echo "📝 创建 .gitignore..."
    cat > .gitignore << 'GITIGNORE'
# 虚拟环境
.venv/
venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# 打包文件
build/
dist/
*.egg-info/
*.spec

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# macOS
.DS_Store
.AppleDouble
.LSOverride

# 用户配置（包含敏感信息）
config.ini
*.log
GITIGNORE
    echo "✅ .gitignore 创建成功"
    echo ""
fi

# 8. 完成总结
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎉 安装完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 安装信息："
echo "   • Python:  $PYTHON_VERSION"
echo "   • pip:     $PIP_VERSION"
echo "   • PyQt6:   $PYQT_VERSION"
echo "   • 虚拟环境: .venv/"
echo ""
echo "🚀 现在可以运行程序了："
echo ""
echo "   方法1（推荐）: ./run.sh"
echo "   方法2: source .venv/bin/activate && python email_assistant_gui.py"
echo ""
echo "📖 查看使用说明："
echo "   cat 开始使用.md"
echo ""
echo "💡 提示："
echo "   • 虚拟环境位于 .venv/ 目录"
echo "   • 已添加到 .gitignore，不会提交到 Git"
echo "   • 如需重新安装: rm -rf .venv && ./install.sh"
echo "   • 使用清华镜像源加速下载"
echo ""
echo "🌐 如果安装太慢，可以手动指定镜像源："
echo "   pip install PyQt6 -i https://pypi.tuna.tsinghua.edu.cn/simple"
echo ""
