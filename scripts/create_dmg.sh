#!/bin/bash

# Eason DMG 创建脚本
# 用于创建专业的 macOS 安装包

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📀 Eason DMG 创建工具"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查 Eason.app 是否存在
if [ ! -d "dist/Eason.app" ]; then
    echo "❌ 错误: 未找到 dist/Eason.app"
    echo "   请先运行: ./scripts/build_app.sh"
    exit 1
fi

# 检查 create-dmg 是否安装
if ! command -v create-dmg &> /dev/null; then
    echo "⚠️  未找到 create-dmg，正在安装..."
    brew install create-dmg
    echo "✅ create-dmg 安装完成"
    echo ""
fi

# 获取版本号
VERSION="1.0.0"
if [ ! -z "$1" ]; then
    VERSION="$1"
fi

DMG_NAME="Eason-v${VERSION}.dmg"
RELEASE_DIR="release/v${VERSION}"

# 创建 release 目录
mkdir -p "${RELEASE_DIR}"

echo "📦 创建信息:"
echo "   应用: dist/Eason.app"
echo "   版本: v${VERSION}"
echo "   输出: ${RELEASE_DIR}/${DMG_NAME}"
echo ""

# 删除旧的 DMG（如果存在）
if [ -f "${RELEASE_DIR}/${DMG_NAME}" ]; then
    echo "🧹 删除旧的 DMG 文件..."
    rm -f "${RELEASE_DIR}/${DMG_NAME}"
fi

# 临时 DMG 文件名
TEMP_DMG="${DMG_NAME}"

echo "🔨 正在创建 DMG..."
echo "   这可能需要 1-2 分钟..."
echo ""

# 创建 DMG
create-dmg \
  --volname "Eason" \
  --volicon "dist/Eason.app/Contents/Resources/icon-windowed.icns" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "Eason.app" 175 190 \
  --hide-extension "Eason.app" \
  --app-drop-link 425 190 \
  --no-internet-enable \
  "${DMG_NAME}" \
  "dist/Eason.app" > /dev/null 2>&1

# 移动 DMG 到 release 目录
if [ -f "${TEMP_DMG}" ]; then
    mv "${TEMP_DMG}" "${RELEASE_DIR}/"
    
    # 创建校验和
    cd "${RELEASE_DIR}"
    shasum -a 256 "${DMG_NAME}" > checksums.txt
    cd "$PROJECT_DIR"
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  ✅ DMG 创建成功！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📦 DMG 信息:"
    echo "   文件名: ${DMG_NAME}"
    DMG_SIZE=$(du -sh "${RELEASE_DIR}/${DMG_NAME}" | awk '{print $1}')
    echo "   大小: ${DMG_SIZE}"
    echo "   位置: ${RELEASE_DIR}/"
    echo "   路径: $PROJECT_DIR/${RELEASE_DIR}/${DMG_NAME}"
    echo ""
    echo "🔐 校验和:"
    cat "${RELEASE_DIR}/checksums.txt"
    echo ""
    echo "🎯 使用方法:"
    echo "   测试: open ${RELEASE_DIR}/${DMG_NAME}"
    echo ""
    echo "📤 分发方式:"
    echo "   1. 上传 ${RELEASE_DIR}/${DMG_NAME} 到 GitHub Release"
    echo "   2. 同时上传 checksums.txt 供用户验证"
    echo ""
    
    # 询问是否打开测试
    read -p "是否立即打开 DMG 测试？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "正在打开 ${RELEASE_DIR}/${DMG_NAME}..."
        open "${RELEASE_DIR}/${DMG_NAME}"
    fi
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🎉 完成！"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
else
    echo ""
    echo "❌ DMG 创建失败"
    exit 1
fi
