import re
from matchTree import *

with open("results/IPLoM_results/2kHPC_head_0.10/logTemplates.txt", "r") as f:
    templates = [line.strip() for line in f.readlines()]

with open("data/2kHPC_tail_0.10/rawlog.log", "r") as f:
    logs = [re.sub(r'^\s*\d+\s*', '', line.strip()) for line in f.readlines()]

matcher = MatchTree()
print("add templates")
for t in templates:
    print(matcher.add_template(t.split(" ")))
print("match logs")
for l in logs:
    print(matcher.match_template(l.split(" ")))
print("template map")
print(matcher.template_map)


# This block is used to calculate the RI precision.
# from RI_precision import *
# gt_path = "data/2kHPC_tail_0.10/"
# pd_path = "results/LogSig_results/test_res/"
# logname = "rawlog.log"
# parameters=prePara(groundTruthDataPath=gt_path ,logName = logname , geneDataPath=pd_path)
# TP,FP,TN,FN,p,r,f,RI=process(parameters)