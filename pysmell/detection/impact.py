import astChecker
import csv
import os
import time
import subprocess
import customast
import ast
import datetime
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

# smells = {'LongParameterList':[PAR],'LongMethod':[MLOC],'LongScopeChaining':[DOC],'LongBaseClassList':[NBC],
# 'LargeClass':[CLOC],'LongMessageChain':[LMC], 'ComplexLambdaExpression':[NOC,LPAR,NOO],
# 'LongTernaryConditionalExpression':[TNOC,TNOL], 'ComplexContainerComprehension':[CNOC,NOFF,CNOO],
# 'MultiplyNestedContainer':[LEC,DNC,NCT] }

smells = ['LongParameterList','LongMethod',	'LongScopeChaining','LongBaseClassList','LargeClass','LongMessageChain',
'ComplexLambdaExpression',	'LongTernaryConditionalExpression','ComplexContainerComprehension','MultiplyNestedContainer']

subject_visions = {
'django':['1.2','1.2.2','1.3','1.3.1','1.4','1.3.3','1.3.5','1.4.5','1.6a1','1.4.6','1.6','1.6.2','1.6.5','1.7','1.7.4','1.8.2'],
'numpy':['v1.0','v1.0.3','v1.1.0','v1.2.0','v1.3.0','v1.4.0','v1.5.0','v1.6.0','v1.6.2','v1.7.0','v1.8.0','v1.9.0','v1.9.2'],
'ipython':['rel-0.10.1','rel-0.10.2','rel-0.11','rel-0.12','rel-0.12.1','rel-0.13.1','rel-0.13.2','rel-1.1.0','rel-1.2.0','rel-2.1.0','rel-2.3.1','rel-3.1.0'],
'boto':['2.1.0','2.2.0','2.4.0','2.6.0','2.8.0','2.9.5','2.13.0','2.21.2','2.27.0','2.30.0','2.33.0','2.35.0','2.38.0'],
'tornado':['v1.2.1','v2.1.0','v2.2.0','v2.3.0','v2.4.1','v3.0.1','v3.1.1','v3.2.0','v3.2.1','v4.0.2','v4.1.0','v4.2.0'],
'matplotlib':['v1.0.0','v1.0.1','v1.1.0','v1.1.1','v1.2.0rc3','v1.2.1','v1.3.0rc4','v1.3.1','v1.4.0rc1','v1.4.2','v1.4.3'],
'scipy':['v0.5.0','v0.6.0','v0.7.0','v0.8.0','v0.9.0','v0.10.0','v0.11.0','v0.12.0','v0.13.0','v0.14.0','v0.15.0','v0.16.0b2'],
'nltk':['2.0.1rc1','2.0.1rc3','2.0.3','3.0a1','3.0a4','3.0.0','3.0.2'], 
'ansible':['v1.2.2','v1.4.0','v1.5.0','v1.6.0','v1.7.0','v1.8.0','v1.8.4','v1.9.2-0.1.rc1']
}

# strategies = ['experience-based','statistics-based','tuning machine']

def walkDirectory(rootdir):
	sourcedirs = set()
	for root, dirs, files in os.walk(rootdir):
		for name in files:
			if (os.path.splitext(name)[1][1:] == 'py'):
				sourcedirs.add(os.path.join(root,name)[(len(rootdir)+1):].replace("\\", "/"))
	return sourcedirs

def changegittag(directory,tag):
  os.chdir(directory)
  p = subprocess.Popen('git checkout '+tag,shell=True,stdout=subprocess.PIPE)

