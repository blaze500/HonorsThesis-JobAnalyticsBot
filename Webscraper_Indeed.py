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

class IndeedJobs:

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

    def indeedJobsLinkMaker(self):

        self.indeedJobsLink = "https://www.indeed.com/jobs?"

        if self.field != "":
            self.indeedJobsLink +="&q=" + self.field.replace(" ", "+")

        if len(self.location) > 0:
            self.indeedJobsLink +="&l=" + self.location.replace(" ", "+")

        self.indeedJobsLink += "&sc=0kf%3A"

        if self.education == "associate":
            self.indeedJobsLink += "attr(FCGTU%7CQJZM9%7CUTPWG%252COR)"
        elif self.education == "bachelor":
            self.indeedJobsLink +="attr(FCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)"
        elif self.education == "masters":
            self.indeedJobsLink +="attr(EXSNN%7CFCGTU%7CHFDVW%7CQJZM9%7CUTPWG%252COR)"
        else:
            self.indeedJobsLink += "attr(FCGTU%7CQJZM9%252COR)"

        if self.type == "internship":
            self.indeedJobsLink += "jt(internship)"
        elif self.fullTime == "full time":
            self.indeedJobsLink +="jt(fulltime)"
        elif self.fullTime == "part time":
            self.indeedJobsLink +="jt(parttime)"

        if self.inPerson == "remote":
            self.indeedJobsLink +="attr(DSQF7)"

        if self.experience == "entry":
            self.indeedJobsLink +="explvl(ENTRY_LEVEL)"
        elif self.experience =="mid":
            self.indeedJobsLink +="explvl(MID_LEVEL)"
        elif self.experience =="senior":
            self.indeedJobsLink +="explvl(SENIOR_LEVEL)"
        else:
            self.indeedJobsLink +="attr(D7S5D)"

        self.indeedJobsLink += "%3B"
        print(self.indeedJobsLink)

    def linkToHTML(self, link):
        #Gets URL, add .content to turn it into something readable
        self.seleniumDriver.get(link.strip())
        time.sleep(2)
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
        link = self.indeedJobsLink
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
                link = self.indeedJobsLink + "&start=" + str((page-1)*10)
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
        if "/rc/clk?jk=" in url:
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

