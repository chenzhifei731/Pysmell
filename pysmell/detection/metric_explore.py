import astChecker
import util
import customast
import os
import time
import csv
import numpy as np
from matplotlib import pyplot
from parameter import subject_dir, directory



    #     LongParameterList = open(resultdir+"LongParameterList.txt",mode="w")#1 PAR
    #     LongMethod = open(resultdir+"LongMethod.txt",mode="w") #2 MLOC
    #     LongScopeChaining = open(resultdir+"LongScopeChaining.txt",mode="w") #3 DOC
    #     LongBaseClassList = open(resultdir+"LongBaseClassList.txt",mode="w") #4 NBC
    #     LargeClass = open(resultdir+"LargeClass.txt",mode="w")   #5 CLOC
    #     UselessExceptionHandling = open(resultdir+"UselessExceptionHandling.txt",mode="w") #7
    #     ComplexLambdaExpression = open(resultdir+"ComplexLambdaExpression.txt",mode="w") #9 NOC,LPAR,NOO
    #     LongTernaryConditionalExpression = open(resultdir+"LongTernaryConditionalExpression.txt",mode="w") #10 TNOC,TNOL
    #     ComplexContainerComprehension = open(resultdir+"ComplexContainerComprehension.txt",mode="w") #11 CNOC,NOFC+NOFE,CNOO
    #     LongMessageChain = open(resultdir+"LongMessageChain.txt",mode="w") #13 LMC
    #     MultiplyNestedContainer = open(resultdir+"MultiplyNestedContainer.txt",mode="w") #6 LEC/DNC,NCT
    #     ViolatedMagicMethod = open(resultdir+"ViolatedMagicMethod.txt",mode="w") #12
    #     UnusedImport = open(resultdir+"UnusedImport.txt",mode="w") #8

#1,2,3,4,5,6,9,10,11,13
PAR,MLOC,DOC,NBC,CLOC,NOC,LPAR,NOO,TNOC,TNOL,CNOC,NOFF,CNOO,LMC,LEC,DNC,NCT = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]

smells = {'LongParameterList':{'PAR':PAR},'LongMethod':{'MLOC':MLOC},'LongScopeChaining':{'DOC':DOC},
  'LongBaseClassList':{'NBC':NBC},'LargeClass':{'CLOC':CLOC},'LongMessageChain':{'LMC':LMC},
  'ComplexLambdaExpression':{'NOC':NOC,'PAR':LPAR,'NOO':NOO},'LongTernaryConditionalExpression':{'NOC':TNOC,'NOL':TNOL},
  'ComplexContainerComprehension':{'NOC':CNOC,'NOFF':NOFF,'NOO':CNOO},'MultiplyNestedContainer':{'LEC':LEC,'DNC':DNC,'NCT':NCT}
}

LongParameter = csv.writer(file('metric\\LongParameterList.csv','wb'))
LongParameter.writerow(['subject','tag','file','lineno','PAR'])
LongMethod = csv.writer(file('metric\\LongMethod.csv','wb'))
LongMethod.writerow(['subject','tag','file','lineno','MLOC'])
LongScopeChaining = csv.writer(file('metric\\LongScopeChaining.csv','wb'))
LongScopeChaining.writerow(['subject','tag','file','lineno','DOC'])
LongBaseClass = csv.writer(file('metric\\LongBaseClassList.csv','wb'))
LongBaseClass.writerow(['subject','tag','file','lineno','NBC'])
LargeClass = csv.writer(file('metric\\LargeClass.csv','wb'))
LargeClass.writerow(['subject','tag','file','lineno','CLOC'])
ComplexLambda = csv.writer(file('metric\\ComplexLambdaExpression.csv','wb'))
ComplexLambda.writerow(['subject','tag','file','lineno','NOC','PAR','NOO'])
LongTernary = csv.writer(file('metric\\LongTernaryConditionalExpression.csv','wb'))
LongTernary.writerow(['subject','tag','file','lineno','NOC','NOL'])
ContainerComprehension = csv.writer(file('metric\\ComplexContainerComprehension.csv','wb'))
ContainerComprehension.writerow(['subject','tag','file','lineno','NOC','NOFF','NOO'])
LongMessageChain = csv.writer(file('metric\\LongMessageChain.csv','wb'))
LongMessageChain.writerow(['subject','tag','file','lineno','LMC'])
MultiplyNestedContainer = csv.writer(file('metric\\MultiplyNestedContainer.csv','wb'))
MultiplyNestedContainer.writerow(['subject','tag','file','lineno','LEC','DNC','NCT'])

