#!/bin/bash

# 项目清理脚本
# 清理旧代码、构建产物、冗余文件

set -e  # 遇到错误立即退出

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║          🧹 Eason 项目清理脚本                             ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# 检查是否在正确的目录
if [ ! -f "main.py" ]; then
    echo "❌ 错误: 不在项目根目录"
    exit 1
fi

echo "📋 当前目录: $PROJECT_DIR"
echo ""

# 询问清理方式
echo "选择清理方式:"
echo "  1) 彻底清理 (删除旧代码，推荐)"
echo "  2) 保守清理 (归档旧代码)"
echo "  3) 仅清理构建产物"
echo "  4) 取消"
echo ""
read -p "请选择 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "🗑️  执行彻底清理..."
        echo ""
        
        # 1. 备份测试数据
        if [ -d "emailcode" ]; then
            echo "📦 备份测试数据到 tests/fixtures/"
            mkdir -p tests/fixtures
            cp emailcode/contacts*.txt tests/fixtures/ 2>/dev/null || true
            cp emailcode/contacts*.csv tests/fixtures/ 2>/dev/null || true
        fi
        
        # 2. 删除旧代码
        if [ -d "emailcode" ]; then
            echo "🗑️  删除 emailcode/ 目录"
            rm -rf emailcode/
        fi
        
        # 3. 删除旧主程序
        if [ -f "email_assistant_gui.py" ]; then
            echo "🗑️  删除 email_assistant_gui.py"
            rm -f email_assistant_gui.py
        fi
        
        # 4. 移动配置文件
        if [ -f "Eason.spec" ]; then
            echo "📦 移动 Eason.spec 到 scripts/build/"
            mkdir -p scripts/build
            mv Eason.spec scripts/build/
        fi
        
        # 5. 清理构建产物（保留目录）
        echo "🗑️  清理构建产物内容（保留目录结构）"
        rm -rf build/* dist/* release/* 2>/dev/null || true
        mkdir -p build dist release
        
        # 6. 清理Python缓存
        echo "🗑️  清理Python缓存"
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
        find . -type f -name "*.pyo" -delete 2>/dev/null || true
        
        echo ""
        echo "✅ 彻底清理完成！"
        ;;
        
    2)
        echo ""
        echo "🗂️  执行保守清理（归档）..."
        echo ""
        
        # 创建归档目录
        mkdir -p archive
        
        # 归档旧代码
        if [ -d "emailcode" ]; then
            echo "📦 归档 emailcode/ → archive/emailcode_v1/"
            mv emailcode archive/emailcode_v1
        fi
        
        # 归档旧主程序
        if [ -f "email_assistant_gui.py" ]; then
            echo "📦 归档 email_assistant_gui.py → archive/"
            mv email_assistant_gui.py archive/email_assistant_gui_v1.py
        fi
        
        # 清理构建产物（保留目录）
        echo "🗑️  清理构建产物内容（保留目录结构）"
        rm -rf build/* dist/* release/* 2>/dev/null || true
        mkdir -p build dist release
        
        # 创建 .gitkeep 文件
        for dir in build dist release; do
            echo "# 此文件确保目录被Git追踪" > "$dir/.gitkeep"
        done
        
        echo ""
        echo "✅ 保守清理完成！旧代码已归档到 archive/"
        ;;
        
    3)
        echo ""
        echo "🗑️  仅清理构建产物内容（保留目录）..."
        echo ""
        
        rm -rf build/* dist/* release/* 2>/dev/null || true
        mkdir -p build dist release
        
        # 创建 .gitkeep 文件
        for dir in build dist release; do
            echo "# 此文件确保目录被Git追踪" > "$dir/.gitkeep"
        done
        
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
        
        echo ""
        echo "✅ 构建产物清理完成！"
        ;;
        
    4)
        echo ""
        echo "❌ 取消清理"
        exit 0
        ;;
        
    *)
        echo ""
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 清理统计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 统计项目大小
echo "项目结构:"
ls -lh | grep ^d | awk '{print "  📁 " $9 ": " $5}'
echo ""

# 文件统计
echo "文件统计:"
echo "  Python文件: $(find . -name "*.py" -not -path "./.venv/*" | wc -l | tr -d ' ')"
echo "  文档文件: $(find docs -name "*.md" 2>/dev/null | wc -l | tr -d ' ')"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎯 下一步操作"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 查看清理结果:"
echo "   git status"
echo ""
echo "2. 提交清理:"
echo "   git add -A"
echo "   git commit -m '🧹 清理旧代码和构建产物'"
echo "   git push"
echo ""
echo "3. 开始添加新功能:"
echo "   查看 docs/项目清理与功能规划.md"
echo ""
