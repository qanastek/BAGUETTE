import os

c=os.popen('ls *.pdf').read()

os.system('rm *.html')

splitted = c.split("\n")

for item in splitted[0:len(splitted)-1]:
	name = item.split(".")[0]
	query = "pdf2txt -t html -o %s.html %s.pdf" % (name,name)
	os.system(query)