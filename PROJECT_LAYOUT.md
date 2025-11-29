# 📁 项目目录结构

## 整理后的清晰结构

```
Eason/
│
├── 📱 email_assistant_gui.py    # 主程序（GUI应用）
├── 📋 requirements.txt           # Python 依赖清单
├── 📖 README.md                  # 项目介绍（必读）
│
├── 🔗 install.sh                 # 快捷链接 → scripts/install.sh
├── 🔗 run.sh                     # 快捷链接 → scripts/run.sh
├── 🔗 fix_install.sh             # 快捷链接 → scripts/fix_install.sh
├── 🔗 check_install.sh           # 快捷链接 → scripts/check_install.sh
│
├── 📂 scripts/                   # 所有脚本文件
│   ├── install.sh               # 🔧 安装脚本（创建虚拟环境）
│   ├── run.sh                   # 🚀 运行脚本
│   ├── fix_install.sh           # 🔨 修复安装问题
│   ├── check_install.sh         # ✅ 检查安装状态
│   ├── build_app.sh             # 📦 打包为 .app
│   └── activate.sh              # ℹ️  虚拟环境说明
│
├── 📂 config/                    # 配置文件
│   └── pip.conf                 # pip 镜像源配置
│
├── 📂 docs/                      # 所有文档
│   ├── 开始使用.md              # ⭐️ 中文快速指南
│   ├── QUICKSTART.md            # 5分钟快速开始
│   ├── INSTALL.md               # 详细安装指南
│   ├── USER_GUIDE.md            # 完整使用手册
│   ├── VENV_GUIDE.md            # 虚拟环境指南
│   ├── PROJECT_STRUCTURE.md     # 代码结构说明
│   ├── PROJECT_SUMMARY.md       # 项目技术总览
│   ├── 镜像源配置说明.md        # pip 镜像源配置
│   ├── 安装速度优化说明.txt     # 安装优化说明
│   ├── 虚拟环境说明.txt         # 虚拟环境说明
│   └── 🎉 项目完成.txt          # 项目完成报告
│
├── 📂 emailcode/                 # 原始命令行版本
│   ├── main.py                  # 命令行发送脚本
│   ├── fetch_contacts.py        # 命令行采集脚本
│   ├── contact.py               # 联系人处理
│   └── contacts.txt             # 示例联系人列表
│
└── 📂 .venv/                     # 虚拟环境（自动创建）
    ├── bin/                     # Python、pip 等可执行文件
    └── lib/                     # 安装的包（PyQt6 等）
```

## 📍 快速导航

### 🚀 日常使用

| 操作 | 命令 |
|------|------|
| 安装 | `./install.sh` |
| 运行 | `./run.sh` |
| 检查 | `./check_install.sh` |
| 修复 | `./fix_install.sh` |

> 💡 根目录的 `.sh` 文件都是符号链接，指向 `scripts/` 目录

### 📖 文档查看

| 文档 | 位置 | 说明 |
|------|------|------|
| 项目介绍 | `README.md` | 项目总览 |
| 快速开始 | `docs/开始使用.md` | 中文快速指南 ⭐️ |
| 快速开始 | `docs/QUICKSTART.md` | 5分钟上手 |
| 安装指南 | `docs/INSTALL.md` | 详细安装步骤 |
| 使用手册 | `docs/USER_GUIDE.md` | 完整功能说明 |
| 虚拟环境 | `docs/VENV_GUIDE.md` | 虚拟环境详解 |
| 镜像源 | `docs/镜像源配置说明.md` | 加速下载 |

### ⚙️ 配置文件

| 文件 | 位置 | 用途 |
|------|------|------|
| pip.conf | `config/pip.conf` | pip 镜像源配置 |
| requirements.txt | `requirements.txt` | Python 依赖 |

### 🔧 脚本详解

| 脚本 | 位置 | 功能 |
|------|------|------|
| install.sh | `scripts/install.sh` | 创建虚拟环境并安装依赖 |
| run.sh | `scripts/run.sh` | 运行 GUI 应用 |
| fix_install.sh | `scripts/fix_install.sh` | 清理重装（解决问题）|
| check_install.sh | `scripts/check_install.sh` | 检查环境状态 |
| build_app.sh | `scripts/build_app.sh` | 打包为 macOS 应用 |
| activate.sh | `scripts/activate.sh` | 虚拟环境使用说明 |

## 🎯 目录说明

### 根目录
- ✅ 只保留最核心的文件
- ✅ 创建符号链接方便访问
- ✅ README.md 作为项目入口

### scripts/ 目录
- 所有可执行脚本
- 统一管理，便于维护
- 保持根目录整洁

### docs/ 目录
- 所有文档集中存放
- 按用途分类
- 便于查找和管理

### config/ 目录
- 配置文件统一存放
- 便于修改和备份
- 清晰的配置管理

### emailcode/ 目录
- 保留原始命令行版本
- 作为参考和备份
- 不影响新版本

## 💡 使用建议

### 新用户
1. 阅读 `README.md`
2. 查看 `docs/开始使用.md`
3. 运行 `./install.sh`
4. 运行 `./run.sh`

### 开发者
1. 查看 `docs/PROJECT_STRUCTURE.md`
2. 查看 `docs/PROJECT_SUMMARY.md`
3. 了解 `docs/VENV_GUIDE.md`

### 遇到问题
1. 运行 `./fix_install.sh`
2. 查看 `docs/INSTALL.md`
3. 查看 `docs/镜像源配置说明.md`

## 🔄 符号链接说明

根目录的以下文件是符号链接：
- `install.sh` → `scripts/install.sh`
- `run.sh` → `scripts/run.sh`
- `fix_install.sh` → `scripts/fix_install.sh`
- `check_install.sh` → `scripts/check_install.sh`

**优点**：
- ✅ 根目录保持整洁
- ✅ 保持向后兼容（原有命令不变）
- ✅ 实际文件统一管理

**注意**：
- 符号链接在文件管理器中显示为快捷方式
- 删除符号链接不会删除原文件
- Git 可以正常跟踪符号链接

## 📊 文件统计

| 类型 | 数量 | 说明 |
|------|------|------|
| Python 源码 | 1 | email_assistant_gui.py |
| 脚本文件 | 6 | scripts/*.sh |
| 配置文件 | 2 | pip.conf, requirements.txt |
| 文档文件 | 11 | docs/*.md, docs/*.txt |
| 原始代码 | 3 | emailcode/*.py |

## 🎨 目录设计原则

1. **清晰性** - 一眼就能找到需要的文件
2. **层次性** - 按功能分层组织
3. **易用性** - 常用命令在根目录直接访问
4. **可维护性** - 便于添加新文件
5. **兼容性** - 保持原有命令不变

## 🔗 相关文档

- [项目结构说明](docs/PROJECT_STRUCTURE.md) - 代码结构
- [项目总览](docs/PROJECT_SUMMARY.md) - 技术总览
- [虚拟环境指南](docs/VENV_GUIDE.md) - 虚拟环境详解

---

**💡 提示**：所有操作都可以在根目录直接执行，无需进入子目录！
