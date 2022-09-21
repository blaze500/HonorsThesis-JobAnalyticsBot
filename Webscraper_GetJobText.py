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

class JobTextGrabber:

    #Starts the Program
    def __init__(self, seleniumDriver):
        self.seleniumDriver = seleniumDriver
        directoryNames = ["HandshakeJobText", "IndeedJobText", "LinkedinJobText"]
        for fileName in directoryNames:
            if not os.path.exists(fileName):
                os.mkdir(fileName)

        #for file in os.scandir(path):
        #    os.remove(file.path)


    def getHandshakeJobText(self):
        reader = csv.reader(open('HandshakeJobs.csv', 'rt'), delimiter=',')
        jobTextNumber = 0
        for row in reader:
            self.seleniumDriver.get(row[0])
            time.sleep(3)
            jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "style__margin-control___1oseO")
            jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
            self.writeToTxt('HandshakeJobText', str(jobTextNumber), jobDescriptionText)
            jobTextNumber += 1


    def getIndeedJobText(self):
        reader = csv.reader(open('IndeedJobs.csv', 'rt'), delimiter=',')
        jobTextNumber = 0
        for row in reader:
            self.seleniumDriver.get(row[0])
            time.sleep(3)
            jobDescriptionTextHTML = self.seleniumDriver.find_element(By.ID, "jobDescriptionText")
            jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
            self.writeToTxt('IndeedJobText', str(jobTextNumber), jobDescriptionText)
            jobTextNumber += 1

    def getLinkedinJobText(self):
        reader = csv.reader(open('LinkedinJobs.csv', 'rt'), delimiter=',')
        jobTextNumber = 0
        for row in reader:
            self.seleniumDriver.get(row[0])
            time.sleep(3)
            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.ID, "job-details")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                self.writeToTxt('LinkedinJobText' + str(jobTextNumber), jobDescriptionText)
            except:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                self.writeToTxt('LinkedinJobText', str(jobTextNumber), jobDescriptionText)
            jobTextNumber += 1

    def writeToTxt(self, fileName, fileNumber, jobDescriptionText):
        txtFile = open(fileName + '/' + fileName + fileNumber + '.txt', 'w', encoding="utf-8")
        txtFile.write(jobDescriptionText)
        txtFile.close()