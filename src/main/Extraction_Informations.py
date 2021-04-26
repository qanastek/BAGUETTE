# -*- coding: utf-8 -*-

import time
import re
import os
import sys
from collections import Counter

from wordcloud import WordCloud

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

stopwords = []

# reload(sys)
# sys.setdefaultencoding('utf-8')
# sys.path.append("/usr/bin/pdf2txt")

from xml.etree.ElementTree import Element, SubElement, Comment, tostring

mostCommonWords = Counter()

if len(sys.argv) != 2:
	sys.exit("Erreur argument manquant !")

def displayWordsCloud():

	global mostCommonWords

	print(list(mostCommonWords))

	mostCommonKeys = [key for key, _ in mostCommonWords.most_common(45)]
	
	# Before => " ".join(list(mostCommonWords))
	wordcloud = WordCloud(width = 800, height = 800,
					background_color ='white',
					min_font_size = 10).generate(" ".join(mostCommonKeys))
	
	# plot the WordCloud image                       
	plt.figure(figsize = (8, 8), facecolor = None)
	plt.imshow(wordcloud)
	plt.axis("off")
	plt.tight_layout(pad = 0)
	
	plt.show()

def loadStopwords():

	stopFileName = "/mnt/d/Projects/LIA/LIA-Words-Cloud/Parseur-PDF/stopswords/biggest_stopwords_ever.txt"

	with open(stopFileName) as f:

		content = f.readlines()

		for line in content:

			stopwords.append(
				line
				.replace(" ","")
				.replace("\t","")
				.replace("\n","")
				.replace("\r","")
			)
	
	# f = open("biggest_stopwords_ever.txt", "w")
	# content = list(set(stopwords))
	# [f.write(c + "\n") for c in content]
	# f.close()

def convertPdfToTxt(name):
    	
	nameRaw = name.split(".")[0]
	rst = "pdftotext -enc UTF-8 '{}' '{}.txt'".format(name,nameRaw)
	os.system(rst)

def convertPdfToHtml(item):

	name = str(item.split(".")[0])

	print("Convert " + name + " to HTML")

	os.system('rm -f {}.html'.format(name))

	query = "pdf2txt.py -t html -o {}.html {}.pdf".format(name,name)
	os.system(query)

def getResume(data):

	global mostCommonWords

	data = data.lower()
	# print(data)
    	
	splitted = ""

	if re.search("abstract",data):
		splitted = data.split("abstract")[1]

	# Get first paragraphe
	splitted2 = splitted.split("\n\n")[0]

	# Cut after Keywords
	splitted2 = splitted2.split("keywords")[0]

	# Replace jump line by spaces
	splitted2 = splitted2.replace("\n"," ")

	# Delete characters which aren't Alpha and Space
	splitted2 = re.sub('[^a-zA-Z ]+', '', splitted2[:5]) + splitted2[5:]

	technicalWords = [a for a in splitted2.split(" ") if a not in stopwords]
	technicalWords = Counter(technicalWords)

	# print(technicalWords)
	# print("\n")

	mostCommonWords = mostCommonWords + technicalWords
	# print(mostCommonWords)

	return splitted2

def getTitle(txtFile, title):
    
	data = open(title + ".html","r")
	# print("getTitle for " + nameFile + ".html")
	soup = BeautifulSoup(data, "html.parser")

	spans = soup.find_all("span")
	highestItem = []
	highestSize = 0
	fontSize = 0
	content = ""
	
	if len(spans) <= 0:
		return "No title found"
	else:
		for span in spans:
      
			s = str(span["style"])
			start = "font-size:"
			end = "px;"
			if s.find(start) >= 0:
				fontSize = s[s.find(start)+len(start):s.rfind(end)-1]
				# print("style : ")
				fontSize = int(fontSize)
				content = span.text
				# print(content + " : " + str(fontSize))
				# print("-----")

				if (fontSize >= 10 and fontSize <= 35 and len(content) > 8):
					highestItem.append((fontSize,content));

		if len(highestItem) > 0:
			highestItem.sort(key=lambda x: x[0], reverse=True)
		
			noDuplicated = list(set(highestItem))
			highestSize = highestItem[0][0]
			res = ""
		
			for elem in noDuplicated:
				if elem[0] == highestSize:
					res += elem[1]
		
			res = res.replace('\n', ' ')
			if res.find('(cid:') >= 0:
				res = txtFile.split("\n")[0] 
			print("----------------" + res)
			return res
   
	return "Empty"

