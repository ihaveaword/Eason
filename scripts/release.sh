#!/bin/bash

# Eason 版本发布脚本
# 自动化整个发布流程

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🚀 Eason 版本发布工具"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查版本号参数
if [ -z "$1" ]; then
    echo "❌ 错误: 请提供版本号"
    echo ""
    echo "用法: $0 <版本号>"
    echo ""
    echo "示例:"
    echo "  $0 1.0.0    # 发布 v1.0.0"
    echo "  $0 1.0.1    # 发布 v1.0.1"
    echo ""
    exit 1
fi

VERSION="$1"
RELEASE_DIR="release/v${VERSION}"

echo "📋 发布计划:"
echo "   版本: v${VERSION}"
echo "   输出目录: ${RELEASE_DIR}/"
echo ""

# 确认
read -p "确认开始发布流程？(y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "已取消"
    exit 0
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  步骤 1/4: 清理旧文件"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 清理构建文件
rm -rf build/ dist/ *.spec
echo "✅ 构建文件已清理"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  步骤 2/4: 打包应用"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

./scripts/build_app.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  步骤 3/4: 创建 DMG"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

./scripts/create_dmg.sh "${VERSION}"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  步骤 4/4: 生成发布信息"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 创建 release notes
cat > "${RELEASE_DIR}/RELEASE_NOTES.md" << EOF
# 🎉 Eason v${VERSION}

发布日期: $(date +%Y-%m-%d)

## 📦 下载

- [Eason-v${VERSION}.dmg](https://github.com/你的用户名/Eason/releases/download/v${VERSION}/Eason-v${VERSION}.dmg)

## 📊 文件信息

EOF

# 添加文件信息
cd "${RELEASE_DIR}"
echo "| 文件 | 大小 | SHA256 |" >> RELEASE_NOTES.md
echo "|------|------|--------|" >> RELEASE_NOTES.md
DMG_SIZE=$(du -sh "Eason-v${VERSION}.dmg" | awk '{print $1}')
DMG_SHA=$(cat checksums.txt | awk '{print $1}')
echo "| Eason-v${VERSION}.dmg | ${DMG_SIZE} | \`${DMG_SHA}\` |" >> RELEASE_NOTES.md
cd "$PROJECT_DIR"

cat >> "${RELEASE_DIR}/RELEASE_NOTES.md" << 'EOF'

## 💻 系统要求

- macOS 10.14 或更高版本
- 163 邮箱账号及授权码

## 🚀 安装方法

1. 下载 DMG 文件
2. 双击打开
3. 拖动 Eason 到 Applications 文件夹
4. 从 Launchpad 启动

## ⚠️ 首次运行

如遇到"无法打开"的提示：
1. 右键点击 Eason
2. 选择"打开"
3. 在弹出框中再次点击"打开"

## ✨ 功能特点

- 📬 自动采集联系人
- 📨 批量邮件发送
- ⚙️ 智能批次控制
- 📊 实时进度显示
- 💾 配置自动保存
- 🎨 精美 macOS 界面

## 🐛 问题反馈

遇到问题？请在 [Issues](https://github.com/你的用户名/Eason/issues) 中反馈。
EOF

echo "✅ 发布信息已生成: ${RELEASE_DIR}/RELEASE_NOTES.md"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ✅ 发布准备完成！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 发布文件:"
ls -lh "${RELEASE_DIR}/"
echo ""
echo "📝 发布清单:"
echo "   ✅ 应用已打包"
echo "   ✅ DMG 已创建"
echo "   ✅ 校验和已生成"
echo "   ✅ Release Notes 已生成"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  📤 下一步: 上传到 GitHub Release"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 访问: https://github.com/你的用户名/Eason/releases/new"
echo ""
echo "2. 填写信息:"
echo "   Tag: v${VERSION}"
echo "   Title: 🎉 Eason v${VERSION}"
echo ""
echo "3. 复制 Release Notes:"
echo "   cat ${RELEASE_DIR}/RELEASE_NOTES.md"
echo ""
echo "4. 上传文件:"
echo "   - ${RELEASE_DIR}/Eason-v${VERSION}.dmg"
echo "   - ${RELEASE_DIR}/checksums.txt"
echo ""
echo "5. 点击 Publish release"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 询问是否查看 Release Notes
read -p "是否查看 Release Notes？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    cat "${RELEASE_DIR}/RELEASE_NOTES.md"
fi

echo ""
echo "🎉 完成！"
