#!/bin/bash

# Eason 图标生成脚本
# 从 PNG 素材生成 macOS .icns 图标

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🎨 Eason 图标生成工具"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

ICON_SOURCE="picture/AppIcons/Assets.xcassets/AppIcon.appiconset"

# 检查源文件
if [ ! -d "$ICON_SOURCE" ]; then
    echo "❌ 错误: 找不到图标源文件"
    echo "   期望位置: $ICON_SOURCE"
    exit 1
fi

echo "📂 图标源文件: $ICON_SOURCE"
echo ""

# 创建临时 iconset 目录
ICONSET_DIR="/tmp/Eason.iconset"
rm -rf "$ICONSET_DIR"
mkdir -p "$ICONSET_DIR"

echo "📋 复制图标文件..."

# macOS 需要的标准尺寸
declare -A ICON_SIZES=(
    ["icon_16x16.png"]="16.png"
    ["icon_16x16@2x.png"]="32.png"
    ["icon_32x32.png"]="32.png"
    ["icon_32x32@2x.png"]="64.png"
    ["icon_128x128.png"]="128.png"
    ["icon_128x128@2x.png"]="256.png"
    ["icon_256x256.png"]="256.png"
    ["icon_256x256@2x.png"]="512.png"
    ["icon_512x512.png"]="512.png"
    ["icon_512x512@2x.png"]="1024.png"
)

MISSING_FILES=0

for output_name in "${!ICON_SIZES[@]}"; do
    source_file="${ICON_SIZES[$output_name]}"
    source_path="$ICON_SOURCE/$source_file"
    
    if [ -f "$source_path" ]; then
        cp "$source_path" "$ICONSET_DIR/$output_name"
        echo "   ✓ $output_name"
    else
        echo "   ⚠ $source_file 不存在"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

echo ""

if [ $MISSING_FILES -gt 0 ]; then
    echo "⚠️  警告: 有 $MISSING_FILES 个尺寸的图标文件缺失"
    echo "   但仍会尝试生成 .icns 文件"
    echo ""
fi

# 生成 icns 文件
echo "🔨 生成 macOS 图标文件..."

if iconutil -c icns "$ICONSET_DIR" -o "Eason.icns"; then
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ✅ 图标生成成功！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📦 图标信息:"
    echo "   文件名: Eason.icns"
    ICON_SIZE=$(du -sh "Eason.icns" | awk '{print $1}')
    echo "   大小: $ICON_SIZE"
    echo "   路径: $PROJECT_DIR/Eason.icns"
    echo ""
    echo "🎯 下一步:"
    echo "   重新打包应用以应用新图标:"
    echo "   ./scripts/build_app.sh"
    echo ""
else
    echo ""
    echo "❌ 图标生成失败"
    exit 1
fi

# 清理临时文件
rm -rf "$ICONSET_DIR"

echo "✨ 完成！"
echo ""
