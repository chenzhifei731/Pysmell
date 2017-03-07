import csv

PAR = range(2,6)
MLOC = range(9,56)
DOC = (2,3,4)
NBC = (1,2,3)
CLOC = range(7,79)
LMC = (2,3,4,5)
NOC,LPAR,NOO = range(37,116),range(0,6),range(4,27)
TNOC,TNOL = range(53,119),(1,2,3)
CNOC,NOFF,CNOO = range(56,165),(1,2,3),range(9,35)
LEC,DNC,NCT = (1,2,3),range(3,7),(1,2,3)

result = open('example repository\\manual inspection\\ComplexContainerComprehension.txt',mode='wb+')
mincount = 300
for t1 in CNOC:
	for t2 in NOFF:
		for t3 in CNOO:
			fp = 0
			fn = 0
			erfile = csv.reader(open("example repository\\manual inspection\\ComplexContainerComprehension.csv"))
			for item in erfile:
				if erfile.line_num == 1:
					continue;
				if (int(item[4])>=t1 and int(item[6])>=t3) or int(item[5])>=t2:
					if int(item[-1])==0:
						fn = fn+1
				else:
					if int(item[-1])==1:
						fp = fp+1
			result.write("CNOC:%d NOFF:%d CNOO:%d FP:%d FN:%d TOTAL:%d \r\n" %(t1,t2,t3,fp,fn,fp+fn))
			if fp+fn <= mincount:
				mincount = fp+fn
print mincount