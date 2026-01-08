@echo off
REM ===== 强制 UTF-8 code page（关键）=====
chcp 65001 > nul

REM ===== 强制 Python stdout 编码（关键）=====
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

setlocal EnableDelayedExpansion

REM ================= 基本参数 =================
set RATIO=0.1
set EVAL_FLAG=1

set ALGORITHM_LIST=IPLoM LKE LogSig FT_tree Spell Drain MoLFI
set DATASET_LIST=2kBGL 2kHPC 2kHDFS 2kZookeeper 2kProxifier 2kLinux 2kHadoop

REM ================= 日志目录 =================
set LOG_ROOT=logs\logTIM
if not exist %LOG_ROOT% mkdir %LOG_ROOT%

REM ================= 主循环 =================
for %%A in (%ALGORITHM_LIST%) do (
  for %%D in (%DATASET_LIST%) do (

    set LOG_FILE=%LOG_ROOT%\%%A_%%D_%RATIO%.log

    echo ================================================== >> "!LOG_FILE!"
    echo RUN: logTIM %%A %%D %RATIO% %EVAL_FLAG% >> "!LOG_FILE!"
    echo START: %DATE% %TIME% >> "!LOG_FILE!"
    echo ================================================== >> "!LOG_FILE!"

    REM ===== -u 禁用缓冲，确保逐行写入 =====
    python -u .\logTIM.py %%A %%D %RATIO% %EVAL_FLAG% >> "!LOG_FILE!" 2>&1

    echo. >> "!LOG_FILE!"
    echo END: %DATE% %TIME% >> "!LOG_FILE!"
    echo ================================================== >> "!LOG_FILE!"

  )
)

echo.
echo All logTIM experiments finished.
pause
