__author__ = 'Zhifei Chen'

# collect detection results of 9 and 106 projects

import csv

projects9_names = ('ansible','boto','django','ipython','matplotlib', 'nltk','numpy','scipy','tornado')
results100_root = "result100\\"

smell_names = ('LongParameterList','LongMethod','LongScopeChaining','LongBaseClassList',
'LargeClass','LongMessageChain', 'LongLambdaFunction','LongTernaryConditionalExpression',
               'ComplexContainerComprehension','MultiplyNestedContainer')

for smell in smell_names:
    print(smell)
    record = csv.reader(open(results100_root+smell+'.csv'))
    counts100 = [0,0,0]
    # counts_for_projects9 = {}
    # for project in projects9_names:
    #     counts_for_projects9[project] = [0,0,0]
    for item in record:
        if record.line_num == 1:
            continue
        counts100[0] += int(item[-3])
        counts100[1] += int(item[-2])
        counts100[2] += int(item[-1])
        # if item[0] in projects9_names:
        #     counts_for_projects9[item[0]][0] += int(item[-3])
        #     counts_for_projects9[item[0]][1] += int(item[-2])
        #     counts_for_projects9[item[0]][2] += int(item[-1])
    # for project in projects9_names:
    #     print '%s:%d %d %d' %(project,counts_for_projects9[project][0],counts_for_projects9[project][1],counts_for_projects9[project][2])
    # print counts100[0],counts100[1],counts100[2]
    print counts100[0]/106,counts100[1]/106,counts100[2]/106
    # print counts100[0]/5.690635,counts100[1]/5.690635,counts100[2]/5.690635
    # print '\n'
