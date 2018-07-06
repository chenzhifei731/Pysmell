import astChecker
import util
import customast
import os
import time
import csv
import numpy as np
from matplotlib import pyplot
from parameter import subject_dir


def compute_statistics(metricdata):
    return (np.mean(metricdata)+np.std(metricdata))*1.5


subjects = util.subDirectory(subject_dir)
metric_file = csv.writer(open('metric\\metric_file.csv', 'wb+'))
metric_file.writerow(['Project','PAR','MLOC','DOC','NBC','CLOC','NOC','LPAR','NOO',
                      'TNOC','TNOL','CNOC','NOFF','CNOO','LMC','LEC','DNC','NCT'])

for subjectName in subjects:
    sourcedir = subject_dir + '\\'+ subjectName
    print 'processing', subjectName
    PAR,MLOC,DOC,NBC,CLOC,NOC,LPAR,NOO,TNOC,TNOL,CNOC,NOFF,CNOO,LMC,LEC,DNC,NCT = [],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]
    smells = {'LongParameterList':{'PAR':PAR},'LongMethod':{'MLOC':MLOC},'LongScopeChaining':{'DOC':DOC},
          'LongBaseClassList':{'NBC':NBC},'LargeClass':{'CLOC':CLOC},'LongMessageChain':{'LMC':LMC},
          'ComplexLambdaExpression':{'NOC':NOC,'PAR':LPAR,'NOO':NOO},'LongTernaryConditionalExpression':{'NOC':TNOC,'NOL':TNOL},
          'ComplexContainerComprehension':{'NOC':CNOC,'NOFF':NOFF,'NOO':CNOO},'MultiplyNestedContainer':{'LEC':LEC,'DNC':DNC,'NCT':NCT}
          }
    for currentFileName in util.walkDirectory(sourcedir):
        try:
            astContent = customast.parse_file(currentFileName)
        except:
            print sourcedir, currentFileName
            continue
        myast = astChecker.MyAst()
        myast.fileName = currentFileName
        myast.visit(astContent)
        for item in myast.result:
            if item[0] == 1:
                PAR.append(item[3])
                # LongParameter.writerow([name,tag,item[1],item[2],item[3]])
            elif item[0] == 2:
                MLOC.append(item[3])
                # LongMethod.writerow([name,tag,item[1],item[2],item[3]])
            elif item[0] == 3:
                DOC.append(item[3])
                # LongScopeChaining.writerow([name,tag,item[1],item[2],item[3]])
            elif item[0] == 4:
                NBC.append(item[3])
                # LongBaseClass.writerow([name,tag,item[1],item[2],item[3]])
            elif item[0] == 5:
                CLOC.append(item[3])
                # LargeClass.writerow([name,tag,item[1],item[2],item[3]])
            elif item[0] == 6:
                if len(item)==4:
                    LEC.append(item[3])
                    # MultiplyNestedContainer.writerow([name,tag,item[1],item[2],item[3],'',''])
                else:
                    DNC.append(item[3])
                    NCT.append(item[4])
                    # MultiplyNestedContainer.writerow([name,tag,item[1],item[2],'',item[3],item[4]])
            elif item[0] == 9:
                NOC.append(item[3])
                LPAR.append(item[4])
                NOO.append(item[5])
                # ComplexLambda.writerow([name,tag,item[1],item[2],item[3],item[4],item[5]])
            elif item[0] == 10:
                TNOC.append(item[3])
                TNOL.append(item[4])
                # LongTernary.writerow([name,tag,item[1],item[2],item[3],item[4]])
            elif item[0] == 11:
                CNOC.append(item[3])
                NOFF.append(item[4])
                CNOO.append(item[5])
                # ContainerComprehension.writerow([name,tag,item[1],item[2],item[3],item[4],item[5]])
            elif item[0] == 13:
                LMC.append(item[3])
                # LongMessageChain.writerow([name,tag,item[1],item[2],item[3]])

    metric_file.writerow([subjectName, compute_statistics(PAR),compute_statistics(MLOC),compute_statistics(DOC),
                            compute_statistics(NBC),compute_statistics(CLOC),compute_statistics(NOC),
                            compute_statistics(LPAR),compute_statistics(NOO),compute_statistics(TNOC),
                            compute_statistics(TNOL),compute_statistics(CNOC),compute_statistics(NOFF),
                            compute_statistics(CNOO),compute_statistics(LMC),compute_statistics(LEC),
                            compute_statistics(DNC),compute_statistics(NCT)])
