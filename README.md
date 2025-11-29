# Shutdown Timer

一个简单的图形化关机定时器，支持以 `m`（分钟）或 `s`（秒）为单位直接输入数字进行倒计时。

## 使用方法

```bash
python shutdown_timer.py
```

1. 在输入框键入时间，例如 `5m` 或 `30s`。
2. 可勾选“计时后执行系统关机”来在计时结束后尝试调用系统关机命令（默认只提示）。
3. 点击“开始计时”后可看到剩余时间提示；需要中止时可点击“停止”。

> 默认不会真正执行关机，避免误操作；如需关机请勾选复选框。应用会自动选择 Windows 或类 Unix 系统常见的关机命令。

## 生成可双击运行的 Windows EXE

如果希望直接通过 `shutdown_timer.exe` 打开界面，可以在 Windows 上使用 [PyInstaller](https://pyinstaller.org/) 打包：

1. 安装依赖：

   ```bash
   python -m pip install pyinstaller
   ```

2. 运行仓库根目录下的 `build_exe.bat`（或直接执行同等命令）：

   ```bash
   pyinstaller --noconsole --onefile --name shutdown_timer shutdown_timer.py
   ```

3. 完成后在 `dist/` 目录下会生成 `shutdown_timer.exe`，双击即可打开界面输入 `5m`/`30s` 等倒计时。
