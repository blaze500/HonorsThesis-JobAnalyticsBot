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

class JobFinder:

    #Starts the Program
    def __init__(self):

        switch= True

        if switch is True:
            self.readFile("JobText")
        else:
            self.Questionare()

        self.seleniumDriver = webdriver.Chrome("chromedriver.exe")

        #self.seleniumDriver.get("https://www.linkedin.com/login")
        #print("Please log in to your Linkedin account. Do not exit the Selenium Browser")
        #wait = input("Press Enter to continue.")

        #self.seleniumDriver.get("https://app.joinhandshake.com/login")
        #print("Please log in to your Handshake account. Do not exit the Selenium Browser")
        #wait = input("Press Enter to continue.")

        #self.seleniumDriver.get("https://secure.indeed.com/auth?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2F&tmpl=desktop&service=my&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fwww.indeed.com%2F&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.216882070.1436526071.1662068128-19035690.1662068128")
        #print("Please log in to your Indeed account. Do not exit the Selenium Browser")
        #wait = input("Press Enter to continue.")

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

        """
        googleJobs = Webscraper_GoogleCareers.GoogleCareerJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                               self.salary, self.location, self.education,
                                                               self.experience, self.writeTo, self.seleniumDriver)
        googleJobs.googleJobsLinkMaker()
        googleJobs.findLinks()


        # Linkedin needs login
        LinkedinJobs = Webscraper_Linkedin.LinkedinJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                               self.salary, self.location, self.education,
                                                               self.experience, self.writeTo, self.seleniumDriver)
        LinkedinJobs.LinkedinLinkMaker()
        LinkedinJobs.findLinks()

        HandshakeJobs = Webscraper_Handshake.HandshakeJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                        self.salary, self.location, self.education,
                                                        self.experience, self.writeTo, self.seleniumDriver)
        HandshakeJobs.HandshakeLinkMaker()
        HandshakeJobs.findLinks()
        """

        indeedJobs = Webscraper_Indeed.IndeedJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                               self.salary, self.location, self.education,
                                                               self.experience, self.writeTo, self.seleniumDriver)
        indeedJobs.indeedJobsLinkMaker()
        indeedJobs.findLinks()

        self.seleniumDriver.quit()

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

JobFinder()
