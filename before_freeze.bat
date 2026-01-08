@echo off
setlocal EnableDelayedExpansion

set RATIO=0.1

set ALGORITHM_LIST=IPLoM LKE LogSig FT_tree Spell Drain MoLFI
set DATASET_LIST=2kBGL 2kHPC 2kHDFS 2kZookeeper 2kProxifier 2kLinux 2kHadoop


for %%A in (%ALGORITHM_LIST%) do (
  for %%D in (%DATASET_LIST%) do (
    echo Running: algorithm=%%A dataset=%%D
    python .\evaluateLogParse.py ^
      -algorithm %%A ^
      -dataset %%D ^
      -ratio %RATIO%
  )
)

echo All done.
pause
