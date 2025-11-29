# 📧 Eason - 邮件批量发送助手

<div align="center">
  <img src="./picture/cover/Gemini_Generated_Image_qifrgrqifrgrqifr.png" alt="Eason Cover" width="800"/>
</div>

一个精美的 macOS 邮件批量发送工具,支持联系人采集和批量邮件发送。

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey)

## ✨ 功能特点

### 📥 联系人采集
- 🔍 自动从 163 邮箱收件箱采集发件人邮箱
- 🧹 智能去重，保持联系人唯一性
- 💾 支持导出为 TXT 或 CSV 格式
- ⏸️ 可随时停止采集任务

### 📤 批量发送
- 📨 批量发送个性化邮件
- 📎 支持添加图片/PDF 附件
- ⚡️ 批次发送机制，避免被封禁
- 📊 实时进度显示和日志反馈
- 💾 自动保存配置，下次使用更便捷

### 🎨 界面设计
- 🍎 原生 macOS 风格界面
- 🌈 精美的深色主题日志窗口
- 📱 直观的选项卡式布局
- ⚡️ 多线程处理，界面永不卡顿

## 📁 项目结构

```
Eason/
├── email_assistant_gui.py    # 主程序
├── scripts/                  # 所有脚本
├── docs/                     # 所有文档
├── config/                   # 配置文件
└── emailcode/                # 原始命令行版本
```

> 💡 详细结构说明见 [PROJECT_LAYOUT.md](PROJECT_LAYOUT.md)

## 📋 系统要求

- macOS 10.14 或更高版本
- Python 3.8 或更高版本
- 163 邮箱账号及授权码

## 🚀 快速开始

### 1️⃣ 一键安装（推荐）

```bash
cd /Users/code/Eason
./install.sh
```

这将自动：
- 创建虚拟环境（.venv/）
- 安装所有依赖（PyQt6等）
- 配置运行环境

### 2️⃣ 运行程序

```bash
./run.sh
```

或手动激活虚拟环境：

```bash
source .venv/bin/activate
python email_assistant_gui.py
```

### 3️⃣ 获取 163 邮箱授权码

1. 登录 [163 邮箱](https://mail.163.com)
2. 点击「设置」→「POP3/SMTP/IMAP」
3. 开启「IMAP/SMTP服务」
4. 按提示获取授权码（非登录密码）
5. 将授权码填入软件的「授权码」输入框

## 📖 使用指南

### 采集联系人

1. 在「账号配置」区域填写邮箱和授权码
2. 切换到「📥 采集联系人」标签页
3. 设置采集数量（默认 200 封）
4. 点击「🚀 开始采集」按钮
5. 等待采集完成，查看结果
6. 点击「💾 导出联系人」保存到文件

### 批量发送邮件

1. 确保已填写账号配置
2. 切换到「📤 批量发送」标签页
3. 选择联系人列表文件（.txt 或 .csv）
4. 填写邮件主题和正文
5. （可选）添加图片或 PDF 附件
6. 设置发送策略：
   - **批次大小**: 每批发送多少封（建议 10 封）
   - **间隔时间**: 批次之间等待秒数（建议 20-60 秒）
7. 点击「🚀 开始发送」
8. 在日志窗口查看实时进度

### ⚠️ 注意事项

- **授权码非密码**: 必须使用邮箱的授权码，不是登录密码
- **批次发送**: 建议每批 10 封，间隔 20 秒以上，避免被识别为垃圾邮件
- **联系人格式**: 每行一个邮箱地址，或使用 CSV 文件
- **附件大小**: 建议单个附件不超过 10MB

## 🎁 打包为独立应用

### 方法一：使用 PyInstaller

```bash
# 1. 安装 PyInstaller
pip3 install pyinstaller

# 2. 打包应用
pyinstaller --noconsole \
            --onefile \
            --name="邮件助手" \
            --icon=icon.icns \
            email_assistant_gui.py

# 3. 查看生成的应用
open dist/
```

生成的 `.app` 文件可以双击运行，无需安装 Python。

### 方法二：使用 py2app

```bash
# 1. 安装 py2app
pip3 install py2app

# 2. 创建 setup.py
cat > setup.py << 'EOF'
from setuptools import setup

APP = ['email_assistant_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PyQt6'],
    'iconfile': 'icon.icns',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
EOF

# 3. 打包
python3 setup.py py2app

# 4. 查看应用
open dist/
```

### 制作应用图标（可选）

如果有 PNG 图片，可以转换为 macOS 图标：

```bash
mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset
```

## 🔧 高级配置

### 配置文件位置

软件会自动保存配置到：
```
~/Library/Preferences/com.EmailAssistant.BatchSender.plist
```

### 支持的邮箱服务商

当前版本仅支持 **163 邮箱**。如需支持其他邮箱，需修改代码中的 SMTP/IMAP 服务器地址：

- **QQ 邮箱**: `smtp.qq.com` / `imap.qq.com`
- **Gmail**: `smtp.gmail.com` / `imap.gmail.com`
- **Outlook**: `smtp-mail.outlook.com` / `outlook.office365.com`

## 🐛 常见问题

### Q: 提示"登录失败"？
**A**: 请确认：
1. 使用的是授权码，不是登录密码
2. 已开启 IMAP/SMTP 服务
3. 网络连接正常

### Q: 邮件发送失败？
**A**: 可能原因：
1. 授权码错误
2. 收件人邮箱地址格式错误
3. 附件过大
4. 发送频率过高被限制

### Q: 如何避免被识别为垃圾邮件？
**A**: 建议：
1. 使用小批次发送（10 封/批）
2. 增加批次间隔时间（≥30 秒）
3. 邮件内容避免敏感词汇
4. 不要频繁使用同一账号大量发送

### Q: 可以同时运行多个发送任务吗？
**A**: 不建议。同一邮箱账号同时发送可能被服务器拒绝。

## 📝 更新日志

### v1.0 (2024-11)
- ✨ 首次发布
- 📥 支持联系人采集
- 📤 支持批量发送
- 🎨 精美的 macOS 原生界面
- 💾 自动保存配置

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 作者

开发者：Your Name

---

<div align="center">
  <img src="./picture/cover/Gemini_Generated_Image_d15x2id15x2id15x.png" alt="Eason" width="800"/>
</div>

---

**⭐️ 如果这个项目对你有帮助，请给个 Star！**
