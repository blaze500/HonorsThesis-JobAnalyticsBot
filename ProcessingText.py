import requests
from bs4 import BeautifulSoup
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import csv
import LocationChecker
import Webscraper_GoogleCareers
import Webscraper_Linkedin
import Webscraper_Handshake
import Webscraper_Indeed
import html2text
import nltk
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords.words('english')
import re
from nltk.stem import WordNetLemmatizer

class TextProcessor:

    #Starts the Program
    def __init__(self):

        self.directoryNames = ["HandshakeJobText", "IndeedJobText", "LinkedinJobText"]

        # Years Of Experience (YOE), dictonaries which record the years of ___ found in each text.
        self.YOEDictionaries = {}

        # An array which contains the dictionaries for each job website
        self.SpecialWordDictionaries = {}

        # An array which contains the dictionaries for each job website
        self.WordDictionaries = {}

        for directory in self.directoryNames:
            self.WordDictionaries[directory] = {}

        # An array which contains the arrays of each job website
        self.JobTexts = {}

    def TextFilesToJobTextArrays(self):

        for fileName in self.directoryNames:
            directoryJobTexts=[]
            for textFilePath in os.listdir(fileName):
                with open(os.path.join(fileName, textFilePath), 'r', encoding="utf-8") as jobDescription:
                    jobDescriptionText = jobDescription.read().lower().replace("\n"," ")
                    directoryJobTexts.append(jobDescriptionText)
            self.JobTexts[fileName] = directoryJobTexts

        #print(self.JobTexts)


    def CleaningTextAlgorithm(self):
        for fileName in self.directoryNames:
            for number, text in enumerate(self.JobTexts[fileName]):
                self.JobTexts[fileName][number] = self.cleanText(text)


    def cleanText(self, text):

        textWithoutSpecialCharacters = text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", "", text)

        #print(textWithoutSpecialCharacters)

        everyWordInText = textWithoutSpecialCharacters.split(" ")

        fullyCleanedWords = []
        for word in everyWordInText:
            if word not in stopwords.words('english'):
                fullyCleanedWords.append(word)

        fullyCleanedText = ' '.join(fullyCleanedWords)

        return fullyCleanedText


    def SpecialWordCounterAlgorithm(self):

        for fileName in self.directoryNames:
            for count, jobText in enumerate(self.JobTexts[fileName]):
                self.JobTexts[fileName][count] = self.specialWordFinder(jobText, fileName)

        #print(self.WordDictionaries)



    def WordCounterAlgorithm(self):

        for fileName in self.directoryNames:
            for text in self.JobTexts[fileName]:
                for word in text.split():

                    if word in self.WordDictionaries[fileName]:
                        self.WordDictionaries[fileName][word] += 1
                    else:
                        self.WordDictionaries[fileName][word] = 1

        for fileName in self.directoryNames:
            self.WordDictionaries[fileName] = dict(sorted(self.WordDictionaries[fileName].items(), key=lambda x: x[1], reverse=True))

        #print(self.WordDictionaries)



    def specialWordFinder(self, text, fileName):
        newText=""
        specialWordsFile = open('SpecialWords.txt', 'r', encoding="utf-8")

        # replacing end splitting the text
        # when newline ('\n') is seen.
        specialWords = specialWordsFile.read().splitlines()

        for word in specialWords:
            splitText = text.split(word)
            wordsRemoved = len(splitText)-1
            if wordsRemoved > 0:
                if word in self.WordDictionaries[fileName]:
                    self.WordDictionaries[fileName][word] += wordsRemoved
                else:
                    self.WordDictionaries[fileName][word] = wordsRemoved

            newTextWithWordRemoved = ''.join(splitText)
            newText=newTextWithWordRemoved

        #print(newText)

        specialWordsFile.close()

        return newText