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

class GoogleJobs:

    def __init__(self, type, field, inPerson, fullTime, salary, location, education, experience, writeTo):
        self.type = type
        self.field = field
        self.inPerson = inPerson
        self.fullTime = fullTime
        self.salary = salary
        self.location = location
        self.education = education
        self.experience = experience
        self.writeTo = writeTo

    def googleLinkMaker(self):

        fullTime =self.fullTime.replace(" ", "+") + "+"

        expereince = self.experience
        if self.experience != "":
            expereince += "+level+"

        inPerson = self.inPerson.replace(" ", "+")
        if self.inPerson != "":
            inPerson += "+"

        linkField = self.field.replace(" ", "+") + "+"
        type = self.type.replace(" ", "+") + "+"
        location = self.location.replace(" ", "+")

        self.googleLink = "https://www.google.com/search?q=" + fullTime + expereince + inPerson + linkField + type + location
        print(self.googleLink)

    def linkToHTML(self,link):
        #Gets URL, add .content to turn it into something readable
        url = requests.get(link.strip())
        print(url.content)
        #Turns Page into HTML
        urlHTML = BeautifulSoup(url.content, 'html.parser')
        return urlHTML

    def findLinks(self):
        page=1
        link=self.googleLink
        while link != "":

            # A link page _ in a tag
            page+=1
            link=""


class GoogleCareerJobs:

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

    def googleJobsLinkMaker(self):

        self.googleJobsLink = "https://careers.google.com/jobs/results/"

        if self.education == "associate":
            self.googleJobsLink += "&degree=ASSOCIATE"
        elif self.education == "bachelor":
            self.googleJobsLink +="&degree=BACHELORS"
        elif self.education == "masters":
            self.googleJobsLink +="&degree=MASTERS"

        if self.fullTime == "full time":
            self.googleJobsLink +="&employment_type=FULL_TIME"
        elif self.fullTime == "part time":
            self.googleJobsLink +="&employment_type=PART_TIME"
        elif self.fullTime == "both":
            self.googleJobsLink +="&employment_type=FULL_TIME&employment_type=PART_TIME"

        if self.type == "internship":
            self.googleJobsLink += "&employment_type=INTERN"

        if self.inPerson != "in person":
            self.googleJobsLink +="&has_remote=true"

        if len(self.location) > 0:
            self.googleJobsLink +="&location=" + self.location.replace(" ", "%20")

        if self.field != "":
            self.googleJobsLink +="&q=" + self.field.replace(" ", "%20")

        if len(self.googleJobsLink) > 40:
            self.googleJobsLink = self.googleJobsLink.replace("https://careers.google.com/jobs/results/&", "https://careers.google.com/jobs/results/?")

        print(self.googleJobsLink)

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
        link = self.googleJobsLink
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
                link = self.googleJobsLink + "&page=" + str(page)
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
        if "/jobs/results/" in url and "/jobs/results/?" not in url:
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

