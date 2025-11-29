# 📦 安装指南

## 快速安装（推荐）

### 方法一：一键自动安装（推荐 ⭐️）

```bash
cd /Users/code/Eason
./install.sh
```

这个脚本会自动：
- ✅ 检查 Python 环境
- ✅ 创建虚拟环境（.venv/）
- ✅ 安装所有依赖
- ✅ 设置脚本权限
- ✅ 创建 .gitignore

### 方法二：手动安装

```bash
# 1. 进入项目目录
cd /Users/code/Eason

# 2. 创建虚拟环境
python3 -m venv .venv

# 3. 激活虚拟环境
source .venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 运行程序
python email_assistant_gui.py
```

## 🔧 详细安装步骤

### 1. 检查 Python 版本

```bash
python3 --version
```

确保版本 ≥ 3.8。如果没有安装，请访问 [python.org](https://www.python.org/downloads/macos/) 下载安装。

### 2. 安装依赖包

#### 选项 A：使用 pip（推荐）

```bash
pip3 install PyQt6
```

#### 选项 B：使用 Homebrew + pip

```bash
# 如果 pip 出现问题，先安装/更新 pip
python3 -m ensurepip --upgrade

# 然后安装 PyQt6
pip3 install PyQt6
```

#### 选项 C：使用虚拟环境（适合开发）

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install PyQt6

# 运行程序
python email_assistant_gui.py
```

### 3. 验证安装

```bash
python3 -c "import PyQt6; print('✅ PyQt6 安装成功')"
```

如果看到 "✅ PyQt6 安装成功"，说明安装成功。

### 4. 运行程序

```bash
python3 email_assistant_gui.py
```

## 🐛 常见安装问题

### 问题 1: pip3 command not found

**解决方案**：

```bash
# 使用 python3 -m pip 代替
python3 -m pip install PyQt6
```

### 问题 2: Permission denied

**解决方案**：

```bash
# 使用 --user 参数安装到用户目录
pip3 install --user PyQt6
```

### 问题 3: SSL Certificate Error

**解决方案**：

```bash
# 更新证书
/Applications/Python\ 3.9/Install\ Certificates.command

# 或使用 --trusted-host
pip3 install --trusted-host pypi.org --trusted-host files.pythonhosted.org PyQt6
```

### 问题 4: Multiple Python versions

如果有多个 Python 版本，明确指定版本：

```bash
# 查看所有 Python 版本
ls /Library/Frameworks/Python.framework/Versions/

# 使用特定版本
/Library/Frameworks/Python.framework/Versions/3.9/bin/python3 -m pip install PyQt6
```

## 📦 打包为独立应用

安装打包工具：

```bash
pip3 install pyinstaller
```

执行打包脚本：

```bash
./build_app.sh
```

打包完成后，应用位于 `dist/邮件助手.app`。

## 💡 使用建议

### 开发模式

如果需要修改代码：

```bash
# 1. 创建虚拟环境
python3 -m venv venv

# 2. 激活环境
source venv/bin/activate

# 3. 安装开发依赖
pip install -r requirements.txt

# 4. 运行程序
python email_assistant_gui.py

# 5. 退出虚拟环境
deactivate
```

### 生产模式

如果只是使用：

```bash
# 直接运行启动脚本
./run.sh
```

或打包为应用：

```bash
./build_app.sh
```

## 🆘 获取帮助

如果遇到问题：

1. 查看 [README.md](README.md) 的常见问题部分
2. 检查 Python 和 pip 版本是否符合要求
3. 尝试使用虚拟环境隔离依赖
4. 查看详细错误信息并搜索解决方案

## 📋 系统要求清单

- ✅ macOS 10.14+ (Mojave 或更高)
- ✅ Python 3.8+
- ✅ pip 20.0+
- ✅ 至少 100MB 可用磁盘空间
- ✅ 网络连接（用于安装依赖和发送邮件）

## 🎉 安装完成

安装成功后，你可以：

1. 运行 `./run.sh` 启动程序
2. 运行 `./build_app.sh` 打包为独立应用
3. 查看 `README.md` 了解使用方法
