#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Step-by-step script to reuse existing templates, match test logs, and evaluate with RI precision.
The flow follows logTIM's matching logic but skips any adaptive training or template updates.
"""

# 1. 导入需要的模块和工具
import os
import re
import argparse
from globalConfig import DATA_PATH, RESULT_PATH, regL
from matchTree import MatchTree
from RI_precision import prePara, process


# 2. 解析命令行参数，给出常用路径的默认值
parser = argparse.ArgumentParser()
parser.add_argument('-dataset', type=str, default='2kBGL', help='数据集名称')
parser.add_argument('-algorithm', type=str, default='FT_tree', help='使用的解析算法，用于确定模板目录')
parser.add_argument('-ratio', type=float, default=0.10, help='head/tail 划分比例，例如 0.10')
parser.add_argument('-templates', type=str, default='', help='可选：直接指定 logTemplates.txt 的路径')
parser.add_argument('-test_log', type=str, default='', help='可选：直接指定需要匹配的 rawlog 路径')
parser.add_argument('-output', type=str, default='', help='输出匹配结果的目录，默认写入 ./results/static_match_results/...')
parser.add_argument('-eval', type=int, default=1, help='是否调用 RI_precision 进行评估，1 表示评估，0 表示跳过')
args = parser.parse_args()


# 3. 根据参数准备路径，尽量复用项目现有的目录结构
ratio_str = f"{args.ratio:.2f}"
# 默认模板路径：./results/{ALGO}_results/{DATASET}_head_RATIO/logTemplates.txt
if args.templates:
    template_file = args.templates
else:
    template_dir = os.path.join(RESULT_PATH, f"{args.algorithm}_results", f"{args.dataset}_head_{ratio_str}")
    template_file = os.path.join(template_dir, 'logTemplates.txt')

# 默认测试日志：./data/{DATASET}_tail_RATIO/rawlog.log
if args.test_log:
    test_log_file = args.test_log
else:
    test_dir = os.path.join(DATA_PATH, f"{args.dataset}_tail_{ratio_str}")
    test_log_file = os.path.join(test_dir, 'rawlog.log')

# 默认输出目录：./results/static_match_results/{ALGO}_results/{DATASET}_tail_RATIO/
if args.output:
    output_dir = args.output
else:
    output_dir = os.path.join(RESULT_PATH, 'static_match_results', f"{args.algorithm}_results", f"{args.dataset}_tail_{ratio_str}")

# 评估所需的 ground truth 目录：默认使用 tail 数据所在目录
if args.test_log:
    gt_dir = os.path.dirname(os.path.abspath(test_log_file))
else:
    gt_dir = test_dir

print('模板文件:', template_file)
print('测试日志:', test_log_file)
print('输出目录:', output_dir)
print('ground truth 目录:', gt_dir)


# 4. 加载模板并构建前缀树匹配器
matcher = MatchTree()
if not os.path.exists(template_file):
    raise FileNotFoundError(f"找不到模板文件: {template_file}")

with open(template_file, 'r') as f:
    template_lines = [line.strip() for line in f.readlines() if line.strip()]

for idx, line in enumerate(template_lines):
    parts = line.split('\t')
    if len(parts) == 2:
        temp_id = int(parts[0])
        temp_words = parts[1].split(' ')
    else:
        temp_id = idx + 1
        temp_words = line.split(' ')
    matcher.add_template(temp_words, template_id=temp_id)

print('已载入模板数:', matcher.templateNum())


# 5. 读取测试日志，并在缺少行号时自动补上
if not os.path.exists(test_log_file):
    raise FileNotFoundError(f"找不到测试日志: {test_log_file}")

with open(test_log_file, 'r') as f:
    raw_logs = f.readlines()

# 统一格式：每行形如 "编号\t内容"
if raw_logs and len(raw_logs[0].split('\t')) == 1:
    raw_logs = [f"{i+1}\t{line}" for i, line in enumerate(raw_logs)]


# 6. 逐条匹配日志，未匹配到的日志标记为模板 0
os.makedirs(output_dir, exist_ok=True)
match_results = []
regex_rules = regL.get(args.dataset, [])

for line in raw_logs:
    log_id, log_text = line.strip().split('\t', 1)

    # 清洗日志内容（沿用 globalConfig 中的规则）
    cleaned_log = log_text
    for current_rex in regex_rules:
        cleaned_log = re.sub(current_rex, '', cleaned_log)

    log_words = cleaned_log.strip().split(' ')
    result = matcher.match_template(log_words)
    if result:
        template_id, variables = result
    else:
        template_id, variables = 0, ''

    match_results.append((template_id, variables))

    # 保存到对应的模板文件，便于后续 RI_precision 读取
    template_path = os.path.join(output_dir, f"template{template_id}.txt")
    with open(template_path, 'a') as f:
        f.write(f"{log_id}\t{log_text}\n")


# 7. 写出 matchResults.txt 和 logTemplates.txt
with open(os.path.join(output_dir, 'matchResults.txt'), 'w') as f:
    for item in match_results:
        f.write('\t'.join(map(str, item)) + '\n')

with open(os.path.join(output_dir, 'logTemplates.txt'), 'w') as f:
    for line in template_lines:
        f.write(line + '\n')

print('匹配完成，结果写入:', output_dir)


# 8. 可选：调用 RI_precision 进行评估
if args.eval:
    print('开始评估 RI_precision...')
    parameters = prePara(
        groundTruthDataPath=os.path.join(gt_dir, ''),
        logName=os.path.basename(test_log_file),
        geneDataPath=os.path.join(output_dir, '')
    )
    process(parameters)
else:
    print('跳过评估，可使用 -eval 0 关闭本步骤')
