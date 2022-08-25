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

class HandshakeJobs:

    def __init__(self, type, field, inPerson, fullTime, salary, location, education, experience, writeTo, seleniumDriver):
        self.type = type
        self.field = field
        self.inPerson = inPerson
        self.fullTime = fullTime
        self.salary = salary
        self.location = location
        self.education = education
        self.experience = experience
        self.writeTo = writeTo
        self.seleniumDriver = seleniumDriver

    def HandshakeLinkMaker(self):

        self.HandshakeJobsLink = "https://www.linkedin.com/jobs/search/?"

        #Was looking for degree type, however, Handshake doesnt offer that as a link option
        """
        if self.education == "associate" or self.education == "bachelor" or self.education == "masters":
            if self.education == "associate":
                self.HandshakeJobsLink += "1"
            elif self.education == "bachelor":
                self.HandshakeJobsLink +="1"
            elif self.education == "masters":
                self.HandshakeJobsLink +="1"
        """

        if self.experience == "entry" or self.experience == "mid" or self.experience == "senior" or self.experience == "":
            self.HandshakeJobsLink += "&f_E="
            if self.experience == "entry":
                self.HandshakeJobsLink += "2"
            elif self.experience == "mid" or "senior":
                self.HandshakeJobsLink +="4"

        if self.fullTime == "full time" or self.fullTime == "part time" or self.fullTime == "both" or self.type == "internship":
            #Because I need to check what gets added to this, I will add this to the end of the link at the end
            timeStartingCode = "&f_JT="
            if self.fullTime == "full time":
                timeStartingCode +="F"
            elif self.fullTime == "part time":
                timeStartingCode +="P"
            elif self.fullTime == "both":
                timeStartingCode +="F%2CP"
            if self.type == "internship":
                if len(timeStartingCode) > 5:
                    timeStartingCode += "%2C"
                timeStartingCode += "I"
            self.HandshakeJobsLink += timeStartingCode

        if self.inPerson == "in person":
            self.HandshakeJobsLink +="&f_WT=1"
        elif self.inPerson == "remote":
            self.HandshakeJobsLink += "&f_WT=2"
        elif self.inPerson == "both":
            self.HandshakeJobsLink += "&f_WT=1%2C2"


        # Made salary an int, as it was a string
        salary = int(self.salary)
        # There is a salary button starting at 40k and it goes up in increments of 20k
        if salary > 39999:
            # Checking to see how much money is left after 40k
            salaryAbove40k = salary-40000
            # This is to remove the extra numbers as it only goes in increments of 20k
            salaryModulus20k = salary % 20000
            # Does math to see if its 40k, 60k, ..., 200k, and puts the appropriate number in the slot (1 being 40k, 2 being 60k, ect)
            above40kInIncsOf20k = int((salaryAbove40k-salaryModulus20k)/20000)
            if above40kInIncsOf20k > 8:
                self.HandshakeJobsLink += "&f_SB2=9"
            else:
                self.HandshakeJobsLink += "&f_SB2=" + str(1+above40kInIncsOf20k)

        if len(self.location) > 0:
            self.HandshakeJobsLink +="&location=" + self.location.replace(" ", "%20").replace(",", "%2C") + "%2C%20United%20States"

        if self.field != "":
            self.HandshakeJobsLink +="&keywords=" + self.field.replace(" ", "%20")

        if len(self.HandshakeJobsLink) > 40:
            self.HandshakeJobsLink = self.HandshakeJobsLink.replace("https://www.linkedin.com/jobs/search/?&", "https://www.linkedin.com/jobs/search/?")

        print(self.HandshakeJobsLink)

    def linkToHTML(self, link):
        #Gets URL, add .content to turn it into something readable
        self.seleniumDriver.get(link.strip())
        time.sleep(1)
        try:
            WebDriverWait(self.seleniumDriver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "li"))
            )
        except:
            #self.seleniumDriver.quit()
            #self.seleniumDriver.close()
            return None

        return self.seleniumDriver.find_elements(By.TAG_NAME, "a")

    def findLinks(self):
        link = self.HandshakeJobsLink
        page = 1
        if not os.path.exists(self.writeTo + '.csv'):
            open(self.writeTo + '.csv', 'x')
        while True:
            a_tags = self.linkToHTML(link)
            print("current link: " + link)
            #print(urlHTML)
            if a_tags is not None:
                keepGoing = self.linkAlgorithm(a_tags)
                if keepGoing == False:
                    break
                page += 1
                link = self.HandshakeJobsLink + "&start=" + str(25*(page-1))
                print("nextLink= " + link)
            else:
                print("Did not find what you are looking for!")
                break
        #self.seleniumDriver.quit()
        print("Task Ended Sucessfully")

    def isProperLink(self, url):
        # Checks if the href is actually a word
        if url is not None:
            # Checks if the href is actually there (at least one letter)
            if len(url) > 0:
                # Checks to make sure it is not a downloadable file type (i.e, the link is not sending you to a download)
                if "pdf" not in url and "zIp" not in url and "zip" not in url \
                        and "win" not in url and "mp3" not in url and "mp4" not in \
                        url and "jpg" not in url and "JPEG" not in url and \
                        "jpeg" not in url and "docx" not in url and "pptx" not in \
                        url and "png" not in url:
                    return True

        return False

    def linkConditions(self, url):
        if "/jobs/view/" in url and "/jobs/view/externalApply/" not in url:
            return True
        return False

    def linkAlgorithm(self, a_tags):
        urlCleaning=[a_tag.get_attribute("href") for a_tag in a_tags if self.isProperLink(a_tag.get_attribute("href"))]
        urls=[url for url in urlCleaning if self.linkConditions(url)]
        if len(urls) > 0:
            for url in urls:
                if url not in open(self.writeTo + '.csv', encoding="utf-8").read():
                    self.writeToCSV(url)
            return True
        return False

    def writeToCSV(self, finalURL):
        csv = open(self.writeTo + '.csv', 'a', encoding="utf-8")
        csv.write(finalURL + "\n")
        csv.close()

