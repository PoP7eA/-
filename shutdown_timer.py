#!/usr/bin/env python3
"""Graphical shutdown timer supporting m/s duration inputs.

Enter a duration such as ``5m`` or ``30s``, click **开始计时**, and watch the
countdown. Optionally tick **计时后执行系统关机** to attempt running the system
shutdown command when the timer finishes.
"""
from __future__ import annotations

import platform
import re
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox
from typing import Tuple

DURATION_PATTERN = re.compile(r"^(?P<value>\d+)(?P<unit>[ms])$", re.IGNORECASE)


def parse_duration(duration: str) -> int:
    """Convert a duration string with an ``m`` or ``s`` suffix to total seconds."""
    match = DURATION_PATTERN.match(duration.strip())
    if not match:
        raise ValueError("时间格式必须是形如 5m 或 30s 的数字+单位")

    value = int(match.group("value"))
    unit = match.group("unit").lower()
    if unit == "m":
        return value * 60
    return value


def format_time(seconds: int) -> str:
    minutes, sec = divmod(seconds, 60)
    if minutes and sec:
        return f"{minutes}分{sec}秒"
    if minutes:
        return f"{minutes}分"
    return f"{sec}秒"


def shutdown_command() -> Tuple[str, ...]:
    system = platform.system().lower()
    if system == "windows":
        return ("shutdown", "/s", "/t", "0")
    return ("shutdown", "-h", "now")


def perform_shutdown(execute: bool) -> None:
    if not execute:
        messagebox.showinfo("计时结束", "计时已结束，未执行关机（未勾选关机选项）。")
        return

    command = shutdown_command()
    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("关机命令", "关机命令已执行。")
    except subprocess.CalledProcessError as exc:
        messagebox.showerror("关机失败", f"关机命令执行失败：{exc}")
    except FileNotFoundError:
        messagebox.showerror("关机失败", "未找到系统关机命令，请确认本机支持 shutdown。")


class ShutdownTimerApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("关机定时器")
        self.root.resizable(False, False)

        self.duration_var = tk.StringVar()
        self.execute_var = tk.BooleanVar(value=False)
        self.remaining_seconds: int | None = None
        self.timer_job: str | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        padding = {"padx": 12, "pady": 8}

        title = tk.Label(self.root, text="请输入倒计时时间 (如 5m 或 30s)", font=("Arial", 12, "bold"))
        title.grid(row=0, column=0, columnspan=2, **padding)

        entry = tk.Entry(self.root, textvariable=self.duration_var, width=15, font=("Arial", 12))
        entry.grid(row=1, column=0, sticky="ew", **padding)
        entry.focus_set()

        start_btn = tk.Button(self.root, text="开始计时", command=self.start_countdown, width=12)
        start_btn.grid(row=1, column=1, **padding)

        self.status_label = tk.Label(self.root, text="尚未开始", font=("Arial", 11))
        self.status_label.grid(row=2, column=0, columnspan=2, **padding)

        execute_check = tk.Checkbutton(
            self.root, text="计时后执行系统关机", variable=self.execute_var, onvalue=True, offvalue=False
        )
        execute_check.grid(row=3, column=0, columnspan=2, **padding)

        stop_btn = tk.Button(self.root, text="停止", command=self.stop_countdown, width=12)
        stop_btn.grid(row=4, column=0, columnspan=2, **padding)

    def start_countdown(self) -> None:
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

        try:
            total_seconds = parse_duration(self.duration_var.get())
        except ValueError as exc:
            messagebox.showerror("输入错误", str(exc))
            return

        if total_seconds <= 0:
            messagebox.showerror("输入错误", "时间必须大于 0")
            return

        self.remaining_seconds = total_seconds
        self.status_label.config(text=f"剩余时间：{format_time(total_seconds)}")
        self._schedule_tick()

    def _schedule_tick(self) -> None:
        if self.remaining_seconds is None:
            return

        if self.remaining_seconds <= 0:
            self.status_label.config(text="计时结束！")
            perform_shutdown(self.execute_var.get())
            self.timer_job = None
            return

        self.status_label.config(text=f"剩余时间：{format_time(self.remaining_seconds)}")
        self.remaining_seconds -= 1
        self.timer_job = self.root.after(1000, self._schedule_tick)

    def stop_countdown(self) -> None:
        if self.timer_job is not None:
            self.root.after_cancel(self.timer_job)
            self.timer_job = None
        self.remaining_seconds = None
        self.status_label.config(text="计时已停止")


def main() -> None:
    root = tk.Tk()
    app = ShutdownTimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
