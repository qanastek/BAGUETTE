import os
import re
from collections import Counter

import PyPDF2

import pandas as pd
from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer

class Baguette:

    def __init__(self):
        self.stopwords = self.__loadStopwords()

    def __loadStopwords(self):

        stopwords_ = []

        stopFileName = "/mnt/d/Projects/LIA/LIA-Words-Cloud/Parseur-PDF/stopswords/biggest_stopwords_ever.txt"

        with open(stopFileName) as f:

            content = f.readlines()

            for line in content:

                stopwords_.append(
                    line
                    .replace(" ","")
                    .replace("\t","")
                    .replace("\n","")
                    .replace("\r","")
                )

        print(str(len(stopwords_)) + " tokens loaded!")

        return stopwords_

    def __tokenizer(self, text):
        
        text = text.lower().replace("\n"," ")

        # print(text)

        text = re.sub("([^@|\s]+@[^@]+\.[^@|\s]+)", " ", text)

        text = re.sub("\(", " ( ", text)
        text = re.sub("\)", " ) ", text)
        text = re.sub("\{", " { ", text)
        text = re.sub("\}", " } ", text)
        text = re.sub("\[", " [ ", text)
        text = re.sub("\]", " ] ", text)

        text = re.sub("\+", " + ", text)
        text = re.sub("\,", " , ", text)
        text = re.sub("\;", " ; ", text)
        text = re.sub("\?", " ? ", text)
        text = re.sub("\!", " ! ", text)

        text = re.sub(" \- ","-",text)
        text = re.sub("\."," . ",text)

        text = re.sub("\s+", " ",  text)

        # print("*"*200)
        # print(text)

        return text

    def __getText(self, filePath):

        # Nbr of pages: pdfReader.numPages
            
        pdfFileObj = open(filePath, 'rb')
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        print(str(pdfReader.numPages) + " pages available.")
        pages = []

        for i in range(1,2):
            content = pdfReader.getPage(i).extractText()
            pages.append(content)

        text = " ".join(pages)

        text = self.__tokenizer(text)

        return text
    
    def __getTechnicalWords(self,filePath):
        content = self.__getText(filePath).split(" ")
        technicalWords = [a for a in content if a not in self.stopwords and len(a) > 1]
        return technicalWords

    def process(self, filePath, k=45):

        technicalWords = self.__getTechnicalWords(filePath)

        technicalWords = Counter(technicalWords).most_common(k)
        mostCommonKeys = [key for key, _ in technicalWords]

        return technicalWords

    def __getFilesContents(self,filePath):

        # Check if contains the backslash at the end of the path
        if filePath.endswith('/') == False:
            filePath = filePath + "/"

        files = [f for f in os.listdir() if ".pdf" in f]

        # print("files:")
        # print(files)

        contents = []

        for fileName in files:
            
            currentFilePath = filePath + fileName
            print("Process " + currentFilePath)

            contents.append(
                " ".join(self.__getTechnicalWords(currentFilePath))
            ) 

        return contents

    def tfIdfFromDir(self, filePath, k=45):

        dataset = self.__getFilesContents(filePath)

        tfIdfVectorizer = TfidfVectorizer(use_idf=True)
        tfIdf = tfIdfVectorizer.fit_transform(dataset)
        df = pd.DataFrame(tfIdf[0].T.todense(), index = tfIdfVectorizer.get_feature_names(), columns=["TF-IDF"])
        df = df.sort_values('TF-IDF', ascending=False)

        resTfIdf = df.head(25)

        # print("#"*100)
        # print(resTfIdf)
        # print("#"*100)

        return resTfIdf