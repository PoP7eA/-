# Shutdown Timer

一个简单的关机定时器脚本，支持以 `m`（分钟）或 `s`（秒）为单位直接输入数字进行倒计时。

## 使用方法

```bash
python shutdown_timer.py 5m          # 倒计时 5 分钟，仅提示，不执行关机
python shutdown_timer.py 30s         # 倒计时 30 秒，仅提示，不执行关机
python shutdown_timer.py 30s --execute  # 倒计时结束后尝试执行系统关机
```

> 默认不会真正执行关机，避免误操作；如需关机请添加 `--execute` 选项。脚本会自动选择 Windows 或类 Unix 系统常见的关机命令。
