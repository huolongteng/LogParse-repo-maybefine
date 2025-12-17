from matchTree import *
import csv

template_path = "overall_results/IPLoM_result/HPC_2k.log_templates.csv"
Template = []
with open(template_path, "r") as f:
    f = csv.reader(f)
    for row in f:
        Template.append(row[1])
Template.pop(0)