for (subject,versions) in subject_visions.items():
	if not os.path.isdir('impact\\%s' %subject):
		os.mkdir('impact\\%s' %subject)

	tagtime = {} #version:time
	tagfile = csv.reader(file(subject_dir+subject+'\\tags_info.csv','rb')) 
	for line in tagfile:
		if tagfile.line_num == 1:
			continue
		v = line[1]
		t = line[3]
		if v in versions:
			tagtime[v] = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')


	for i in range(len(versions)-1):
		tag = versions[i]

		e_writer = csv.writer(file('impact\\%s\\%s_experience-based.csv' %(subject,tag),'wb'))
		s_writer = csv.writer(file('impact\\%s\\%s_statistics-based.csv' %(subject,tag),'wb'))
		t_writer = csv.writer(file('impact\\%s\\%s_tuning-machine.csv' %(subject,tag),'wb'))
		e_writer.writerow(['tag','file']+smells+['LOC','change','fault'])
		s_writer.writerow(['tag','file']+smells+['LOC','change','fault'])
		t_writer.writerow(['tag','file']+smells+['LOC','change','fault'])

		nexttagtime = tagtime[versions[i+1]]
		sourcedir = subject_dir+subject+'\\'+subject
		changegittag(sourcedir,tag)
		time.sleep(3)

		#change {filename:count}
		change_info = {}
		changenum = csv.reader(file(subject_dir+subject+'\\change_log.csv','rb'))	
		for line in changenum:
			if changenum.line_num == 1:
				continue
			if len(line[2])==0:
				continue
			else:
				currenttime = datetime.datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S')
			if tagtime[tag] >= currenttime or nexttagtime < currenttime:
				continue
			elif currenttime > tagtime[tag] and currenttime<=nexttagtime and len(line)==5:
				if line[4] in change_info.keys():
					change_info[line[4]] = change_info[line[4]] + 1
				else:
					change_info[line[4]] = 1

		#fault {filename:count}
		fault_info = {}
		faultnum = csv.reader(file(subject_dir+subject+'\\fault_log.csv','rb'))
		for line in faultnum:
			if faultnum.line_num == 1:
				continue
			currenttime = datetime.datetime.strptime(line[2], '%Y-%m-%d %H:%M:%S')
			if tagtime[tag] >= currenttime or nexttagtime < currenttime:
				continue
			elif currenttime > tagtime[tag] and currenttime<=nexttagtime and len(line)==6:
				if line[5] in fault_info.keys():
					fault_info[line[5]] = fault_info[line[5]] + 1
				else:
					fault_info[line[5]] = 1

		for currentFileName in walkDirectory(sourcedir):
			try:
				astContent = customast.parse_file(currentFileName)
			except:
				print subject,tag,currentFileName
				continue
			lines = set()
			for n in ast.walk(astContent):
				if hasattr(n,'lineno'):
					lines.add(n.lineno)

			if currentFileName in change_info.keys():
				change_count = change_info[currentFileName]
			else:
				change_count = 0

			if currentFileName in fault_info.keys():
				fault_count = fault_info[currentFileName]
			else:
				fault_count = 0

			myast = astChecker.MyAst()
			myast.fileName = currentFileName
			myast.visit(astContent)
			e_counts = [0,0,0,0,0,0,0,0,0,0]
			s_counts = [0,0,0,0,0,0,0,0,0,0]
			t_counts = [0,0,0,0,0,0,0,0,0,0]
			for item in myast.result:
				if item[0] == 1:
					if item[3] >= PAR[0]:
						e_counts[0] = e_counts[0]+1
					if item[3] >= PAR[1]:
						s_counts[0] = s_counts[0]+1
					if item[3] >= PAR[2]:
						t_counts[0] = t_counts[0]+1
				elif item[0] == 2:
					if item[3] >= MLOC[0]:
						e_counts[1] = e_counts[1]+1
					if item[3] >= MLOC[1]:
						s_counts[1] = s_counts[1]+1
					if item[3] >= MLOC[2]:
						t_counts[1] = t_counts[1]+1
				elif item[0] == 3:
					if item[3] >= DOC[0]:
						e_counts[2] = e_counts[2]+1
					if item[3] >= DOC[1]:
						s_counts[2] = s_counts[2]+1
					if item[3] >= DOC[2]:
						t_counts[2] = t_counts[2]+1
				elif item[0] == 4:
					if item[3] >= NBC[0]:
						e_counts[3] = e_counts[3]+1
					if item[3] >= NBC[1]:
						s_counts[3] = s_counts[3]+1
					if item[3] >= NBC[2]:
						t_counts[3] = t_counts[3]+1
				elif item[0] == 5:
					if item[3] >= CLOC[0]:
						e_counts[4] = e_counts[4]+1
					if item[3] >= CLOC[1]:
						s_counts[4] = s_counts[4]+1
					if item[3] >= CLOC[2]:
						t_counts[4] = t_counts[4]+1
				elif item[0] == 6:
					if len(item)==4:
						if item[3] >= LEC[0]:
							e_counts[9] = e_counts[9]+1
						if item[3] >= LEC[1]:
							s_counts[9] = s_counts[9]+1
						if item[3] >= LEC[2]:
							t_counts[9] = t_counts[9]+1
					else:
						if item[3]>=DNC[0] and item[4]>=NCT[0]:
							e_counts[9] = e_counts[9]+1
						if item[3]>=DNC[1] and item[4]>=NCT[1]:
							s_counts[9] = s_counts[9]+1
						if item[3]>=DNC[2] and item[4]>=NCT[2]:
							t_counts[9] = t_counts[9]+1
				elif item[0] == 9:
					if item[3]>=NOC[0] and (item[4]>=LPAR[0] or item[5]>=NOO[0]):
						e_counts[6] = e_counts[6]+1
					if item[3]>=NOC[1] and (item[4]>=LPAR[1] or item[5]>=NOO[1]):
						s_counts[6] = s_counts[6]+1
					if item[3]>=NOC[2] and (item[4]>=LPAR[2] or item[5]>=NOO[2]):
						t_counts[6] = t_counts[6]+1
				elif item[0] == 10:
					if item[3]>=TNOC[0] or item[4]>=TNOL[0]:
						e_counts[7] = e_counts[7]+1
					if item[3]>=TNOC[1] or item[4]>=TNOL[1]:
						s_counts[7] = s_counts[7]+1
					if item[3]>=TNOC[2] or item[4]>=TNOL[2]:
						t_counts[7] = t_counts[7]+1
				elif item[0] == 11:
					if (item[3]>=CNOC[0] and item[5]>=CNOO[0]) or item[4]>=NOFF[0]:
						e_counts[8] = e_counts[8]+1
					if (item[3]>=CNOC[1] and item[5]>=CNOO[1]) or item[4]>=NOFF[1]:
						s_counts[8] = s_counts[8]+1
					if (item[3]>=CNOC[2] and item[5]>=CNOO[2]) or item[4]>=NOFF[2]:
						t_counts[8] = t_counts[8]+1
				elif item[0] == 13:
					if item[3] >= LMC[0]:
						e_counts[5] = e_counts[5]+1
					if item[3] >= LMC[1]:
						s_counts[5] = s_counts[5]+1
					if item[3] >= LMC[2]:
						t_counts[5] = t_counts[5]+1
			e_writer.writerow([tag,currentFileName]+e_counts+[len(lines),change_count,fault_count])
			s_writer.writerow([tag,currentFileName]+s_counts+[len(lines),change_count,fault_count])
			t_writer.writerow([tag,currentFileName]+t_counts+[len(lines),change_count,fault_count])

