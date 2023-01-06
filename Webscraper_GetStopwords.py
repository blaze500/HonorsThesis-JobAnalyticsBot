import os
import Webscraper_Linkedin
import Webscraper_Handshake
import Webscraper_Indeed
import Webscraper_GetJobText
import ProcessingText
import csv

class StopWordGenerator:

    #Starts the Program
    def __init__(self, field, fields, gatherXAmountOfJobLinks, seleniumDriver):

        self.type = 'job'
        self.fields = [element.lower() for element in fields]
        if field in self.fields:
            self.fields.remove(field)
        self.inPerson = 'both'
        self.fullTime = 'full time'
        self.salary = 0
        self.location = ''
        self.education = 'bachelor'
        self.experience = 'entry'
        self.gatherXAmountOfJobLinks = gatherXAmountOfJobLinks
        self.seleniumDriver = seleniumDriver



    def GetJobLinksForStopWords(self):
        for field in self.fields:

            indeedJobs = Webscraper_Indeed.IndeedJobs(self.type, field, self.inPerson, self.fullTime,
                                                      self.salary, self.location, self.education,
                                                      self.experience, 'IndeedJobs' + field.replace(' ', ''), self.gatherXAmountOfJobLinks, self.seleniumDriver)
            indeedJobs.indeedJobsLinkMaker()
            indeedJobs.findLinks()






            LinkedinJobs = Webscraper_Linkedin.LinkedinJobs(self.type, field, self.inPerson, self.fullTime,
                                                            self.salary, self.location, self.education,
                                                            self.experience, 'LinkedinJobs' + field.replace(' ', ''), self.gatherXAmountOfJobLinks, self.seleniumDriver)
            LinkedinJobs.LinkedinLinkMaker()
            LinkedinJobs.findLinks()






            HandshakeJobs = Webscraper_Handshake.HandshakeJobs(self.type, field, self.inPerson, self.fullTime,
                                                               self.salary, self.location, self.education,
                                                               self.experience, 'HandshakeJobs' + field.replace(' ', ''), self.gatherXAmountOfJobLinks, self.seleniumDriver)
            HandshakeJobs.HandshakeLinkMaker()
            HandshakeJobs.findLinks()



    def GatherXJobLinksFromCSVs(self):
        jobSearchJobs= ['IndeedJobs', 'LinkedinJobs', 'HandshakeJobs']
        for name in jobSearchJobs:
            for field in self.fields:
                with open(name + field.replace(' ', '') + '.csv', 'rt') as file:
                    reader = csv.reader(file, delimiter=',')
                    count = 0
                    for row in reader:
                        print('row[0]:' + str(row[0]))
                        CSV = open(name + 'StopWords' + '.csv', 'a', encoding="utf-8")
                        CSV.write(row[0] + "\n")
                        CSV.close()
                        count += 1
                        if count == self.gatherXAmountOfJobLinks:
                            break

        for field in self.fields:
            os.remove('HandshakeJobs' + field.replace(' ', '') + ".csv")
            os.remove('IndeedJobs' + field.replace(' ', '') + ".csv")
            os.remove('LinkedinJobs' + field.replace(' ', '') + ".csv")




    def GetJobTextForStopWords(self):
        getJobText = Webscraper_GetJobText.JobTextGrabber(self.seleniumDriver, ["HandshakeJobsStopWords", "IndeedJobsStopWords", "LinkedinJobsStopWords"])
        getJobText.getHandshakeJobText('HandshakeJobsStopWords')
        getJobText.getIndeedJobText('IndeedJobsStopWords')
        getJobText.getLinkedinJobText('LinkedinJobsStopWords')



    def ProcessJobTextIntoStopWords(self):
        TextProcessor = ProcessingText.TextProcessor(["HandshakeJobsStopWordsText", "IndeedJobsStopWordsText", "LinkedinJobsStopWordsText"])

        TextProcessor.TextFilesToJobTextArrays()

        TextProcessor.CleaningTextAlgorithm()

        TextProcessor.WordCounterAlgorithm()

        TextProcessor.SortDictonaries()

        stopWordDictonaries = TextProcessor.RemoveTopWordsInJobSearchDictsByPercentage(75)

        print(stopWordDictonaries)

        for dictonary in stopWordDictonaries.values():
            self.PutWordsIntoStopwordsFile(dictonary.keys())

    def PutWordsIntoStopwordsFile(self, stopwords):
        txtFile = open('stopwords.txt', 'a', encoding="utf-8")
        for word in stopwords:
            with open('stopwords.txt', 'rt', encoding="utf-8") as stopWordFile:
                if str(word) not in stopWordFile:
                    txtFile.write(str(word) + "\n")
        txtFile.close()



