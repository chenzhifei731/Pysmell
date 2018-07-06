__author__ = 'Zhifei Chen'

from matplotlib import pyplot
import csv

smell_metrics = {'LongParameterList':['PAR'],'LongMethod':['MLOC'],'LongScopeChaining':['DOC'],
          'LongBaseClassList':['NBC'],'LargeClass':['CLOC'],'LongMessageChain':['LMC'],
          'LongLambdaFunction':['NOC','PAR','NOO'],
          'LongTernaryConditionalExpression':['NOC','NOL'],
          'ComplexContainerComprehension':['NOC','NOFF','NOO'],
          'MultiplyNestedContainer':['LEC','DNC','NCT'] }

projects9 = ['ansible', 'boto', 'django', 'ipython', 'matplotlib', 'nltk', 'numpy', 'scipy', 'tornado']

# def compute_each_sb_threshold_for_9projects():


def compare_metrics_for_projects9():
    for smell in smell_metrics.keys():
        project_2_metrics = {}
        smell_record = csv.reader(open('metric\\'+smell+'.csv'))
        universal_record = csv.reader(open('result100\\'+smell+'.csv'))
        universal_metric = [[] for i in smell_metrics[smell]]
        for record in universal_record:
            if universal_record.line_num == 1:
                continue
            for metric_index in range(len(smell_metrics[smell])):
                if len(record[3+metric_index]) != 0:
                    universal_metric[metric_index].append(int(record[3+metric_index]))
        for record in smell_record:
            if smell_record.line_num == 1:
                continue
            if record[0] not in project_2_metrics.keys():
                project_2_metrics[record[0]] = [[int(m)] if len(m)!=0 else [] for m in record[4:]]
            else:
                for metric_index in range(len(smell_metrics[smell])):
                    if len(record[4+metric_index]) != 0:
                        project_2_metrics[record[0]][metric_index].append(int(record[4+metric_index]))
        # print project_2_metrics
        for metric_index in range(len(smell_metrics[smell])):
            metric = smell_metrics[smell][metric_index]
            data = [project_2_metrics[project][metric_index] for project in projects9] + [universal_metric[metric_index]]
            xlabels = projects9[:] + ['Total']
            pyplot.boxplot(data,labels=xlabels)
            pyplot.savefig('metric_figures\\%s.%s.png' %(smell, metric))
            pyplot.close()


if __name__ == '__main__':
    compare_metrics_for_projects9()
