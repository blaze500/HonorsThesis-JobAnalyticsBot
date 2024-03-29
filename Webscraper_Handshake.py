import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os


class HandshakeJobs:

    def __init__(self, type, field, inPerson, fullTime, salary, location, education, experience, writeTo, numberOfJobsLimit, seleniumDriver):
        self.type = type
        self.field = field
        self.inPerson = inPerson
        self.fullTime = fullTime
        self.salary = salary
        self.location = location
        self.education = education
        self.experience = experience
        self.writeTo = writeTo
        self.numberOfJobsLimit = 1000000
        if numberOfJobsLimit is not None:
            self.numberOfJobsLimit = numberOfJobsLimit
        self.seleniumDriver = seleniumDriver










    # Makes the link based off of search filters in the search engine. This is done by figuring
    # out what filter (for example, salary, degree type, job type) is correlated to in the link
    # when you click on a filter. By doing this instead of say, clicking on each filter with a
    # selenium bot, it saves a lot of time and is more or less prone to the same errors a selenium
    # bot that clicks on the websites filters is (things moving, words changing, ect.).
    def HandshakeLinkMaker(self):

        self.HandshakeJobsLink ="https://app.joinhandshake.com/stu/postings?"

        if self.type == "internship":
            self.HandshakeJobsLink +="job.job_types%5B%5D=3"
        else:
            self.HandshakeJobsLink +="job.job_types%5B%5D=9"

        if self.fullTime == "full time":
            self.HandshakeJobsLink +="&employment_type_names%5B%5D=Full-Time"
        elif self.fullTime == "part time":
            self.HandshakeJobsLink +="&employment_type_names%5B%5D=Part-Time"
        else:
            self.HandshakeJobsLink +="&employment_type_names%5B%5D=Full-Time&employment_type_names%5B%5D=Part-Time"

        if self.salary > 0:
            self.HandshakeJobsLink +="&job.salary_types%5B%5D=1"

        if self.inPerson == "remote":
            self.HandshakeJobsLink += "&job.remote=true"
        elif self.inPerson == "in person":
            self.HandshakeJobsLink += "&job.on_site=true"
        else:
            self.HandshakeJobsLink += "&job.remote=true&job.on_site=true"

        #Replaces spaces with character number and then hexadecimal equivalent, as web links cannot function with a space in them.
        self.HandshakeJobsLink += "&query=" + self.field.replace(" ", "%20")


        print(self.HandshakeJobsLink)









    # Takes the link, turns it into something the Selenium driver can read
    # And waits for the page to load with the jobs
    def linkToHTML(self, link):
        #Gets URL, add .content to turn it into something readable
        self.seleniumDriver.get(link.strip())
        time.sleep(5)
        try:
            WebDriverWait(self.seleniumDriver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "li"))
            )
        except:
            #self.seleniumDriver.quit()
            #self.seleniumDriver.close()
            return None

        return self.seleniumDriver.find_elements(By.TAG_NAME, "a")










    # The skeleton of the search algorithm for gathering each webpage that contains
    # job links.
    def findLinks(self):
        link = self.HandshakeJobsLink
        page = 1
        # Makes a CSV if one doesnt exist, as the job links will be stored in a CSV
        if not os.path.exists(self.writeTo + '.csv'):
            open(self.writeTo + '.csv', 'x')
        while True:
            # Grabs a webpages a tags (an HTML DOM element which holds web links)
            a_tags = self.linkToHTML(link)
            print("current link: " + link)
            #print(urlHTML)
            if a_tags is not None:
                # Gathers the job postings on a page or stops the algorithm when there are none
                keepGoing = self.linkAlgorithm(a_tags)
                if keepGoing == False:
                    break
                page += 1
                # Goes to the next page of job listings on the job search engine.
                link = self.HandshakeJobsLink + "&page=" + str(page)
                print("nextLink= " + link)
            else:
                print("Did not find what you are looking for!")
                break
        #self.seleniumDriver.quit()
        print("Task Ended Sucessfully")







    # Checks to see if the link is not downloadable as we are not downloading anything
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





    # Checking conditions for link in order to get the links that have job.
    # Typically each job search will have their own thing in each link to
    # differentiate a job from some other link.
    def linkConditions(self, url):
        if "/stu/jobs/" in url and "ref=open-in-new-tab" in url:
            return True
        return False





    # Generic algorithm which takes all the links from the webpage/selenium objects and
    # filters them so that only the jobs remain and then writes them to a csv file.
    def linkAlgorithm(self, a_tags):
        #Gets all of the links that are not a downlodable one
        urlCleaning=[a_tag.get_attribute("href") for a_tag in a_tags if self.isProperLink(a_tag.get_attribute("href"))]
        # Gets all of the links that are job postings
        urls=[url for url in urlCleaning if self.linkConditions(url)]
        urlsInCSV = [url for url in urls if url not in open(self.writeTo + '.csv', encoding="utf-8").read()]
        if len(urlsInCSV) > 0:
            for url in urls:
                if url not in open(self.writeTo + '.csv', encoding="utf-8").read():
                    self.writeToCSV(url)
                if self.checkIfEnoughLinksInCSV():
                    return False
            return True
        return False





    # Generic CSV writter, which takes URLS (or any string for that matter) and places them in a CSV.
    def writeToCSV(self, finalURL):
        csv = open(self.writeTo + '.csv', 'a', encoding="utf-8")
        csv.write(finalURL + "\n")
        csv.close()

    def checkIfEnoughLinksInCSV(self):
        csv = open(self.writeTo + '.csv', encoding="utf-8")
        numberOfLines = len(csv.readlines())
        csv.close()
        if numberOfLines >= self.numberOfJobsLimit:
            return True
        return False