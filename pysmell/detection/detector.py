from __future__ import division 
import csv

counts = {'django': [0,0,0],'numpy': [0,0,0],'ipython': [0,0,0],'boto': [0,0,0],'tornado': [0,0,0],
'matplotlib': [0,0,0],'scipy': [0,0,0], 'nltk': [0,0,0],'ansible': [0,0,0] }

PAR = [5,4,5]
MLOC = [38,28,52]
DOC = [3,4,4]
CLOC = [29,59,37]
LMC = [5,4,4]
NBC = [3,2,3]
NOC,LPAR,NOO = [48,82,73],[3,3,4],[7,13,15]
TNOC,TNOL = [54,102,101],[3,3,3]
CNOC,NOFF,CNOO = [62,131,92],[3,3,3],[8,24,22]
LEC,DNC,NCT = [3,3,3],[3,4,3],[3,2,2]

portion = {}

smells = {'LongParameterList':[PAR],'LongMethod':[MLOC],'LongScopeChaining':[DOC],'LongBaseClassList':[NBC],
'LargeClass':[CLOC],'LongMessageChain':[LMC], 'LongLambdaFunction':[NOC,LPAR,NOO],
'LongTernaryConditionalExpression':[TNOC,TNOL], 'ComplexContainerComprehension':[CNOC,NOFF,CNOO],
'MultiplyNestedContainer':[LEC,DNC,NCT] }

count_log = open('metric\\count9.txt',mode='wb+')

for smellname in smells.keys():
	count_log.write("################################%s################################\r\n" %smellname)
	for sub in counts.keys():
		counts[sub] = [0,0,0]
	reader = csv.reader(open('metric\\%s.csv' %smellname))
	writer = csv.writer(file('metric\\a_%s.csv' %smellname,'wb'))
	for line in reader:
		if reader.line_num == 1:
			writer.writerow(line+['experience-based','statistics-based','tuning machine'])
			continue
		if smellname=='LongLambdaFunction':
			m1 = smells[smellname][0]
			m2 = smells[smellname][1]
			m3 = smells[smellname][2]
			if int(line[-3])>=m1[0] and (int(line[-2])>=m2[0] or int(line[-1])>=m3[0]):
				flag0 = 1
				counts[line[0]][0] = counts[line[0]][0]+1
			else:
				flag0 = 0
			if int(line[-3])>=m1[1] and (int(line[-2])>=m2[1] or int(line[-1])>=m3[1]):
				flag1 = 1
				counts[line[0]][1] = counts[line[0]][1]+1
			else:
				flag1 = 0
			if int(line[-3])>=m1[2] and (int(line[-2])>=m2[2] or int(line[-1])>=m3[2]):
				flag2 = 1
				counts[line[0]][2] = counts[line[0]][2]+1
			else:
				flag2 = 0
			writer.writerow(line+[flag0,flag1,flag2])
		elif smellname=='ComplexContainerComprehension':
			m1 = smells[smellname][0]
			m2 = smells[smellname][1]
			m3 = smells[smellname][2]
			if (int(line[-3])>=m1[0] and int(line[-1])>=m3[0]) or int(line[-2])>=m2[0]:
				flag0 = 1
				counts[line[0]][0] = counts[line[0]][0]+1
			else:
				flag0 = 0
			if (int(line[-3])>=m1[1] and int(line[-1])>=m3[1]) or int(line[-2])>=m2[1]:
				flag1 = 1
				counts[line[0]][1] = counts[line[0]][1]+1
			else:
				flag1 = 0
			if (int(line[-3])>=m1[2] and int(line[-1])>=m3[2]) or int(line[-2])>=m2[2]:
				flag2 = 1
				counts[line[0]][2] = counts[line[0]][2]+1
			else:
				flag2 = 0
			writer.writerow(line+[flag0,flag1,flag2])
		elif smellname=='LongTernaryConditionalExpression':
			m1 = smells[smellname][0]
			m2 = smells[smellname][1]
			if int(line[-2])>=m1[0] or int(line[-1])>=m2[0]:
				flag0 = 1
				counts[line[0]][0] = counts[line[0]][0]+1
			else:
				flag0 = 0
			if int(line[-2])>=m1[1] or int(line[-1])>=m2[1]:
				flag1 = 1
				counts[line[0]][1] = counts[line[0]][1]+1
			else:
				flag1 = 0
			if int(line[-2])>=m1[2] or int(line[-1])>=m2[2]:
				flag2 = 1
				counts[line[0]][2] = counts[line[0]][2]+1
			else:
				flag2 = 0
			writer.writerow(line+[flag0,flag1,flag2])
		elif smellname=='MultiplyNestedContainer':
			m1 = smells[smellname][0]
			m2 = smells[smellname][1]
			m3 = smells[smellname][2]
			if (len(line[-3])>0 and int(line[-3])>=m1[0]) or (len(line[-1])>0 and int(line[-2])>=m2[0] and int(line[-1])>=m3[0]):
				flag0 = 1
				counts[line[0]][0] = counts[line[0]][0]+1
			else:
				flag0 = 0
			if (len(line[-3])>0 and int(line[-3])>=m1[1]) or (len(line[-1])>0 and int(line[-2])>=m2[1] and int(line[-1])>=m3[1]):
				flag1 = 1
				counts[line[0]][1] = counts[line[0]][1]+1
			else:
				flag1 = 0
			if (len(line[-3])>0 and int(line[-3])>=m1[2]) or (len(line[-1])>0 and int(line[-2])>=m2[2] and int(line[-1])>=m3[2]):
				flag2 = 1
				counts[line[0]][2] = counts[line[0]][2]+1
			else:
				flag2 = 0
			writer.writerow(line+[flag0,flag1,flag2])
		else:
			m = smells[smellname][0]
			if int(line[-1])>=m[0]:
				flag0 = 1
				counts[line[0]][0] = counts[line[0]][0]+1
			else:
				flag0 = 0
			if int(line[-1])>=m[1]:
				flag1 = 1
				counts[line[0]][1] = counts[line[0]][1]+1
			else:
				flag1 = 0
			if int(line[-1])>=m[2]:
				flag2 = 1
				counts[line[0]][2] = counts[line[0]][2]+1
			else:
				flag2 = 0
			writer.writerow(line+[flag0,flag1,flag2])
	for (subject,i) in counts.items():
		count_log.write('%s:   	experience-based %d, statistics-based %d, tuning machine %d\r\n' \
				%(subject,i[0],i[1],i[2]))
		if smellname in portion.keys():
			portion[smellname][subject] = [i[0],i[1],i[2]]
		else:
			portion[smellname] = {}
			portion[smellname][subject] = [i[0],i[1],i[2]]
	count_log.write('\r\n')

total = {} #subject:[total1,total2,total3]
for smellname in portion.keys():
	i = portion[smellname]
	for sub in i.keys():
		if sub in total.keys():
			total[sub][0] = total[sub][0]+i[sub][0]
			total[sub][1] = total[sub][1]+i[sub][1]
			total[sub][2] = total[sub][2]+i[sub][2]
		else:
			total[sub] = i[sub][:]

for smellname in portion.keys():
	i = portion[smellname]
	count_log.write('\r\n%s\r\n' %smellname)
	for sub in i.keys():
		i[sub][0] = i[sub][0]/total[sub][0]
		i[sub][1] = i[sub][1]/total[sub][1]
		i[sub][2] = i[sub][2]/total[sub][2]
		count_log.write('%.2f,%.2f,%.2f,\r\n' %(i[sub][0]*100,i[sub][1]*100,i[sub][2]*100))
count_log.close()