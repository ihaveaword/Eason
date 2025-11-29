# 🐍 虚拟环境使用指南

## 什么是虚拟环境？

虚拟环境（Virtual Environment）是 Python 的独立运行环境，可以：

- ✅ **隔离依赖**: 项目依赖安装在 `.venv/` 目录，不影响系统 Python
- ✅ **版本管理**: 每个项目可以使用不同版本的库
- ✅ **清理方便**: 删除 `.venv/` 目录即可完全清理
- ✅ **便于分享**: 通过 `requirements.txt` 轻松复制环境

## 📁 项目结构

```
Eason/
├── .venv/                    # 虚拟环境目录（自动创建）
│   ├── bin/                  # 可执行文件
│   │   ├── python           # 虚拟环境的 Python
│   │   ├── pip              # 虚拟环境的 pip
│   │   └── activate         # 激活脚本
│   └── lib/                  # 安装的库
├── email_assistant_gui.py    # 主程序
├── install.sh               # 一键安装脚本
├── run.sh                   # 启动脚本
└── requirements.txt         # 依赖清单
```

## 🚀 快速开始

### 方法 1: 使用自动化脚本（推荐）

```bash
# 一键安装
./install.sh

# 运行程序
./run.sh
```

### 方法 2: 手动管理虚拟环境

#### 创建虚拟环境

```bash
python3 -m venv .venv
```

#### 激活虚拟环境

```bash
# macOS/Linux
source .venv/bin/activate

# 激活后，提示符会显示 (.venv)
(.venv) user@mac Eason $
```

#### 安装依赖

```bash
# 在激活的虚拟环境中
pip install -r requirements.txt
```

#### 运行程序

```bash
# 在激活的虚拟环境中
python email_assistant_gui.py
```

#### 退出虚拟环境

```bash
deactivate
```

## 📋 常用命令

### 检查虚拟环境状态

```bash
# 检查是否在虚拟环境中
which python
# 输出: /Users/code/Eason/.venv/bin/python (在虚拟环境中)
# 输出: /usr/bin/python3 (系统 Python)

# 查看已安装的包
pip list

# 查看 Python 版本
python --version
```

### 管理依赖

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装新包
pip install package_name

# 卸载包
pip uninstall package_name

# 更新包
pip install --upgrade package_name

# 导出依赖列表
pip freeze > requirements.txt

# 安装依赖列表
pip install -r requirements.txt
```

### 重建虚拟环境

```bash
# 删除旧环境
rm -rf .venv

# 重新安装
./install.sh
```

## 🔧 脚本说明

### install.sh - 一键安装

自动完成环境配置：

```bash
./install.sh
```

功能：
- ✅ 检查 Python 版本
- ✅ 创建虚拟环境
- ✅ 升级 pip
- ✅ 安装所有依赖
- ✅ 验证安装
- ✅ 设置脚本权限
- ✅ 创建 .gitignore

### run.sh - 快速启动

自动激活虚拟环境并运行：

```bash
./run.sh
```

功能：
- ✅ 检查虚拟环境是否存在
- ✅ 检查依赖是否安装
- ✅ 自动调用 install.sh（如需要）
- ✅ 启动应用程序

### check_install.sh - 环境检查

检查安装状态：

```bash
./check_install.sh
```

检查项：
- ✅ Python 版本
- ✅ 虚拟环境状态
- ✅ PyQt6 安装
- ✅ 程序文件完整性

### build_app.sh - 打包应用

打包为独立 .app 文件：

```bash
./build_app.sh
```

功能：
- ✅ 检查虚拟环境
- ✅ 安装 PyInstaller
- ✅ 打包为 macOS 应用
- ✅ 生成 dist/邮件助手.app

## ⚠️ 常见问题

### Q1: 虚拟环境在哪里？

**A**: 在项目根目录的 `.venv/` 文件夹中。这是一个隐藏目录（以 `.` 开头）。

查看：
```bash
ls -la | grep venv
```

### Q2: 为什么不能直接运行 Python 程序？

**A**: 如果直接运行 `python3 email_assistant_gui.py`，会使用系统 Python，可能找不到依赖。

解决方法：
1. 使用 `./run.sh`（推荐）
2. 激活虚拟环境后再运行

### Q3: 虚拟环境占用多少空间？

**A**: 大约 50-100MB，主要是 PyQt6 库。

查看大小：
```bash
du -sh .venv
```

### Q4: 可以删除虚拟环境吗？

**A**: 可以！虚拟环境随时可以重建：

```bash
rm -rf .venv
./install.sh
```

### Q5: .gitignore 包含虚拟环境吗？

**A**: 是的！`install.sh` 会自动创建 `.gitignore`，排除：
- `.venv/` - 虚拟环境
- `__pycache__/` - Python 缓存
- `build/`, `dist/` - 打包文件
- `.DS_Store` - macOS 文件

### Q6: 多个项目可以共享虚拟环境吗？

**A**: 不建议。每个项目应该有独立的虚拟环境。

### Q7: 如何在 IDE 中使用虚拟环境？

**VSCode**:
1. 打开项目
2. 按 `Cmd+Shift+P`
3. 选择 "Python: Select Interpreter"
4. 选择 `.venv/bin/python`

**PyCharm**:
1. Settings → Project → Python Interpreter
2. 添加新解释器
3. 选择 `.venv/bin/python`

## 📊 性能对比

| 方式 | 优点 | 缺点 |
|------|------|------|
| 系统 Python | 简单 | 依赖冲突、难以管理 |
| 虚拟环境 | 隔离、清晰、专业 | 额外空间、需要激活 |

## 🎓 最佳实践

1. ✅ **始终使用虚拟环境** - 即使是小项目
2. ✅ **不要提交虚拟环境到 Git** - 使用 .gitignore
3. ✅ **定期更新依赖** - `pip install --upgrade package`
4. ✅ **使用 requirements.txt** - 方便环境复制
5. ✅ **命名统一** - 使用 `.venv` 或 `venv`

## 🔗 相关资源

- [Python 虚拟环境官方文档](https://docs.python.org/3/library/venv.html)
- [pip 用户指南](https://pip.pypa.io/en/stable/user_guide/)
- [项目最佳实践](https://docs.python-guide.org/writing/structure/)

---

**💡 提示**: 使用虚拟环境是 Python 开发的标准做法，本项目已完全配置好，你只需运行 `./install.sh` 即可！
