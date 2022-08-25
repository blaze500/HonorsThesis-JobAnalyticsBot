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

class JobFinder:

    '''
    type = ""
    field = ""
    inPerson = ""
    fullTime = ""
    salary = ""
    location = ""
    education = ""
    experience = ""
    '''

    #Starts the Program
    def __init__(self):

        switch= True

        if switch is True:
            self.readFile("JobText")
        else:
            self.Questionare()

        self.seleniumDriver = webdriver.Chrome("chromedriver.exe")
        print("something")
        wait = input("Press Enter to continue.")
        print("something")

        print(self.type)
        print(self.field)
        print(self.inPerson)
        print(self.fullTime)
        print(self.salary)
        print(self.location)
        print(self.education)
        print(self.experience)
        print(self.writeTo)
        #createFile()



        googleJobs = Webscraper_GoogleCareers.GoogleCareerJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                               self.salary, self.location, self.education,
                                                               self.experience, self.writeTo, self.seleniumDriver)
        googleJobs.googleJobsLinkMaker()
        googleJobs.findLinks()

        print("something")
        wait = input("Press Enter to continue.")
        print("something")
        
        # Linkedin needs login
        LinkedinJobs = Webscraper_Linkedin.LinkedinJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                               self.salary, self.location, self.education,
                                                               self.experience, self.writeTo, self.seleniumDriver)
        LinkedinJobs.LinkedinLinkMaker()
        LinkedinJobs.findLinks()

        """
        HandshakeJobs = Webscraper_Handshake.HandshakeJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                        self.salary, self.location, self.education,
                                                        self.experience, self.writeTo, self.seleniumDriver)
        HandshakeJobs.HandshakeLinkMaker()
        HandshakeJobs.findLinks()
        """

        self.seleniumDriver.quit()
        self.seleniumDriver.close()

    def Questionare(self):

        print("Are You Looking For a Job or Internship?")
        while True:
            self.type = input("Your Answer:").lower()
            if self.type == "job" or self.type == "internship":
                break
            else:
                print("The Answer You Put In Was Wrong. Please Try Again.")
        print("")

        print("What Field Are You Looking For?")
        self.field = input("Your Answer:").lower()
        print("")

        print("Do You Want This Remote, In Person, or Both?")
        while True:
            self.inPerson = input("Your Answer:").lower()
            if self.inPerson == "in person" or self.inPerson == "remote" or self.inPerson == "both":
                break
            else:
                print("The Answer You Put In Was Wrong. Please Try Again.")
        print("")

        print("Do You Want This Full Time or Part Time? (if you want both, just hit enter)")
        while True:
            self.fullTime = input("Your Answer:").lower()
            if self.fullTime == "full time" or self.fullTime == "part time" or self.fullTime == "both":
                break
            else:
                print("The Answer You Put In Was Wrong. Please Try Again.")
        print("")

        print("What Salary Are You Looking For?")
        print("Note: this will look for the number you type in or higher")
        print("so if you are looking for any salary, type in 0")
        self.salary = int(input("Your Answer:"))
        print("")

        while True:
            print(
                "What city do you want this job to be located at? (If you are not looking for a specific city, hit enter)")
            print("PLEASE NOTE: The starting letter of each word MUST be capitalized")
            while True:
                city = input("Your Answer:")
                if city == "" or LocationChecker.isCity(city):
                    self.location = city
                    break
                print("The city you were looking for isnt there")
            print("")

            print(
                "What state do you want this job to be located at? (If you are not looking for a specific state, hit enter)")
            print("PLEASE NOTE: The starting letter of each word MUST be capitalized")
            while True:
                state = input("Your Answer:")
                if state == "":
                    break
                elif LocationChecker.isState(state):
                    if len(self.location) > 0:
                        self.location += ","
                    self.location += state
                    break
                print("The State you were looking for isnt there")
            print(self.location)
            print("")

            if self.location == "" or "," not in self.location or LocationChecker.isLocation(self.location):
                break
            else:
                print("The city and state you have selected is not a location in the United States")
                print("You will have to enter a new city and state")
                self.location = ""

        print("What is the highest level of Education you have? (Associate, Bachelor, Masters, or hit enter)")
        while True:
            self.education = input("Your Answer:").lower()
            if self.education == "associate" or self.education == "bachelor" or self.education == "masters" or self.experience == "":
                break
            else:
                print("The Answer You Put In Was Wrong. Please Try Again")
        print("")

        print("What is your experience level? (Entry, Mid, Senior, or just hit enter)")
        while True:
            self.experience = input("Your Answer:").lower()
            if self.experience == "entry" or self.experience == "mid" or self.experience == "senior" or self.experience == "":
                break
            else:
                print("The Answer You Put In Was Wrong. Please Try Again")
        print("")

        print("What Is The Name Of The CSV File You Would Like This Written To?")
        self.writeTo = input("Your Answer:")
        print("")

    def readFile(self, fileName):
        file = open(fileName + ".txt", "r")
        fileLines = file.readlines()
        self.type = fileLines[0].strip()
        self.field = fileLines[1].strip()
        self.inPerson = fileLines[2].strip()
        self.fullTime = fileLines[3].strip()
        self.salary = fileLines[4].strip()
        self.location = fileLines[5].strip()
        self.education = fileLines[6].strip()
        self.experience = fileLines[7].strip()
        self.writeTo = fileLines[8].strip()
        file.close()

    def linkToHTML(self,link):
        #Gets URL, add .content to turn it into something readable
        url = requests.get(link.strip())
        print(url.content)
        #Turns Page into HTML
        urlHTML = BeautifulSoup(url.content, 'html.parser')
        return urlHTML


    def linkMakerForJobSites(self,phrase):
        # self.googleLink= "https://www.google.com/search?q=computer+science+job"
        # %20 = a space encoded in hex
        # %2C = a comma encoded in hex

        return
        #https://www.google.com/search?q=computer+science+job
        # %20 = a space encoded in hex
        # %2C = a comma encoded in hex
        # https://www.indeed.com/jobs?q= &l=
        # https://www.linkedin.com/jobs/search/?keywords=software%20engineer

    #findLinks('https://github.com/blaze500/TwitterCovidMisinformation-Project1-1/blob/main/Search.py')


