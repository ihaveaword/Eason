# 📁 项目结构说明

## 目录结构

```
Eason/
├── email_assistant_gui.py    # 🎨 主程序（GUI界面）
├── README.md                  # 📖 使用说明文档
├── INSTALL.md                 # 📦 安装指南
├── requirements.txt           # 📋 依赖包列表
├── run.sh                     # 🚀 快速启动脚本
├── build_app.sh              # 🔨 打包脚本
└── emailcode/                 # 📂 原始命令行版本
    ├── main.py               # 发送邮件脚本
    ├── fetch_contacts.py     # 采集联系人脚本
    ├── contact.py            # 联系人处理脚本
    ├── contacts.txt          # 联系人列表示例
    └── contacts.csv          # 联系人列表示例（CSV）
```

## 核心文件说明

### 1. email_assistant_gui.py

**主 GUI 应用程序**，包含以下模块：

#### 类结构

- `FetchContactsThread`: 后台采集联系人的工作线程
  - 连接 IMAP 服务器
  - 遍历邮箱获取发件人地址
  - 去重并返回结果

- `SendEmailThread`: 后台发送邮件的工作线程
  - 连接 SMTP 服务器
  - 批次发送邮件
  - 处理附件
  - 错误处理和重试

- `EmailAssistantApp`: 主窗口类
  - UI 布局和组件
  - 事件处理
  - 配置管理
  - 日志显示

#### 核心功能

```python
# 采集联系人
def start_fetch()           # 启动采集任务
def on_fetch_finished()     # 采集完成处理
def save_fetched_contacts() # 导出联系人

# 发送邮件
def start_send()            # 启动发送任务
def on_send_finished()      # 发送完成处理
def update_progress()       # 更新进度条

# 配置管理
def load_config()           # 加载配置
def save_config()           # 保存配置
```

### 2. 脚本文件

#### run.sh - 快速启动

```bash
#!/bin/bash
# 检查依赖
# 启动 GUI 程序
python3 email_assistant_gui.py
```

#### build_app.sh - 打包应用

```bash
#!/bin/bash
# 使用 PyInstaller 打包为 .app
# 生成独立可执行程序
pyinstaller --noconsole --onefile --name="邮件助手" email_assistant_gui.py
```

### 3. 配置文件

#### requirements.txt

```
PyQt6>=6.4.0      # GUI 框架
pyinstaller>=5.0.0 # 打包工具
```

## 原始代码说明

### emailcode/ 目录

这是项目的原始命令行版本，包含：

1. **main.py** - 批量发送邮件
   - 使用 `smtplib` 连接 SMTP
   - 批次发送机制
   - 附件支持

2. **fetch_contacts.py** - 采集联系人
   - 使用 `imaplib` 连接 IMAP
   - 提取发件人地址
   - 返回联系人列表

3. **contact.py** - 联系人处理
   - 调用 `fetch_contacts.py`
   - 去重处理
   - 导出为 TXT/CSV

## 数据流程

### 采集流程

```
用户输入（邮箱、授权码、数量）
    ↓
FetchContactsThread 启动
    ↓
连接 IMAP 服务器
    ↓
遍历邮箱获取发件人
    ↓
去重处理
    ↓
返回结果并显示
    ↓
导出为文件（可选）
```

### 发送流程

```
用户输入（主题、正文、附件、联系人）
    ↓
SendEmailThread 启动
    ↓
解析联系人文件
    ↓
分批次处理
    ↓
对每个批次：
  - 连接 SMTP
  - 发送邮件
  - 记录结果
  - 等待间隔
    ↓
完成并显示统计
```

## UI 布局结构

```
EmailAssistantApp (主窗口)
├── 账号配置区 (QGroupBox)
│   ├── 邮箱输入框 (QLineEdit)
│   └── 授权码输入框 (QLineEdit)
│
├── 功能选项卡 (QTabWidget)
│   ├── Tab 1: 采集联系人
│   │   ├── 控制区
│   │   │   ├── 数量选择 (QSpinBox)
│   │   │   ├── 开始按钮 (QPushButton)
│   │   │   ├── 停止按钮 (QPushButton)
│   │   │   └── 导出按钮 (QPushButton)
│   │   └── 结果预览 (QTextEdit)
│   │
│   └── Tab 2: 批量发送
│       ├── 表单区 (QFormLayout)
│       │   ├── 联系人文件选择
│       │   ├── 邮件主题
│       │   ├── 邮件正文
│       │   ├── 附件选择
│       │   └── 批次设置
│       └── 控制按钮
│           ├── 开始发送 (QPushButton)
│           └── 停止发送 (QPushButton)
│
└── 运行状态区 (QGroupBox)
    ├── 进度条 (QProgressBar)
    └── 日志窗口 (QTextEdit)
```

## 配置存储

应用配置使用 `QSettings` 自动保存在：

```
~/Library/Preferences/com.EmailAssistant.BatchSender.plist
```

保存的配置项：
- `email`: 邮箱账号
- `pwd`: 授权码（加密存储）
- `last_contact_file`: 上次使用的联系人文件
- `last_subject`: 上次的邮件主题
- `last_body`: 上次的邮件正文
- `last_attachment`: 上次的附件路径

## 扩展建议

### 添加新功能

1. **支持更多邮箱服务商**
   - 修改 `IMAP/SMTP` 服务器配置
   - 添加服务商选择下拉框

2. **邮件模板功能**
   - 保存常用模板
   - 变量替换（如 {姓名}）

3. **定时发送**
   - 使用 `QTimer` 实现
   - 添加时间选择器

4. **发送历史**
   - 使用 SQLite 存储
   - 查看历史记录界面

### 代码优化

1. **配置文件**
   - 将 SMTP/IMAP 配置抽离到配置文件
   - 支持自定义服务器

2. **错误处理**
   - 更详细的错误提示
   - 自动重试机制

3. **性能优化**
   - 连接池复用
   - 异步 IO

## 打包后的应用结构

```
邮件助手.app/
├── Contents/
│   ├── MacOS/
│   │   └── 邮件助手          # 可执行文件
│   ├── Resources/
│   │   ├── icon.icns         # 应用图标
│   │   └── ...               # 其他资源
│   └── Info.plist            # 应用信息
```

## 依赖说明

### PyQt6

- **用途**: GUI 框架
- **版本**: ≥ 6.4.0
- **模块**:
  - `QtWidgets`: UI 组件
  - `QtCore`: 核心功能（线程、信号）
  - `QtGui`: 图形功能（字体、图标）

### Python 标准库

- `smtplib`: SMTP 客户端
- `imaplib`: IMAP 客户端
- `email`: 邮件消息处理
- `csv`: CSV 文件处理
- `json`: JSON 处理
- `re`: 正则表达式

## 安全注意事项

1. **授权码存储**: 使用 `QSettings` 加密存储
2. **敏感信息**: 不记录到日志
3. **文件权限**: 配置文件仅用户可读
4. **网络安全**: 使用 SSL/TLS 连接

## 版本历史

### v1.0 (当前版本)
- ✅ 基础 GUI 界面
- ✅ 联系人采集
- ✅ 批量发送
- ✅ 配置自动保存
- ✅ 实时日志显示
- ✅ 进度跟踪
- ✅ 多线程处理

### 计划功能
- 🔜 支持更多邮箱
- 🔜 邮件模板
- 🔜 定时发送
- 🔜 发送历史
