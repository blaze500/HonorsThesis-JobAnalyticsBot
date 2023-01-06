import time
from selenium.webdriver.common.by import By
import os
import csv
import html2text

class JobTextGrabber:

    #Starts the Program
    def __init__(self, seleniumDriver, directoryNames):
        self.seleniumDriver = seleniumDriver
        self.directoryNames = directoryNames
        #directoryNames = ["HandshakeJobText", "IndeedJobText", "LinkedinJobText"]
        for fileName in self.directoryNames:
            if not os.path.exists(fileName + "Text"):
                os.mkdir(fileName + "Text")


        #for file in os.scandir(path):
        #    os.remove(file.path)


    def getHandshakeJobText(self, csvName):
        reader = csv.reader(open(csvName + '.csv', 'rt'), delimiter=',')
        jobTextNumber = 0
        for row in reader:
            self.seleniumDriver.get(row[0])
            time.sleep(3)

            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "style__formatted___qRoxk")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                self.writeToTxt(self.directoryNames[0] + 'Text', str(jobTextNumber), jobDescriptionText)
                jobTextNumber += 1
            except:
                print("This link caused a problem in the getHandshakeJobText method: " + row[0])


    def getIndeedJobText(self, csvName):
        reader = csv.reader(open(csvName + '.csv', 'rt'), delimiter=',')
        jobTextNumber = 0
        for row in reader:
            self.seleniumDriver.get(row[0])
            time.sleep(3)

            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.ID, "jobDescriptionText")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                self.writeToTxt(self.directoryNames[1] + 'Text', str(jobTextNumber), jobDescriptionText)
                jobTextNumber += 1
            except:
                print("This link caused a problem in the getIndeedJobText method: " + row[0])

    def getLinkedinJobText(self, csvName):
        reader = csv.reader(open(csvName + '.csv', 'rt'), delimiter=',')
        jobTextNumber = 0
        for row in reader:
            goToNext = False

            self.seleniumDriver.get(row[0])
            time.sleep(3)

            try:
                jobDescriptionTextHTML = self.seleniumDriver.find_element(By.ID, "job-details")
                jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                self.writeToTxt(self.directoryNames[2] + 'Text', str(jobTextNumber), jobDescriptionText)
                jobTextNumber += 1
            except:
                goToNext = True

            if goToNext is True:
                try:
                    jobDescriptionTextHTML = self.seleniumDriver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
                    jobDescriptionText = html2text.html2text(jobDescriptionTextHTML.get_attribute("innerHTML"))
                    self.writeToTxt(self.directoryNames[2] + 'Text', str(jobTextNumber), jobDescriptionText)
                    jobTextNumber += 1
                except:
                    print("This link caused a problem in the getLinkedinJobText method: " + row[0])


    def writeToTxt(self, fileName, fileNumber, jobDescriptionText):
        txtFile = open(fileName + '/' + fileName + fileNumber + '.txt', 'w', encoding="utf-8")
        txtFile.write(jobDescriptionText)
        txtFile.close()