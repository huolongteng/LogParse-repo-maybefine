from RI_precision import *

gt_path = 'data/2kHPC/'
pd_path = "results/logTIM_results/template_match_only/2kHPC_0.10/"
logname = 'rawlog.log'

parameters=prePara(groundTruthDataPath=gt_path ,logName = logname , geneDataPath=pd_path)
TP,FP,TN,FN,p,r,f,RI=process(parameters)