JobFinder()


"""

class GoogleCareerJobs:

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
        self.selenium = webdriver.Chrome("chromedriver.exe")

    def googleJobsLinkMaker(self):

        self.googleJobsLink = "https://careers.google.com/jobs/results/"

        if self.education == "associate":
            self.googleJobsLink += "&degree=ASSOCIATE"
        elif self.education == "bachelor":
            self.googleJobsLink +="&degree=BACHELOR"
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

        if self.field == "":
            self.googleJobsLink +="&q=" + self.field.replace(" ", "%20")

        if len(self.googleJobsLink) > 40:
            self.googleJobsLink = self.googleJobsLink.replace("https://careers.google.com/jobs/results/&", "https://careers.google.com/jobs/results/?")

        print(self.googleJobsLink)

    def linkToHTML(self, link):
        #Gets URL, add .content to turn it into something readable
        print(link.strip())
        url = requests.get(link.strip())
        print(url.content)
        #Turns Page into HTML
        urlHTML = BeautifulSoup(url.content, 'html.parser')
        return urlHTML

    def findLinks(self):
        link = self.googleJobsLink
        page = 1
        while link != "":
            urlHTML = self.linkToHTML(link)
            print(urlHTML)
            link = self.linkAlgorithm(urlHTML, page)
            page += 1

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
        if "/jobs/results/" in url:
            print("true")
            return True
        return False

    def linkAlgorithm(self, linkList, page):
        nextLink=""
        for a_tag in linkList.find_all('li'):
            url=a_tag.get('href')
            print(url)
            #
            if self.isProperLink(url):
                #
                if self.linkConditions(url):
                    # checks to see if that is the link to the next page
                    if url.contains("page="+str(page+1)):
                        nextLink=url
                    # if its not, write it to a csv
                    else:
                        #Because I am not looking for new links, I will
                        finalURL = 'http://' + urlparse(url).netloc + url.get('href')
                        self.writeToCSV(finalURL)
        return nextLink

    def writeToCSV(self, finalURL):
        csv = open(self.writeTo + '.csv', 'a', encoding="utf-8")
        csv.write(finalURL + "\n")
        csv.close()

"""

"""
class GoogleCareerJobs:

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
        self.seleniumDriver = webdriver.Chrome("chromedriver.exe")

    def googleJobsLinkMaker(self):

        self.googleJobsLink = "https://careers.google.com/jobs/results/"

        if self.education == "associate":
            self.googleJobsLink += "&degree=ASSOCIATE"
        elif self.education == "bachelor":
            self.googleJobsLink +="&degree=BACHELOR"
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

        if self.field == "":
            self.googleJobsLink +="&q=" + self.field.replace(" ", "%20")

        if len(self.googleJobsLink) > 40:
            self.googleJobsLink = self.googleJobsLink.replace("https://careers.google.com/jobs/results/&", "https://careers.google.com/jobs/results/?")

        print(self.googleJobsLink)

    def linkToHTML(self, link):
        #Gets URL, add .content to turn it into something readable
        self.seleniumDriver.get(link.strip())
        try:
            a_tags = WebDriverWait(self.seleniumDriver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "li"))
            )
        except:
            self.seleniumDriver.quit()
            self.seleniumDriver.close()
            return None

        return self.seleniumDriver.find_elements(By.TAG_NAME, "a")


    def findLinks(self):
        link = self.googleJobsLink
        page = 1
        while link != "":
            a_tags = self.linkToHTML(link)
            #print(urlHTML)
            if a_tags is not None:
                link = self.linkAlgorithm(a_tags, link, page)
                page += 1
                print("nextLink= " + link)
            else:
                print("Did not find what you are looking for!")
                break;

        self.seleniumDriver.close()

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

    def linkConditions(self, url, link, page):
        if "/jobs/results/" in url and "/jobs/results/?" not in url:
            #print("true")
            return True
        elif link in url and "page="+str(page+1) in url:
            return True
        return False

    def linkAlgorithm(self, a_tags, link, page):
        nextLink=""
        for a_tag in a_tags:
            url=a_tag.get_attribute("href")
            #print(url)
            #
            if self.isProperLink(url):
                #
                if self.linkConditions(url, link, page):
                    # checks to see if that is the link to the next page
                    if "page="+str(page+1) in url:
                        nextLink=url
                    # if its not, write it to a csv
                    else:
                        print(url)
                        #Because I am not looking for new links, I will
                        self.writeToCSV(url)
        return nextLink

    def writeToCSV(self, finalURL):
        csv = open(self.writeTo + '.csv', 'a', encoding="utf-8")
        csv.write(finalURL + "\n")
        csv.close()

"""