from __future__ import division 
import csv
import os
import util
import astChecker
import customast
from parameter import subject_dir


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

myportion = open('result100\\portion.txt',mode='wb+')

smells = {'LongParameterList':[PAR],'LongMethod':[MLOC],'LongScopeChaining':[DOC],'LongBaseClassList':[NBC],
'LargeClass':[CLOC],'LongMessageChain':[LMC], 'LongLambdaFunction':[NOC,LPAR,NOO],
'LongTernaryConditionalExpression':[TNOC,TNOL], 'ComplexContainerComprehension':[CNOC,NOFF,CNOO],
'MultiplyNestedContainer':[LEC,DNC,NCT] }

subjects = util.subDirectory(subject_dir)

LongParameterList = csv.writer(file('result100\\LongParameterList.csv','wb'))
LongParameterList.writerow(['subject','file','lineno','PAR','experience-based','statistics-based','tuning machine'])
LongMethod = csv.writer(file('result100\\LongMethod.csv','wb'))
LongMethod.writerow(['subject','file','lineno','MLOC','experience-based','statistics-based','tuning machine'])
LongScopeChaining = csv.writer(file('result100\\LongScopeChaining.csv','wb'))
LongScopeChaining.writerow(['subject','file','lineno','DOC','experience-based','statistics-based','tuning machine'])
LongBaseClassList = csv.writer(file('result100\\LongBaseClassList.csv','wb'))
LongBaseClassList.writerow(['subject','file','lineno','NBC','experience-based','statistics-based','tuning machine'])
LargeClass = csv.writer(file('result100\\LargeClass.csv','wb'))
LargeClass.writerow(['subject','file','lineno','CLOC','experience-based','statistics-based','tuning machine'])
LongLambdaFunction = csv.writer(file('result100\\LongLambdaFunction.csv','wb'))
LongLambdaFunction.writerow(['subject','file','lineno','NOC','PAR','NOO','experience-based','statistics-based','tuning machine'])
LongTernaryConditionalExpression = csv.writer(file('result100\\LongTernaryConditionalExpression.csv','wb'))
LongTernaryConditionalExpression.writerow(['subject','file','lineno','NOC','NOL','experience-based','statistics-based','tuning machine'])
ComplexContainerComprehension = csv.writer(file('result100\\ComplexContainerComprehension.csv','wb'))
ComplexContainerComprehension.writerow(['subject','file','lineno','NOC','NOFF','NOO','experience-based','statistics-based','tuning machine'])
LongMessageChain = csv.writer(file('result100\\LongMessageChain.csv','wb'))
LongMessageChain.writerow(['subject','file','lineno','LMC','experience-based','statistics-based','tuning machine'])
MultiplyNestedContainer = csv.writer(file('result100\\MultiplyNestedContainer.csv','wb'))
MultiplyNestedContainer.writerow(['subject','file','lineno','LEC','DNC','NCT','experience-based','statistics-based','tuning machine'])

