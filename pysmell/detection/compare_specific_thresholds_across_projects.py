__author__ = 'Zhifei Chen'
import csv
from matplotlib import pyplot

threshold_record = csv.reader(open('metric\metric_file.csv'))
# [PAR,MLOC,DOC,NBC,CLOC,NOC,LPAR,NOO,TNOC,TNOL,CNOC,NOFF,CNOO,LMC,LEC,DNC,NCT] = [[]]*17
metrics = ['PAR','MLOC','DOC','NBC','CLOC','NOC','LPAR','NOO','TNOC','TNOL','CNOC','NOFF','CNOO','LMC','LEC','DNC','NCT']

xlabels = ('LPL.PAR','LM.MLOC','LSC.DOC','LBCL.NBC',
              'LC.CLOC','LLF.NOC','LLF.PAR',
              'LLF.NOO','LTCE.NOC','LTCE.NOL',
              'CCC.NOC','CCC.NOFF','CCC.NOO',
              'LMC.LMC','MNC.LEC','MNC.DNC','MNC.NCT')

thresholds = {'PAR':[],'MLOC':[],'DOC':[],'NBC':[],'CLOC':[],'NOC':[],'LPAR':[],
              'NOO':[],'TNOC':[],'TNOL':[],
              'CNOC':[],'NOFF':[],'CNOO':[],'LMC':[],'LEC':[],'DNC':[],'NCT':[]}

# thresholds = {'PAR':PAR,'MLOC':MLOC,'DOC':DOC,'NBC':NBC,'CLOC':CLOC,'NOC':NOC,'PAR':LPAR,
#               'NOO':NOO,'NOC':TNOC,'NOL':TNOL,
#               'NOC':CNOC,'NOFF':NOFF,'NOO':CNOO,'LMC':LMC,'LEC':LEC,'DNC':DNC,'NCT':NCT}
# for metrics in thresholds.values():
#     metrics = []

for project_thresholds in threshold_record:
    if threshold_record.line_num == 1:
        continue
    newitem = [t for t in project_thresholds[1:]]
    for i in range(len(newitem)):
        if newitem[i]!='nan':
            thresholds[metrics[i]].append(float(newitem[i]))


data = []
for i in range(len(xlabels)):
    data.append(thresholds[metrics[i]])
pyplot.boxplot(data,labels=xlabels)
pyplot.show()
# pyplot.savefig('specific_metrics.png')
# pyplot.close()