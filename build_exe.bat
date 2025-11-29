@echo off
REM 打包为可双击运行的 shutdown_timer.exe
pyinstaller --noconsole --onefile --name shutdown_timer shutdown_timer.py
IF %ERRORLEVEL% NEQ 0 (
    echo 打包失败，请检查 PyInstaller 是否已安装。
    exit /b %ERRORLEVEL%
)
echo 打包完成：dist\shutdown_timer.exe
