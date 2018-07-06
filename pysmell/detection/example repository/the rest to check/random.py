import csv

reader = csv.reader(open("LongParameterList.csv"))
writer = csv.writer(file('myLongParameterList.csv','wb'))

for line in reader:
	if reader.line_num%31==0:
		writer.writerow(line[:-1])
