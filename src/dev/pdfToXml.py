import os

c=os.popen('ls *.pdf').read()

os.system('rm *.xml')

splitted = c.split("\n")

for item in splitted[0:len(splitted)-1]:
	
	string=item.split(".")[0]

	rst="pdftohtml -xml -i "+"\""+item+"\" \""+string+".xml\""
	os.system(rst)