def getReferences(data):
    
	if re.search("References\n",data):
		if re.search("So far, we only",data):
			rslt = data.split("References\n")[2]
		else:
			rslt = data.split("References\n")[1]

	elif re.search("REFERENCES",data):
		rslt = data.split("REFERENCES")[1]
		if re.search("IEEE TRANSACTIONS",rslt):
			rslt = rslt.split("IEEE TRANSACTIONS")[0]
	# Get each line of the page
	page = rslt.split("\n")

	for line in page:

		if line == "\n" or len(line) <= 15 or re.match("^[\[\]0-9\.\ \|]+$",line) or re.match("",line):
			# print(line)
			page.remove(line)

	# .split("\n\n")[0]
	return "\n".join(page)

def getAuthors(data):
	data = open(data + ".html","r")
	soup = BeautifulSoup(data, "html.parser")

	font_spans = soup.find_all("span", attrs={"style":re.compile("font-size:1[1-3]px")})
	rslt = ""

	if(font_spans != [] ):
		for i in range(len(font_spans)):
			# print(font_spans[i].text)
			rslt+= font_spans[i].text
		# rslt = font_spans[0].text + font_spans[1].text + font_spans[2].text
		# print("1: " + str(rslt))
	else:
		for r in soup.find_all("span")[3:6] :
			rslt += r.text
		# print("2: " + str(rslt))
	rslt=rslt.split('\n')[0]
	# print (rslt)
	return rslt


def getConclusion(data):

	# Get everything after the keyword "Conclusion"
	if re.search("Conclusion",data):
		rslt = data.split('Conclusion')[1]

	elif re.search("CONCLUSION",data):
		rslt = data.split("CONCLUSION")[1]

	else :
		rslt=""	
		return rslt

	if re.search("Acknowledgments",data):
		rslt = rslt.split("Acknowledgments")[0]

	elif re.search("ACKNOWLEDGEMNTS",data):
		rslt = rslt.split("ACKNOWLEDGMENTS")[0]

	if re.search("Acknowledgements",data):
		rslt = rslt.split("Acknowledgements")[0]

	elif re.search("ACKNOWLEDGEMENTS",data):
		rslt = rslt.split("ACKNOWLEDGEMENTS")[0]	

	# Delemit the end
	if re.search("References",data):
		rslt = rslt.split("References")[0]

	elif re.search("REFERENCES",data):
		rslt = rslt.split("REFERENCES")[0]

	# Get each line of the page
	conclu = rslt.split("\n")
	# print(conclu)

	i=0
	if (conclu!=[]):
		for line in conclu:
			if i==0 and not(re.match("([A-Z])\w+",line)):
				del conclu[i]
			if line == "\n" or len(line) <= 15 or re.match("^[\[\]0-9\.\ \|]+$",line) or re.match("^[0-9]+$",line) or re.search(".0x0c.",line):
				del conclu[i]
			i+=1
		# print(line)	
	return "\n".join(conclu)	

def getIntroduction(data):
	
	splitted = ""

	if re.search("Introduction",data):
		splitted = data.split("Introduction")[1]
	elif re.search("INTRODUCTION",data):
		splitted = data.split("INTRODUCTION")[1]
		
	if re.search("\nII",data):
		splitted = splitted.split("II")[0]
	# if re.search("\n2.",data):
	# 	splitted = splitted.split("\n2.")[0]
	if re.search("2\n\n",data):
		splitted = splitted.split("2\n\n")[0]	
	if re.search("\n\n2",data):
		splitted = splitted.split("\n\n2")[0]
		

	intro = splitted.split("\n")

	i=0
	for line in intro:
		if i==0 and not(re.match("([A-Z])\w+",line)):
			del intro[i]
		if line == "\n" or re.match("^[\[\]0-9\.\ \|]+$",line) or re.match("^[0-9]+$",line) or re.search(".0x0c.",line):
			del intro[i]
		i+=1
		# print(line)
	
	return "\n".join(intro)

def getDiscution(data):

	if re.search("Discussion\n",data):

		rslt = data.split('Discussion\n')[1]

	elif re.search("DISCUSSION",data):

		rslt = data.split("DISCUSSION")[1]

	elif re.search("Discussion:",data):

		rslt = data.split("Discussion:")[1]

	else:
		return ""

	if re.search("Conclusion",rslt):
		rslt = rslt.split("Conclusion")[0]

	elif re.search("CONCLUSION",rslt):
		rslt = rslt.split("CONCLUSION")[0]

	# Get each line of the page
	page = rslt.split("\n")


	for line in page:

		if line == "\n" or len(line) <= 15 or re.match("^[\[\]0-9\.\ \|]+$",line):
			# print(line)
			page.remove(line)

	# .split("\n\n")[0]
	return "\n".join(page)

