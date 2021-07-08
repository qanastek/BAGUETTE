# coding: utf8
from bs4 import BeautifulSoup
import re
import os
from io import open

file = "Alexandrov_2015_A_Modified_Tripartite_Model_for_Document_Representation_in_Internet_Sociology.html"

data=open(file,"r",encoding='utf8')

def getAuthors(data):

	soup = BeautifulSoup(data, "html.parser")

	font_spans = soup.find_all("span", attrs={"style":re.compile("font-size:1[1-3]px")})
	rslt = ""

	if(font_spans != [] ):
		rslt = font_spans[0].text + font_spans[1].text + font_spans[2].text
	else:
		for r in soup.find_all("span")[3:6] :
			rslt += r.text
			
	return str(rslt)

print(getAuthors(data))