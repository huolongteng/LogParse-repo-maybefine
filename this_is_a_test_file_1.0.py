import sys
from globalConfig import *
sys.path.append(ALGORITHM_PATH)
import algorithm.IPLoM as iplom
from RI_precision import *
from globalConfig import *
import numpy as np
import time
import os
import shutil

def createDir(path, removeflag=0):
    if removeflag == 1:
        shutil.rmtree(path)
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

def evaluateMethods(dataset, algorithm, leaf_num = 30, logname='rawlog.log', choose='all', ratio=0.5, eval_flag=1):
    if choose == 'all':
        dataPath = os.path.join(DATA_PATH, '%s_all/'%dataset)
        dataName = '%s_all'%dataset
    else:
        dataPath = os.path.join(DATA_PATH, '%s_%s_%0.2f/'%(dataset,choose,ratio))
        dataName = '%s_%s_%0.2f'%(dataset,choose,ratio)
    groupNum = int(GroupNum[dataset][choose]*0.5) # caution!
    removeCol=[] # caution!
    result = np.zeros((1,9))

    #######IPLoM############
    if algorithm == "IPLoM":
        print ('dataset:',logname, "IPLoM")
        t1=time.time()
        parserPara = iplom.Para(path=dataPath,  logname = logname,removeCol=removeCol, rex=regL[dataset], savePath=RESULT_PATH+algorithm+'_results/' + dataName+'/')
        print ('parserPara.path',parserPara.path)
        myParser = iplom.IPLoM(parserPara)
        runningTime = myParser.mainProcess()
        t2=time.time()
        # print 'cur_result_path:','./results/LogSig_results/' + dataName+'/'
        #createDir('./results/LKE_results/' + dataName+'/' + dataName,1)
        if eval_flag:
            parameters=prePara(groundTruthDataPath=dataPath ,logName = logname , geneDataPath=RESULT_PATH+algorithm +'_results/' + dataName+'/')
            TP,FP,TN,FN,p,r,f,RI=process(parameters)
        else: print('No evaluation')
        print ('dataset:', logname)
        print ('training time: %0.3f'%(t2-t1))

if __name__ == '__main__':
    dataset = '2kHPC'
    algorithm = 'IPLoM'
    evaluateMethods(dataset, algorithm, choose='head', ratio=0.1, eval_flag=1)
    print ('algorithm:',algorithm)
    print ('Dataset',dataset)
