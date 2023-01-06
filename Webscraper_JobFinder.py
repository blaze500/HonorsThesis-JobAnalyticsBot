import time
from selenium import webdriver
from selenium.webdriver.common.by import By
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

    #Starts the Program\
    def __init__(self, field, type, location, inPerson, fullTime, salary, experience, education):
        self.field = field
        self.type = type
        self.location = location
        self.inPerson = inPerson
        self.fullTime = fullTime
        self.salary = salary
        self.experience = experience
        self.education = education
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
            gui.msgbox("Please Log In To Your Indeed Account On The Selenium Browser. Once You Are Done Click OK On This Message Box. \nDo not exit the Browser!", title='Job Analytics Bot')

            self.seleniumDriver.get("https://www.linkedin.com/login")
            gui.msgbox("Please Log In To Your Linkedin Account On The Selenium Browser. Once You Are Done Click OK On This Message Box. \nDo not exit the Browser!", title='Job Analytics Bot')

            self.seleniumDriver.get("https://app.joinhandshake.com/login")
            gui.msgbox("Please Log In To Your Handshake Account On The Selenium Browser. Once You Are Done Click OK On This Message Box. \nDo not exit the Browser!", title='Job Analytics Bot')


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
        fields = ['Biology', 'Chinese', 'Chemistry', 'Dance', 'English', 'Film', 'Finance', 'Gender Studies', 'History', 'Journalism', 'Music', 'Philosophy', 'Psychology']

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

        print(TextProcessor.ReturnYOEAllPhraseDictonary())

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
        self.field = gui.enterbox(msg1, title='Job Analytics Bot')
        if self.field is None:
            sys.exit()
        elif len(self.field) > 0:
            self.field.lower()


        msg2 = "Are You Looking For a Job or Internship?"
        joi = ["Job", "Internship"]
        self.type = gui.buttonbox(msg2, title='Job Analytics Bot', choices=joi)
        if self.type is None:
            sys.exit()
        else:
            self.type.lower()

        while True:
            msg3 = "What city do you want this job to be located at? \nIf you are not looking for a specific location leave these fields blank"
            cos = ["City", "State"]
            cityAndState = gui.multenterbox(msg3, title='Job Analytics Bot', fields=cos)

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
        self.inPerson = gui.buttonbox(msg4, title='Job Analytics Bot', choices=roip).lower()
        if self.inPerson is None:
            sys.exit()
        else:
            self.inPerson.lower()

        msg5 = "Do You Want This Job To Be Full Time, Part Time, Or Both?"
        ftopt = ["Full Time", "Part Time", "Both"]
        self.fullTime = gui.buttonbox(msg5, title='Job Analytics Bot', choices=ftopt).lower()
        if self.fullTime is None:
            sys.exit()
        else:
            self.fullTime.lower()

        msg6 = "What Salary Are You Looking For? \nType In 0 If You Aren't Looking For A Specific Salary"
        self.salary = gui.integerbox(msg6, title='Job Analytics Bot')
        if self.salary is None:
            sys.exit()

        msg7 = "What Is The Highest Level Of College Education You Have?"
        degree = ["Associate", "Bachelor", "Masters", "None"]
        self.education = gui.buttonbox(msg7, title='Job Analytics Bot', choices=degree).lower()
        if self.education is None:
            sys.exit()
        elif self.education == "None":
            self.experience = ''
        else:
            self.education.lower()

        msg8 = "What is your experience level?"
        experience = ["Entry", "Mid", "Senior", "None"]
        self.experience = gui.buttonbox(msg8, title='Job Analytics Bot', choices=experience).lower()
        if self.experience is None:
            sys.exit()
        elif self.experience == "None":
            self.experience = ''
        else:
            self.experience.lower()