for name in directory.keys():
    sourcedir = subject_dir+name+'\\'+name
    tag = directory[name]
    # tags = []
    # with open(subject_dir+name+'\\tags') as f:
    #     for line in f:
    #         tags.append(line.strip())
    # tag = tags[-1]
    # print name,tag
    # util.changegittag(sourcedir,tag)
    # time.sleep(3)
    for currentFileName in util.walkDirectory(sourcedir):
      try:
        astContent = customast.parse_file(currentFileName)
      except:
        print name,tag,currentFileName
        continue
      myast = astChecker.MyAst()
      myast.fileName = currentFileName
      myast.visit(astContent)
      # res = util.execute(currentFileName) #5,2,3
      # if len(res) > 0:
      #   myast.result = myast.result + res
      for item in myast.result:
        if item[0] == 1:
          PAR.append(item[3])
          LongParameter.writerow([name,tag,item[1],item[2],item[3]])
        elif item[0] == 2:
          MLOC.append(item[3])
          LongMethod.writerow([name,tag,item[1],item[2],item[3]])
        elif item[0] == 3:
          DOC.append(item[3])
          LongScopeChaining.writerow([name,tag,item[1],item[2],item[3]])
        elif item[0] == 4:
          NBC.append(item[3])
          LongBaseClass.writerow([name,tag,item[1],item[2],item[3]])
        elif item[0] == 5:
          CLOC.append(item[3])
          LargeClass.writerow([name,tag,item[1],item[2],item[3]])
        elif item[0] == 6:
          if len(item)==4:
            LEC.append(item[3])
            MultiplyNestedContainer.writerow([name,tag,item[1],item[2],item[3],'',''])
          else:
            DNC.append(item[3])
            NCT.append(item[4])
            MultiplyNestedContainer.writerow([name,tag,item[1],item[2],'',item[3],item[4]])
        elif item[0] == 9:
          NOC.append(item[3])
          LPAR.append(item[4])
          NOO.append(item[5])
          ComplexLambda.writerow([name,tag,item[1],item[2],item[3],item[4],item[5]])
        elif item[0] == 10:
          TNOC.append(item[3])
          TNOL.append(item[4])
          LongTernary.writerow([name,tag,item[1],item[2],item[3],item[4]])
        elif item[0] == 11:
          CNOC.append(item[3])
          NOFF.append(item[4])
          CNOO.append(item[5])
          ContainerComprehension.writerow([name,tag,item[1],item[2],item[3],item[4],item[5]])
        elif item[0] == 13:
          LMC.append(item[3])
          LongMessageChain.writerow([name,tag,item[1],item[2],item[3]])

metric= open('metric\\metric.txt',mode='w')

for smellname in smells.keys():
  metric.write("\n####################################%s####################################\n\n" %smellname)
  for metricname in smells[smellname].keys():
    metricdata = smells[smellname][metricname]
    outliers = pyplot.boxplot(metricdata)['fliers'][0].get_data()[1]
    metric.write("%s:  count %d, max %d, min %d, mean %s, plot-box outlier %d-%d, statistic very-high %s, 80th percentile %s\n\n" \
  %(metricname,len(metricdata),max(metricdata),min(metricdata),np.mean(metricdata),min(outliers) if len(outliers)>0 else -1,
    max(outliers) if len(outliers)>0 else -1,(np.mean(metricdata)+np.std(metricdata))*1.5,np.percentile(metricdata,80)))

metric.close()
