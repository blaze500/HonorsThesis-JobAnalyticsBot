import os
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords.words('english')
import re
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
import TextCleaningLemmatizer
from word2number import w2n

class TextProcessor:

    #Starts the Program
    def __init__(self, directoryNames):

        self.directoryNames = directoryNames

        # Years Of Experience (YOE), dictonaries which record the years of ___ found in each text.
        self.YOEText = {}

        # Years Of Experience (YOE), dictonaries which record the years of ___ found in each text.
        self.YOEDictionaries = {}
        self.YOEAllPhraseDictonary= {}

        # An array which contains the dictionaries for each job website
        self.SpecialWordDictionaries = {}

        # An array which contains the dictionaries for each job website
        self.WordDictionaries = {}

        for directory in self.directoryNames:
            self.WordDictionaries[directory] = {}
            self.YOEDictionaries[directory] = {}
            self.YOEText[directory] = []
            self.SpecialWordDictionaries[directory] = {}

        self.AllWordsDictonary = {}

        self.AllSpecialWordsDictonary = {}

        # An array which contains the arrays of each job website
        self.JobTexts = {}





    def TextFilesToJobTextArrays(self):

        for fileName in self.directoryNames:
            directoryJobTexts=[]
            for textFilePath in os.listdir(fileName):
                with open(os.path.join(fileName, textFilePath), 'r', encoding="utf-8") as jobDescription:
                    jobDescriptionText = jobDescription.read().lower().replace("\n"," ")
                    directoryJobTexts.append(jobDescriptionText)
            self.JobTexts[fileName] = directoryJobTexts




    def CleaningTextAlgorithm(self):
        for fileName in self.directoryNames:
            for number, text in enumerate(self.JobTexts[fileName]):
                self.JobTexts[fileName][number] = self.cleanText(text)





    def cleanText(self, text):

        textWithoutSpecialCharacters = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", text)

        lemmatizer = TextCleaningLemmatizer.TextCleaningLemmatizer()

        lemmatizedText = lemmatizer.lemmatize_sentence(textWithoutSpecialCharacters)

        everyWordInText = lemmatizedText.split(" ")

        fullyCleanedWords = []



        if os.path.exists('stopwords.txt'):
            for word in everyWordInText:
                if word not in stopwords.words('english') and word not in open('stopwords.txt').read():
                    fullyCleanedWords.append(word)
        else:
            for word in everyWordInText:
                if word not in stopwords.words('english'):
                    fullyCleanedWords.append(word)

        fullyCleanedText = ' '.join(fullyCleanedWords)


        return fullyCleanedText





    def SpecialWordCounterAlgorithm(self):

        for fileName in self.directoryNames:
            for count, jobText in enumerate(self.JobTexts[fileName]):
                self.JobTexts[fileName][count] = self.specialWordFinder(jobText, fileName)





    def WordCounterAlgorithm(self):

        for fileName in self.directoryNames:
            for text in self.JobTexts[fileName]:
                for word in text.split():

                    if word in self.WordDictionaries[fileName]:
                        self.WordDictionaries[fileName][word] += 1
                    else:
                        self.WordDictionaries[fileName][word] = 1

                    if word in self.AllWordsDictonary:
                        self.AllWordsDictonary[word] += 1
                    else:
                        self.AllWordsDictonary[word] = 1





    def specialWordFinder(self, text, fileName):
        newText=""
        specialWordsFile = open('SpecialWords.txt', 'r', encoding="utf-8")

        # replacing end splitting the text
        # when newline ('\n') is seen.
        specialWords = specialWordsFile.read().splitlines()

        for word in specialWords:
            splitText = text.split(word.lower())
            wordsRemoved = len(splitText)-1
            if wordsRemoved > 0:
                if word.lower() in self.SpecialWordDictionaries[fileName]:
                    self.SpecialWordDictionaries[fileName][word.lower()] += wordsRemoved
                else:
                    self.SpecialWordDictionaries[fileName][word.lower()] = wordsRemoved

                if word.lower() in self.AllSpecialWordsDictonary:
                    self.AllSpecialWordsDictonary[word.lower()] += wordsRemoved
                else:
                    self.AllSpecialWordsDictonary[word.lower()] = wordsRemoved

            newTextWithWordRemoved = ''.join(splitText)
            newText=newTextWithWordRemoved


        specialWordsFile.close()

        return newText





    def SortDictonaries(self):
        for fileName in self.directoryNames:
            self.WordDictionaries[fileName] = dict(sorted(self.WordDictionaries[fileName].items(), key=lambda x: x[1], reverse=True))

        for fileName in self.directoryNames:
            self.SpecialWordDictionaries[fileName] = dict(sorted(self.SpecialWordDictionaries[fileName].items(), key=lambda x: x[1], reverse=True))

        self.AllWordsDictonary = dict(sorted(self.AllWordsDictonary.items(), key=lambda x: x[1], reverse=True))
        self.AllSpecialWordsDictonary = dict(sorted(self.AllSpecialWordsDictonary.items(), key=lambda x: x[1], reverse=True))
        self.YOEAllPhraseDictonary={key: value for key, value in sorted(self.YOEAllPhraseDictonary.items(), reverse=True)}






    def RemoveTopWordsInJobSearchDictsByPercentage(self,percantage):
        documentsInEachDirectory = {}
        newDirectoryDictonaries = {}

        for fileName in self.directoryNames:
            documentsInEachDirectory[fileName]=len(os.listdir(fileName))
            newDirectoryDictonaries[fileName] = {}

        for fileName in self.directoryNames:
            documents =  int(documentsInEachDirectory[fileName])
            for key, val in self.WordDictionaries[fileName].items():
                if val >= round(documents*(1-percantage/100)):
                    newDirectoryDictonaries[fileName][key] = val

        return newDirectoryDictonaries




    def RemoveTopAllWordsDicByPercentage(self,percantage):
        newAllWordsDictonary = {}
        totalDocuments = 0

        for fileName in self.directoryNames:
            totalDocuments += len(os.listdir(fileName))

        for key, val in self.AllWordsDictonary.items():
            if val >= round (totalDocuments * (1 - percantage / 100)):
                newAllWordsDictonary[key] = val

        return newAllWordsDictonary




    def RemoveBottomWordsInJobSearchDictsByPercentage(self, percantage):
        documentsInEachDirectory = {}
        newDirectoryDictonaries = {}

        for fileName in self.directoryNames:
            documentsInEachDirectory[fileName] = len(os.listdir(fileName))
            newDirectoryDictonaries[fileName] = {}

        for fileName in self.directoryNames:
            documents = int(documentsInEachDirectory[fileName])
            for key, val in self.WordDictionaries[fileName].items():
                if val >= round(documents * percantage / 100):
                    newDirectoryDictonaries[fileName][key] = val

        return newDirectoryDictonaries




    def RemoveBottomAllWordsDicByPercentage(self, percantage):
        newAllWordsDictonary = {}
        totalDocuments = 0

        for fileName in self.directoryNames:
            totalDocuments += len(os.listdir(fileName))

        for key, val in self.AllWordsDictonary.items():
            if val >= round(totalDocuments * percantage/100):
                newAllWordsDictonary[key] = val

        return newAllWordsDictonary




    def PrintDictionaries(self):
        print("Word Dictonaries:")
        print(self.WordDictionaries)

        print("Special Word Dictonaries")
        print(self.SpecialWordDictionaries)

        print("All Words Dictonary")
        print(self.AllWordsDictonary)

        print("All Special Words Dictonary")
        print(self.AllSpecialWordsDictonary)



    def YearsOfExperienceScentenceGenerator(self):
        for fileName in self.directoryNames:
            for jobText in self.JobTexts[fileName]:
                for scentence in re.split('\n|  |\.' , jobText):
                    if 'year' in scentence and 'degree' not in scentence:
                        newScentence = self.YOETextCleaner(scentence)
                        self.YOEText[fileName].append(newScentence)


    def YOETextCleaner(self, scentence):
        redundentNumberRemovalScentence = re.sub('\(\d\)|\-\d|\s+', ' ', scentence)
        specialCharacterRemovalScentence = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ",redundentNumberRemovalScentence)
        scentenceWithoutNumberAsText = []

        for word in specialCharacterRemovalScentence.split():
            try:
                scentenceWithoutNumberAsText.append(str(w2n.word_to_num(word)))
            except:
                scentenceWithoutNumberAsText.append(word)
        newScentence = ' '.join(scentenceWithoutNumberAsText)

        return newScentence



    def ProcessYearsOfExperienceText(self):
        specialWordsFile = open('SpecialWords.txt', 'r', encoding="utf-8")

        # replacing end splitting the text
        # when newline ('\n') is seen.
        specialWords = specialWordsFile.read().splitlines()

        for fileName in self.directoryNames:
            for scentence in self.YOEText[fileName]:
                blankYears = re.findall('\d year', scentence)
                specialWordsArray = []
                for keyword in specialWords:
                    if keyword in scentence:
                        specialWordsArray.append(keyword)
                yearLength= len(blankYears)
                wordArrayLen = len(specialWordsArray)
                if yearLength > 0 and wordArrayLen > 0:
                    for year in blankYears:
                        for specialWord in specialWordsArray:
                            phrase = year + 's of experience in'

                            if self.YOEDictionaries[fileName].get(phrase) is None:
                                self.YOEDictionaries[fileName][phrase] = {}
                            if self.YOEAllPhraseDictonary.get(phrase) is None:
                                self.YOEAllPhraseDictonary[phrase] = {}

                            if specialWord in self.YOEDictionaries[fileName][phrase]:
                                self.YOEDictionaries[fileName][phrase][specialWord] += 1
                            else:
                                self.YOEDictionaries[fileName][phrase][specialWord] = 1

                            if specialWord in self.YOEAllPhraseDictonary[phrase]:
                                self.YOEAllPhraseDictonary[phrase][specialWord] += 1
                            else:
                                self.YOEAllPhraseDictonary[phrase][specialWord] = 1



        specialWordsFile.close()


    def ReturnWordDictionaries(self):
        return self.WordDictionaries

    def ReturnAllWordsDictonaries(self):
        return self.AllWordsDictonary

    def ReturnSpecialWordDictionaries(self):
        return self.SpecialWordDictionaries

    def ReturnAllSpecialWordsDictonary(self):
        return self.AllSpecialWordsDictonary

    def ReturnYOEAllPhraseDictonary(self):
        return self.YOEAllPhraseDictonary
