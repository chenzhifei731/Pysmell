from __future__ import division 
import csv

# counts = {'django': [0,0,0,0],'numpy': [0,0,0,0],'ipython': [0,0,0,0],'boto': [0,0,0,0],'tornado': [0,0,0,0],
# 'matplotlib': [0,0,0,0],'scipy': [0,0,0,0], 'nltk': [0,0,0,0],'ansible': [0,0,0,0] }

des = ["experience-based","statistics-based","median","60th","70th","99th","outliers","tuning machine"]
PAR = [5,4,1,1,2,5,21,4]
MLOC = [24,28,4,5,8,55,656,27]
DOC = [3,4,2,2,2,3,-1,4]
NBC = [3,2,1,1,1,2,-1,2]
CLOC = [23,59,4,5,6,78,4633,22]
LMC = [5,4,2,2,2,4,-1,4]
NOC,LPAR,NOO = [50,82,25,30,36,115,356,75],[3,3,1,1,1,4,7,3],[7,13,4,5,5,19,67,12]
TNOC,TNOL = [58,102,42,47,52,118,470,90],[2,3,1,1,1,3,-1,4]
CNOC,NOFF,CNOO = [65,131,43,48,55,164,1762,118],[3,3,1,1,1,3,-1,4],[12,24,8,9,11,28,261,22]
LEC,DNC,NCT = [3,3,1,1,1,2,-1,3],[3,4,2,2,2,5,-1,3],[3,2,1,1,1,2,-1,2]

portion = {}

smells = {'LongParameterList':[PAR],'LongMethod':[MLOC],'LongScopeChaining':[DOC],'LongBaseClassList':[NBC],
'LargeClass':[CLOC],'LongMessageChain':[LMC], 'LongLambdaFunction':[NOC,LPAR,NOO],
'LongTernaryConditionalExpression':[TNOC,TNOL], 'ComplexContainerComprehension':[CNOC,NOFF,CNOO],
'MultiplyNestedContainer':[LEC,DNC,NCT] }

index = 4
count_log = open('metric\\count_%s.txt' %des[index], mode='w+')



for smellname in smells.keys():
	count_log.write("################################%s################################\r\n" %smellname)
	# for sub in counts.keys():
	# 	counts[sub] = [0,0,0,0]
	reader = csv.reader(open('metric\\a_%s.csv' %smellname))	
	writer = csv.writer(open('example repository\definite negative\\%s.csv' %smellname,'wb'))
	count = 0
	total = 0
	for line in reader:
		if reader.line_num == 1:
			writer.writerow(line[0:-1]+['manual analysis'])
			continue
		total = total+1
		if smellname=='LongLambdaFunction':
			m1 = smells[smellname][0]
			m2 = smells[smellname][1]
			m3 = smells[smellname][2]
			if int(line[4])>m1[index] and (int(line[5])>m2[index] or int(line[6])>m3[index]):
				if index!=3 and index!=4:
					count = count+1
					writer.writerow(line)
			else:
				if index==3 or index==4:
					count = count+1
					writer.writerow(line)
		elif smellname=='ComplexContainerComprehension':
			m1 = smells[smellname][0] #CNOC
			m2 = smells[smellname][1] #NOFF
			m3 = smells[smellname][2] #CNOO
			if (int(line[4])>m1[index] and int(line[6])>m3[index]) or int(line[5])>m2[index]:
				if index!=3 and index!=4:
					count = count+1
					writer.writerow(line)
			else:
				if index==3 or index==4:
					count = count+1
					writer.writerow(line)
		elif smellname=='LongTernaryConditionalExpression':
			m1 = smells[smellname][0]
			m2 = smells[smellname][1]
			if int(line[4])>m1[index] or int(line[5])>m2[index]:
				if index!=3 and index!=4:
					count = count+1
					writer.writerow(line)
			else:
				if index==3 or index==4:
					count = count+1
					writer.writerow(line)
		elif smellname=='MultiplyNestedContainer':
			m1 = smells[smellname][0]
			m2 = smells[smellname][1]
			m3 = smells[smellname][2]
			if (len(line[4])>0 and int(line[4])>m1[index]) or (len(line[6])>0 and int(line[5])>m2[index] and int(line[6])>m3[index]):
				if index!=3 and index!=4:
					count = count+1
					writer.writerow(line)
			else:
				if index==3 or index==4:
					count = count+1
					writer.writerow(line)
		else:
			m = smells[smellname][0]
			if int(line[4])>m[index]:
				if index!=3 and index!=4:
					count = count+1
					writer.writerow(line)
			else:
				if index==3 or index==4:
					count = count+1
					writer.writerow(line)
	count_log.write("total:%d  " %total)
	count_log.write('%s:%d\r\n' %(des[index],count))