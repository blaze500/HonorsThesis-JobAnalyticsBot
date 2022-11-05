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
import Webscraper_Linkedin
import Webscraper_Handshake
import Webscraper_Indeed
import Webscraper_GetJobText
import ProcessingText
import Webscraper_GetStopwords
import easygui as gui
import sys

class JobFinder:

    #Starts the Program
    def __init__(self, field, type, location, inPerson, fullTime, salary, experience):
        self.field = field
        self.type = type
        self.location = location
        self.inPerson = inPerson
        self.fullTime = fullTime
        self.salary = salary
        self.experience = experience
        self.seleniumDriver = webdriver.Chrome("chromedriver.exe")
        self.automate = False


    def LoginToJobs(self):

        # The logins should NOT BE AUTOMATED. This was only created
        # to ease the process of login in so I can test things. This
        # has a few problems that prevent this from being reliable.
        # For example, captias getting in the way and HTML code changing.
        # Also sleep commands were added as errors are caused by the page
        # not loading in enough time constantly.

        if self.automate:

            logins = open("C:/Users/jaden/Videos/logins.txt", "r")
            loginsInfo = logins.readlines()

            # This is the login automation for indeed. This opens the indeed login, enters email, clicks on continue,
            # clicks on login with password, then enters password and clicks on the login button.
            self.seleniumDriver.get("https://secure.indeed.com/auth?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2F&tmpl=desktop&service=my&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fwww.indeed.com%2F&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.216882070.1436526071.1662068128-19035690.1662068128")

            time.sleep(2)
            self.seleniumDriver.find_element(By.CSS_SELECTOR, "[name='__email']").send_keys(loginsInfo[0].strip())
            button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[type='submit']")
            self.seleniumDriver.execute_script("arguments[0].click();", button)


            time.sleep(2)

            try:
                button = self.seleniumDriver.find_element(By.ID, "auth-page-google-password-fallback")
                self.seleniumDriver.execute_script("arguments[0].click();", button)
            except:
                print("Was Unable To Click On The Put In Password Due To Captcha On Indeed")
                wait = input("Press Enter to continue.")

            time.sleep(2)
            self.seleniumDriver.find_element(By.CSS_SELECTOR, "[name='__password']").send_keys(loginsInfo[1].strip())
            button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[type='submit']")
            self.seleniumDriver.execute_script("arguments[0].click();", button)




            wait = input("Press Enter to continue.")








            # This logs into Lindkedin. This types in the username and password and then clicks the login button.
            self.seleniumDriver.get("https://www.linkedin.com/login")

            time.sleep(2)

            self.seleniumDriver.find_element(By.ID, "username").send_keys(loginsInfo[0].strip())
            self.seleniumDriver.find_element(By.ID, "password").send_keys(loginsInfo[1].strip())
            button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[aria-label='Sign in']")
            self.seleniumDriver.execute_script("arguments[0].click();", button)

            time.sleep(2)


            wait = input("Press Enter to continue.")










            # This logs into handshake. This types in your an NCF school email, clicks on the sign in button, and clicks on the school button.
            # Then it goes to the NCF login page, where it will type in a username and password and click the login button.
            self.seleniumDriver.get("https://app.joinhandshake.com/login")

            time.sleep(2)

            self.seleniumDriver.find_element(By.ID, "email-address-identifier").send_keys( loginsInfo[2].strip() +"@ncf.edu")
            button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[aria-label='submit']")
            self.seleniumDriver.execute_script("arguments[0].click();", button)

            time.sleep(2)
            try:
                button = self.seleniumDriver.find_element(By.CSS_SELECTOR, "[title='Authentication for Handshake WebApp']")
                self.seleniumDriver.execute_script("arguments[0].click();", button)
            except:
                print("Was unable to do this due to click due to handshakes captcha")
                wait = input("Press Enter to continue.")


            time.sleep(2)

            try:
                self.seleniumDriver.find_element(By.ID, "frmLogin_UserName").send_keys(loginsInfo[2].strip())
                self.seleniumDriver.find_element(By.ID, "frmLogin_Password").send_keys(loginsInfo[3].strip())
                button = self.seleniumDriver.find_element(By.ID, "btnLogin")
                self.seleniumDriver.execute_script("arguments[0].click();", button)
            except:
                print("Was unable to do this due to click due to handshakes captcha 2")
                wait = input("Press Enter to continue.")

            time.sleep(2)

        else:
            self.seleniumDriver.get("https://secure.indeed.com/auth?hl=en_US&co=US&continue=https%3A%2F%2Fwww.indeed.com%2F&tmpl=desktop&service=my&from=gnav-util-homepage&jsContinue=https%3A%2F%2Fwww.indeed.com%2F&empContinue=https%3A%2F%2Faccount.indeed.com%2Fmyaccess&_ga=2.216882070.1436526071.1662068128-19035690.1662068128")
            gui.msgbox("Please Log In To Your Indeed Account On The Selenium Browser. Once You Are Done Click OK On This Message Box. \nDo not exit the Browser!")

            self.seleniumDriver.get("https://www.linkedin.com/login")
            gui.msgbox("Please Log In To Your Linkedin Account On The Selenium Browser. Once You Are Done Click OK On This Message Box. \nDo not exit the Browser!")

            self.seleniumDriver.get("https://app.joinhandshake.com/login")
            gui.msgbox("Please Log In To Your Handshake Account On The Selenium Browser. Once You Are Done Click OK On This Message Box. \nDo not exit the Browser!")


    def GetJobLinks(self):

        indeedJobs = Webscraper_Indeed.IndeedJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                  self.salary, self.location, self.education,
                                                  self.experience, 'IndeedJobs', None, self.seleniumDriver)
        indeedJobs.indeedJobsLinkMaker()
        indeedJobs.findLinks()



        LinkedinJobs = Webscraper_Linkedin.LinkedinJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                        self.salary, self.location, self.education,
                                                        self.experience, 'LinkedinJobs', None, self.seleniumDriver)
        LinkedinJobs.LinkedinLinkMaker()
        LinkedinJobs.findLinks()



        HandshakeJobs = Webscraper_Handshake.HandshakeJobs(self.type, self.field, self.inPerson, self.fullTime,
                                                           self.salary, self.location, self.education,
                                                           self.experience, 'HandshakeJobs', None, self.seleniumDriver)
        HandshakeJobs.HandshakeLinkMaker()
        HandshakeJobs.findLinks()


    def GetJobText(self):
        getJobText = Webscraper_GetJobText.JobTextGrabber(self.seleniumDriver, ["HandshakeJobs", "IndeedJobs", "LinkedinJobs"])
        getJobText.getHandshakeJobText("HandshakeJobs")
        getJobText.getIndeedJobText("IndeedJobs")
        getJobText.getLinkedinJobText("LinkedinJobs")


    def GetStopWords(self):
        fields = ['Biology', 'Chinese', 'Computer Science', 'Dance', 'English', 'Film', 'Finance', 'Gender Studies', 'History', 'Journalism', 'Music', 'Philosophy', 'Psychology']

        StopWordGenerator = Webscraper_GetStopwords.StopWordGenerator(self.field, fields, 15, self.seleniumDriver)
        StopWordGenerator.GetJobLinksForStopWords()
        StopWordGenerator.GatherXJobLinksFromCSVs()
        StopWordGenerator.GetJobTextForStopWords()
        StopWordGenerator.ProcessJobTextIntoStopWords()



    def ProcessJobText(self):
        TextProcessor = ProcessingText.TextProcessor(["HandshakeJobsText", "IndeedJobsText", "LinkedinJobsText"])

        TextProcessor.TextFilesToJobTextArrays()

        TextProcessor.YearsOfExperienceScentenceGenerator()

        TextProcessor.ProcessYearsOfExperienceText()

        TextProcessor.SpecialWordCounterAlgorithm()

        TextProcessor.CleaningTextAlgorithm()

        TextProcessor.WordCounterAlgorithm()

        TextProcessor.SortDictonaries()

        return [TextProcessor.ReturnAllSpecialWordsDictonary(), TextProcessor.ReturnYOEAllPhraseDictonary(), TextProcessor.RemoveBottomAllWordsDicByPercentage(10)]

    def EndProgram(self):
        self.seleniumDriver.quit()

    def Questionare(self):
        msg1 = "What Field Of Work Are You Looking For?"
        fow = "Field Of Word"
        self.field = gui.enterbox(msg1, title='Resume Optimizer')
        if self.field is None:
            sys.exit()
        elif len(self.field) > 0:
            self.field.lower()


        msg2 = "Are You Looking For a Job or Internship?"
        joi = ["Job", "Internship"]
        self.type = gui.buttonbox(msg2, title='Resume Optimizer', choices=joi)
        if self.type is None:
            sys.exit()
        else:
            self.type.lower()

        while True:
            msg3 = "What city do you want this job to be located at? \nIf you are not looking for a specific location leave these fields blank"
            cos = ["City", "State"]
            cityAndState = gui.multenterbox(msg3, title='Resume Optimizer', fields=cos)

            if cityAndState is None:
                sys.exit()
            if cityAndState[0] == "" and cityAndState[1] == '':
                self.location = ""
            elif LocationChecker.isCity(cityAndState[0]) and LocationChecker.isState(cityAndState[1]):
                if LocationChecker.isLocation(cityAndState[0] + "," + cityAndState[1]):
                    self.location = cityAndState[0] + "," + cityAndState[1]
                    break
                else:
                    gui.msgbox("The City And State You Have Choosen Do Not Exist Together. \nPlease Try Again.")
            else:
                if len(cityAndState[0]) > 0 and len(cityAndState[1]) > 0:
                    gui.msgbox("The City And State You Have Choosen Do Not Exist Together. \nPlease Try Again.")
                else:
                    gui.msgbox("You Must Either Leave Both Fields Blank or Fill Them BOTH Out. \nPlease Try Again.")

        msg4 = "Do You Want This Job To Be Remote, In Person, or Both?"
        roip = ["Remote", "In Person", "Both"]
        self.inPerson = gui.buttonbox(msg4, title='Resume Optimizer', choices=roip).lower()
        if self.inPerson is None:
            sys.exit()
        else:
            self.inPerson.lower()

        msg5 = "Do You Want This Job To Be Full Time, Part Time, Or Both?"
        ftopt = ["Full Time", "Part Time", "Both"]
        self.fullTime = gui.buttonbox(msg5, title='Resume Optimizer', choices=ftopt).lower()
        if self.fullTime is None:
            sys.exit()
        else:
            self.fullTime.lower()

        msg6 = "What Salary Are You Looking For? \nType In 0 If You Aren't Looking For A Specific Salary"
        self.salary = gui.integerbox(msg6, title='Resume Optimizer')
        if self.salary is None:
            sys.exit()

        msg7 = "What Is The Highest Level Of College Education You Have?"
        degree = ["Associate", "Bachelor", "Masters", "None"]
        self.education = gui.buttonbox(msg7, title='Resume Optimizer', choices=degree).lower()
        if self.education is None:
            sys.exit()
        elif self.education == "None":
            self.experience = ''
        else:
            self.education.lower()

        msg8 = "What is your experience level?"
        experience = ["Entry", "Mid", "Senior", "None"]
        self.experience = gui.buttonbox(msg8, title='Resume Optimizer', choices=experience).lower()
        if self.experience is None:
            sys.exit()
        elif self.experience == "None":
            self.experience = ''
        else:
            self.experience.lower()

"""
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

        print("Do You Want This Full Time or Part Time? (if you want both, just type in both)")
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

            print("What state do you want this job to be located at? (If you are not looking for a specific state, hit enter)")
            print("PLEASE NOTE: The starting letter of each word MUST be capitalized")
            while True:
                state = input("Your Answer:")
                if state == "" and self.location == "":
                    break
                elif len(state) > 0 and self.location == "":
                    print("You must leave this blank or restart the program as you have no city.")
                elif LocationChecker.isState(state):
                    if LocationChecker.isLocation(self.location + ",state"):
                        self.location += ","
                        self.location += state
                        break
                    else:
                        print("The City and State you choose do note exist together. Please pick another pair of a City and a State.")
                else:
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

        '''
        print("What Is The Name Of The CSV File You Would Like This Written To?")
        self.writeTo = input("Your Answer:")
        print("")
        '''

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
        #self.writeTo = fileLines[8].strip()
        file.close()
        return self
"""
