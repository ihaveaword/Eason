#!/bin/bash

# 安装检查脚本
# Installation Check Script

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📧 邮件助手 - 环境检查工具"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查结果计数
pass_count=0
fail_count=0

# 1. 检查 Python
echo "🔍 检查 Python..."
if command -v python3 &> /dev/null; then
    version=$(python3 --version)
    echo "   ✅ $version"
    ((pass_count++))
else
    echo "   ❌ 未找到 Python 3"
    echo "      请访问 https://python.org 下载安装"
    ((fail_count++))
fi
echo ""

# 2. 检查虚拟环境
echo "🔍 检查虚拟环境..."
if [ -d "$VENV_DIR" ]; then
    echo "   ✅ 虚拟环境已存在: .venv/"
    ((pass_count++))
    
    # 激活虚拟环境检查
    if [ -f "$VENV_DIR/bin/activate" ]; then
        echo "   ✅ 虚拟环境可用"
    else
        echo "   ⚠️  虚拟环境损坏"
        echo "      运行: rm -rf .venv && python3 -m venv .venv"
    fi
else
    echo "   ⚠️  未找到虚拟环境"
    echo "      将在安装时自动创建"
fi
echo ""

# 3. 检查 PyQt6（在虚拟环境中）
echo "🔍 检查 PyQt6..."
if [ -d "$VENV_DIR" ]; then
    if "$VENV_DIR/bin/python" -c "import PyQt6; print(PyQt6.__version__)" 2>/dev/null; then
        pyqt_version=$("$VENV_DIR/bin/python" -c "import PyQt6; print(PyQt6.__version__)")
        echo "   ✅ PyQt6 $pyqt_version (虚拟环境)"
        ((pass_count++))
    else
        echo "   ⚠️  虚拟环境中未安装 PyQt6"
        echo "      运行: ./install.sh"
        ((fail_count++))
    fi
else
    echo "   ⚠️  请先创建虚拟环境"
    echo "      运行: ./install.sh"
    ((fail_count++))
fi
echo ""

# 4. 检查主程序文件
echo "🔍 检查程序文件..."
if [ -f "email_assistant_gui.py" ]; then
    size=$(ls -lh email_assistant_gui.py | awk '{print $5}')
    echo "   ✅ email_assistant_gui.py ($size)"
    ((pass_count++))
else
    echo "   ❌ 未找到主程序文件"
    ((fail_count++))
fi
echo ""

# 5. 检查启动脚本
echo "🔍 检查启动脚本..."
if [ -x "run.sh" ]; then
    echo "   ✅ run.sh (可执行)"
    ((pass_count++))
else
    if [ -f "run.sh" ]; then
        echo "   ⚠️  run.sh 存在但不可执行"
        echo "      运行: chmod +x run.sh"
    else
        echo "   ❌ 未找到 run.sh"
        ((fail_count++))
    fi
fi
echo ""

# 6. 检查打包脚本
echo "🔍 检查打包脚本..."
if [ -f "build_app.sh" ]; then
    if [ -x "build_app.sh" ]; then
        echo "   ✅ build_app.sh (可执行)"
    else
        echo "   ⚠️  build_app.sh 存在但不可执行"
        echo "      运行: chmod +x build_app.sh"
    fi
    ((pass_count++))
else
    echo "   ⚠️  未找到 build_app.sh"
fi
echo ""

# 7. 检查文档
echo "🔍 检查文档..."
doc_count=0
for doc in "开始使用.md" "README.md" "QUICKSTART.md" "USER_GUIDE.md" "INSTALL.md"; do
    if [ -f "$doc" ]; then
        ((doc_count++))
    fi
done
if [ $doc_count -ge 3 ]; then
    echo "   ✅ 找到 $doc_count 个文档文件"
    ((pass_count++))
else
    echo "   ⚠️  只找到 $doc_count 个文档文件"
fi
echo ""

# 总结
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📊 检查结果"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   ✅ 通过: $pass_count"
echo "   ⚠️  需要处理: $fail_count"
echo ""

if [ $fail_count -eq 0 ]; then
    echo "🎉 太棒了！所有检查都通过了！"
    echo ""
    echo "📝 下一步："
    echo "   1. 获取163邮箱授权码"
    echo "   2. 运行: ./run.sh"
    echo "   3. 开始使用！"
    echo ""
    exit 0
else
    echo "⚠️  发现 $fail_count 个问题"
    echo ""
    echo "💡 快速修复："
    if ! command -v python3 &> /dev/null; then
        echo "   • 安装 Python: brew install python3"
    fi
    if [ ! -d "$VENV_DIR" ] || ! "$VENV_DIR/bin/python" -c "import PyQt6" 2>/dev/null; then
        echo "   • 安装依赖: ./install.sh"
    fi
    if [ -f "run.sh" ] && [ ! -x "run.sh" ]; then
        echo "   • 修复权限: chmod +x *.sh"
    fi
    echo ""
    exit 1
fi