def getCorps(data):
	start = 'introduction\n'
	s = data
	s = s[s.lower().find(start) + len(start):s.lower().rfind('conclusion')]

	if len(s) <= 10:
		s = s[s.lower().rfind(start) + len(start):s.lower().rfind('references\n')]
	return s

def showChoices(ls):

	id = 0
	for item in ls[:-1]:
		print("[{}] {}".format(str(id),item))
		id += 1

	print("Veuillez saisir la liste des documents:")

	choices = str(input())
	choices = np.array(choices.split(","))

	rslt = []
	
	# For each index selected
	for choice in choices.astype(int):

		# If he enter a bad index
		if (choice < len(ls) - 1):
			rslt.append((choice, ls[choice]))
		elif (choice > len(ls) - 1):
			print("Document inexistant !")
			return showChoices(ls)
			
	return rslt

os.system("rm -f *.txt")
os.system("rm -f *.xml")

# Delete spaces in files names
os.system("""
for file in *.pdf; do mv "$file" "$(echo $file | sed 's/ /_/g')"; done
""")

# List all the PDF available
ls = "ls *.pdf"
c = os.popen(ls).read()

loadStopwords()

splitted = c.split("\n")

# Read the args
if sys.argv[1] == "-t":
    out='txt'
elif sys.argv[1] == "-x":
    out='xml'
else:
    print("argument incorrect") 

# For each selected files
for file in showChoices(splitted):

	choice,item = file

	# Convert each PDF to TXT
	convertPdfToTxt(item)

	# Cut the extension and keep the name only
	nameFile = item.split(".")[0]

	try:

		# Open the converted PDF
		with open(nameFile + ".txt", 'r') as f:

			convertPdfToHtml(item)

			data = f.read()
			# data = f.read().decode('utf-8')

			# Documents Informations

			fileName = nameFile

			title = getTitle(data, nameFile)

			author = getAuthors(nameFile)

			resume = getResume(data)

			bibliographie = getReferences(data)

			conclusion = getConclusion(data)

			introduction = getIntroduction(data)
			# introduction = "rien"

			discution = getDiscution(data)

			corps = getCorps(data)

			# If the user want to export as TXT
			if out == "txt":
					
				# Create the output file
				os.system('touch resultat.txt')

				# Write informations inside the file
				with open("resultat.txt", 'a') as res:
					# res.write("\n")
					res.write("File name: " + str(fileName) + "\n")
					# res.write("\n\n")
					# res.write("Authors: " + str(author))
					# res.write("\n\n")
					res.write("Title: " + str(title) + "\n\n")
					# res.write("\n\n")
					res.write("" + str(resume))
					res.write("\n\n")
					# res.write("Introduction: " + str(introduction))
					# res.write("\n\n")
					# res.write("Corps:" + str(corps))
					# res.write("\n\n")
					# res.write("Discution: " + str(discution))
					# res.write("\n\n")
					# res.write("Conclusion: \n" + str(conclusion))
					# res.write("\n\n")
					# res.write("Biblio: " + str(bibliographie))
					# res.write("\n\n")
					# res.write("\n\n-------------------------------------------------------------\n")
				res.close()

			# If the user want to export as XML
			elif out == "xml":
					
				root = Element('article')

				preamble = SubElement(root, 'preamble')
				preamble.text = str(fileName)

				titre = SubElement(root, 'titre')
				titre.text = str(title)

				auteur = SubElement(root, 'auteur')
				auteur.text = str(author)

				abstract = SubElement(root, 'abstract')
				abstract.text = str(resume)

				abstract = SubElement(root, 'introduction')
				abstract.text = str(introduction)

				abstract = SubElement(root, 'corps')
				abstract.text = str(corps)

				abstract = SubElement(root, 'conclusion')
				abstract.text = str(conclusion)

				abstract = SubElement(root, 'discussion')
				abstract.text = str(discution)

				biblio = SubElement(root, 'biblio')
				biblio.text = str(bibliographie)

				xml = tostring(root)

				# Create the output file
				os.system('touch resultat.xml')

				# Write the XML object inside
				with open("resultat.xml", 'a') as res:
					res.write(xml)

				res.close()

		f.close()

	except Exception as e:
 		print(nameFile + ".txt n'a pas pu être convertie !")
 		print(e)

os.system("rm -f *.html") if len([o for o in os.listdir('.') if o.endswith('.html')]) > 0 else None

displayWordsCloud()

print("#####################################")
print("####### Conversion réussite ! #######")
print("#####################################")