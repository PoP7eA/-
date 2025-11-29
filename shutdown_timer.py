#!/usr/bin/env python3
"""Simple shutdown timer supporting minute and second suffixes.

Usage examples:
    python shutdown_timer.py 5m           # 5-minute countdown (no shutdown command)
    python shutdown_timer.py 30s --execute  # 30-second countdown then request shutdown
"""
from __future__ import annotations

import argparse
import platform
import re
import subprocess
import sys
import time
from typing import Tuple

DURATION_PATTERN = re.compile(r"^(?P<value>\d+)(?P<unit>[ms])$", re.IGNORECASE)


def parse_duration(duration: str) -> int:
    """Convert a duration string with an `m` or `s` suffix to total seconds.

    Args:
        duration: A string like ``"5m"`` or ``"30s"``.

    Returns:
        The duration converted to seconds.

    Raises:
        argparse.ArgumentTypeError: If the value is not valid.
    """

    match = DURATION_PATTERN.match(duration.strip())
    if not match:
        raise argparse.ArgumentTypeError("时间格式必须是形如 5m 或 30s 的数字+单位")

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


def countdown(total_seconds: int) -> None:
    for remaining in range(total_seconds, 0, -1):
        if remaining % 60 == 0 or remaining <= 10:
            print(f"剩余时间：{format_time(remaining)}")
        time.sleep(1)
    print("计时结束。")


def shutdown_command() -> Tuple[str, ...]:
    system = platform.system().lower()
    if system == "windows":
        return ("shutdown", "/s", "/t", "0")
    return ("shutdown", "-h", "now")


def perform_shutdown(execute: bool) -> None:
    if not execute:
        print("未执行关机（未使用 --execute 选项）。")
        return

    command = shutdown_command()
    print("正在尝试执行关机命令：", " ".join(command))
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"关机命令执行失败：{exc}", file=sys.stderr)
    except FileNotFoundError:
        print("未找到系统关机命令，请确认本机支持 shutdown。", file=sys.stderr)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="简单的关机定时器，支持 m 和 s 为单位的时间输入。")
    parser.add_argument("duration", type=parse_duration, help="时间长度，形如 5m 或 30s")
    parser.add_argument("--execute", action="store_true", help="计时结束后实际执行关机命令。默认只提示不关机。")

    args = parser.parse_args(argv)
    total_seconds: int = args.duration

    print(f"已设置倒计时：{format_time(total_seconds)}")
    countdown(total_seconds)
    perform_shutdown(args.execute)


if __name__ == "__main__":
    main()