for subjectName in subjects:
	sourcedir = subject_dir + '\\'+ subjectName
	counts = {'LongParameterList':[0,0,0],'LongMethod':[0,0,0],'LongScopeChaining':[0,0,0],
	'LongBaseClassList':[0,0,0],'LargeClass':[0,0,0],'LongMessageChain':[0,0,0],
	'LongLambdaFunction':[0,0,0],'LongTernaryConditionalExpression':[0,0,0],
	'ComplexContainerComprehension':[0,0,0],'MultiplyNestedContainer':[0,0,0]}
	if not os.path.isdir('result100\\%s' %subjectName):
		os.mkdir('result100\\%s' %subjectName)
	mylog = open('result100\\%s\\count.txt' %subjectName,mode='wb+')

	for currentFileName in util.walkDirectory(sourcedir):
		try:
			astContent = customast.parse_file(currentFileName)
		except:
			print sourcedir,currentFileName
			continue
		myast = astChecker.MyAst()
		myast.fileName = currentFileName
		myast.visit(astContent)
		for item in myast.result:
			if item[0] == 1:
				flag0,flag1,flag2=0,0,0
				if item[3]>=PAR[0]:
					flag0 = 1
					counts['LongParameterList'][0] += 1
				if item[3]>=PAR[1]:
					flag1 = 1
					counts['LongParameterList'][1] += 1
				if item[3]>=PAR[2]:
					flag2 = 1
					counts['LongParameterList'][2] += 1
				LongParameterList.writerow([subjectName,item[1],item[2],item[3],flag0,flag1,flag2])
			elif item[0] == 2:
				flag0,flag1,flag2=0,0,0
				if item[3]>=MLOC[0]:
					flag0 = 1
					counts['LongMethod'][0] += 1
				if item[3]>=MLOC[1]:
					flag1 = 1
					counts['LongMethod'][1] += 1
				if item[3]>=MLOC[2]:
					flag2 = 1
					counts['LongMethod'][2] += 1
				LongMethod.writerow([subjectName,item[1],item[2],item[3],flag0,flag1,flag2])
			elif item[0] == 3:
				flag0,flag1,flag2=0,0,0
				if item[3]>=DOC[0]:
					flag0 = 1
					counts['LongScopeChaining'][0] += 1
				if item[3]>=DOC[1]:
					flag1 = 1
					counts['LongScopeChaining'][1] += 1
				if item[3]>=DOC[2]:
					flag2 = 1
					counts['LongScopeChaining'][2] += 1
				LongScopeChaining.writerow([subjectName,item[1],item[2],item[3],flag0,flag1,flag2])
			elif item[0] == 4:
				flag0,flag1,flag2=0,0,0
				if item[3]>=NBC[0]:
					flag0 = 1
					counts['LongBaseClassList'][0] += 1
				if item[3]>=NBC[1]:
					flag1 = 1
					counts['LongBaseClassList'][1] += 1
				if item[3]>=NBC[2]:
					flag2 = 1
					counts['LongBaseClassList'][2] += 1
				LongBaseClassList.writerow([subjectName,item[1],item[2],item[3],flag0,flag1,flag2])
			elif item[0] == 5:
				flag0,flag1,flag2=0,0,0
				if item[3]>=CLOC[0]:
					flag0 = 1
					counts['LargeClass'][0] += 1
				if item[3]>=CLOC[1]:
					flag1 = 1
					counts['LargeClass'][1] += 1
				if item[3]>=CLOC[2]:
					flag2 = 1
					counts['LargeClass'][2] += 1
				LargeClass.writerow([subjectName,item[1],item[2],item[3],flag0,flag1,flag2])
			elif item[0] == 6:
				flag0,flag1,flag2=0,0,0
				if len(item)==4:
					if item[3]>=LEC[0]:
						flag0 = 1
						counts['MultiplyNestedContainer'][0] += 1
					if item[3]>=LEC[1]:
						flag1 = 1
						counts['MultiplyNestedContainer'][1] += 1
					if item[3]>=LEC[2]:
						flag2 = 1
						counts['MultiplyNestedContainer'][2] += 1
					MultiplyNestedContainer.writerow([subjectName,item[1],item[2],item[3],'','',flag0,flag1,flag2])
				else:
					if item[3]>=DNC[0] and item[4]>=NCT[0]:
						flag0 = 1
						counts['MultiplyNestedContainer'][0] += 1
					if item[3]>=DNC[1] and item[4]>=NCT[1]:
						flag1 = 1
						counts['MultiplyNestedContainer'][1] += 1
					if item[3]>=DNC[2] and item[4]>=NCT[2]:
						flag2 = 1
						counts['MultiplyNestedContainer'][2] += 1
					MultiplyNestedContainer.writerow([subjectName,item[1],item[2],'',item[3],item[4],flag0,flag1,flag2])
			elif item[0] == 9:
				flag0,flag1,flag2=0,0,0
				if item[3]>=NOC[0] and (item[4]>=LPAR[0] or item[5]>=NOO[0]):
					flag0 = 1
					counts['LongLambdaFunction'][0] += 1
				if item[3]>=NOC[1] and (item[4]>=LPAR[1] or item[5]>=NOO[1]):
					flag1 = 1
					counts['LongLambdaFunction'][1] += 1
				if item[3]>=NOC[2] and (item[4]>=LPAR[2] or item[5]>=NOO[2]):
					flag2 = 1
					counts['LongLambdaFunction'][2] += 1
				LongLambdaFunction.writerow([subjectName,item[1],item[2],item[3],item[4],item[5],flag0,flag1,flag2])
			elif item[0] == 10:
				flag0,flag1,flag2=0,0,0
				if item[3]>=TNOC[0] or item[4]>=TNOL[0]:
					flag0 = 1
					counts['LongTernaryConditionalExpression'][0] += 1
				if item[3]>=TNOC[1] or item[4]>=TNOL[1]:
					flag1 = 1
					counts['LongTernaryConditionalExpression'][1] += 1
				if item[3]>=TNOC[2] or item[4]>=TNOL[2]:
					flag2 = 1
					counts['LongTernaryConditionalExpression'][2] += 1
				LongTernaryConditionalExpression.writerow([subjectName,item[1],item[2],item[3],item[4],flag0,flag1,flag2])
			elif item[0] == 11:
				flag0,flag1,flag2=0,0,0
				if (item[3]>=CNOC[0] and item[5]>=CNOO[0]) or item[4]>=NOFF[0]:
					flag0 = 1
					counts['ComplexContainerComprehension'][0] += 1
				if (item[3]>=CNOC[1] and item[5]>=CNOO[1]) or item[4]>=NOFF[1]:
					flag1 = 1
					counts['ComplexContainerComprehension'][1] += 1
				if (item[3]>=CNOC[2] and item[5]>=CNOO[2]) or item[4]>=NOFF[2]:
					flag2 = 1
					counts['ComplexContainerComprehension'][2] += 1
				ComplexContainerComprehension.writerow([subjectName,item[1],item[2],item[3],item[4],item[5],flag0,flag1,flag2])
			elif item[0] == 13:
				flag0,flag1,flag2=0,0,0
				if item[3]>=LMC[0]:
					flag0 = 1
					counts['LongMessageChain'][0] += 1
				if item[3]>=LMC[1]:
					flag1 = 1
					counts['LongMessageChain'][1] += 1
				if item[3]>=LMC[2]:
					flag2 = 1
					counts['LongMessageChain'][2] += 1
				LongMessageChain.writerow([subjectName,item[1],item[2],item[3],flag0,flag1,flag2])

	total = [0,0,0]
	for k,v in counts.items():
		total[0] += v[0]
		total[1] += v[1]
		total[2] += v[2]
	if total[0]==0 or total[1]==0 or total[2]==0:
		myportion.write('%s\r\n' %subjectName)
	for k,v in counts.items():
		mylog.write("%s %d %d %d\r\n" %(k,v[0],v[1],v[2]))
		if k in portion.keys():
			portion[k].append([v[0]/total[0] if total[0]!=0 else 0,
				v[1]/total[1] if total[1]!=0 else 0,
				v[2]/total[2] if total[2]!=0 else 0])
		else:
			portion[k] = [[v[0]/total[0] if total[0]!=0 else 0,
			v[1]/total[1] if total[1]!=0 else 0,
			v[2]/total[2] if total[2]!=0 else 0],]
	mylog.write("total %d %d %d\r\n" %(total[0],total[1],total[2]))
	mylog.close()

smellnames = ["LongParameterList", "LongMethod", "LongScopeChaining", 
	 "LargeClass","LongMessageChain", "LongBaseClassList",
	"LongLambdaFunction", "LongTernaryConditionalExpression",
	"ComplexContainerComprehension", "MultiplyNestedContainer"]

for s in smellnames:
	myportion.write('c(\r\n')
	for values in portion[s]:
		if values==portion[s][-1]:
			myportion.write('%.2f,%.2f,%.2f' %(values[0],values[1],values[2]))
		else:
			myportion.write('%.2f,%.2f,%.2f,\r\n' %(values[0],values[1],values[2]))
	if s=='MultiplyNestedContainer':
		myportion.write(')\r\n')
	else:
		myportion.write('),\r\n')
myportion.close()
