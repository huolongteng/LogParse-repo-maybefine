import os
import glob
import csv

# 配置
LOG_DIR = "logs/logTIM"
OUT_CSV = "logTIM_table.csv"

DATASETS = ["2kHDFS", "2kHadoop", "2kZookeeper", "2kBGL", "2kHPC", "2kLinux", "2kProxifier"]
METHODS = ["IPLoM", "LKE", "LogSig", "FT_tree", "Spell", "Drain", "MoLFI"]

results = {}

for logfile in glob.glob(os.path.join(LOG_DIR, "*.log")):
    fname = os.path.basename(logfile)

    try:
        name = fname.replace(".log", "")
        parts = name.split("_")
        method = parts[0]
        dataset = parts[1]
    except:
        continue

    # 尝试多种编码
    content = ""
    for encoding in ["utf-8", "gbk", "latin-1"]:
        try:
            with open(logfile, "r", encoding=encoding) as f:
                content = f.read()
            break
        except:
            continue

    ri = 0.0
    f1 = 0.0

    # 直接搜索关键行
    for line in content.split("\n"):
        line_lower = line.lower()
        if "ri is" in line_lower or "ri:" in line_lower:
            nums = [s for s in line.split() if s.replace(".", "").replace("-", "").isdigit()]
            if nums:
                ri = float(nums[-1])

        if "f measure" in line_lower or "f1" in line_lower or "f-measure" in line_lower:
            nums = [s for s in line.split() if s.replace(".", "").replace("-", "").isdigit()]
            if nums:
                f1 = float(nums[-1])

    results[(method, dataset)] = {"ri": ri, "f1": f1}
    print(f"{method}_{dataset}: RI={ri}, F1={f1}")  # 调试输出

# 生成表格
# 生成表格
with open(OUT_CSV, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)

    # 写入表头
    header = ["Method"] + DATASETS
    writer.writerow(header)

    # 写入每个方法的结果
    for method in METHODS:
        row_ri = [f"{method} (RI)"]
        row_f1 = [f"{method} (F1)"]

        for dataset in DATASETS:
            key = (method, dataset)
            if key in results:
                row_ri.append(f"{results[key]['ri']:.4f}")
                row_f1.append(f"{results[key]['f1']:.4f}")
            else:
                row_ri.append("N/A")
                row_f1.append("N/A")

        writer.writerow(row_ri)
        writer.writerow(row_f1)

print(f"Results saved to {OUT_CSV}")