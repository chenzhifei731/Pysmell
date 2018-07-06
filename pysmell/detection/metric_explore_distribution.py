
import astChecker
import util
import customast
import numpy as np
from matplotlib import pyplot
from parameter import subject_dir


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

metric= open('metric.txt',mode='w')

subjects = util.subDirectory(subject_dir)
total_lines = 0
total_files = 0
for subjectName in subjects:
    # metric.write("projeect:%s " %subjectName)
    sourcedir = subject_dir + '\\'+ subjectName
    lines = 0
    files = 0
    for currentFileName in util.walkDirectory(sourcedir):
      try:
        astContent = customast.parse_file(currentFileName)
      except:
        print sourcedir,currentFileName
        continue
      myast = astChecker.MyAst()
      myast.fileName = currentFileName
      # lines = lines + myast.count_lines(astContent)
      files = files + 1
      myast.visit(astContent)
      for item in myast.result:
        if item[0] == 1:
          PAR.append(item[3])
        elif item[0] == 2:
          MLOC.append(item[3])
        elif item[0] == 3:
          DOC.append(item[3])
        elif item[0] == 4:
          NBC.append(item[3])
        elif item[0] == 5:
          CLOC.append(item[3])
        elif item[0] == 6:
          if len(item)==4:
            LEC.append(item[3])
          else:
            DNC.append(item[3])
            NCT.append(item[4])
        elif item[0] == 9:
          NOC.append(item[3])
          LPAR.append(item[4])
          NOO.append(item[5])
        elif item[0] == 10:
          TNOC.append(item[3])
          TNOL.append(item[4])
        elif item[0] == 11:
          CNOC.append(item[3])
          NOFF.append(item[4])
          CNOO.append(item[5])
        elif item[0] == 13:
          LMC.append(item[3])
    # metric.write("LOC:%d #files:%d\n"  %(lines,files))
    total_lines = total_lines + lines
    total_files = total_files + files

metric.write("\n*******************Total Prjects:%d*********************\n" %len(subjects))
metric.write("\n*******************Total LOC:%d*********************\n" %total_lines)
metric.write("\n*******************Total Files:%d*********************\n\n\n" %total_files)
for smellname in smells.keys():
  metric.write("\n####################################%s####################################\n\n" %smellname)
  for metricname in smells[smellname].keys():
    metricdata = smells[smellname][metricname]
    outliers = pyplot.boxplot(metricdata)['fliers'][0].get_data()[1]
    metric.write("%s:  count %d, max %d, min %d, mean %s, 50th percentile %s, 60th percentile %s, 70th percentile %s, 98th percentile %s,99th percentile %s,plot-box outlier %d\n\n" \
  %(metricname,len(metricdata),max(metricdata),min(metricdata),np.mean(metricdata),np.percentile(metricdata,50),
    np.percentile(metricdata,60),np.percentile(metricdata,70),np.percentile(metricdata,98),np.percentile(metricdata,99),max(outliers) if len(outliers)>0 else -1))

metric.close()

data = (PAR,MLOC,DOC,CLOC,LMC,NBC,NOC,LPAR,NOO,TNOC,TNOL,CNOC,CNOO,NOFF,LEC,DNC,NCT)
xlabels = ('LPL.PAR','LM.MLOC','LSC.DOC','LC.CLOC','LMC.LMC','LBCL.NBC','LLF.NOC','LLF.PAR','LLF.NOO',
  'LTCE.NOC','LTCE.NOL','CCC.NOC','CCC.NOO','CCC.NOFF','MNC.LEC','MNC.DNC','MNC.NCT')
pyplot.boxplot(data,labels=xlabels,showfliers=False)
pyplot.show()
