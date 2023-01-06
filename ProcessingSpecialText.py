import os

class TextProcessor:

    #Starts the Program
    def __init__(self):

        self.directoryNames = ["HandshakeJobText", "IndeedJobText", "LinkedinJobText"]

        # An array which contains the dictionaries for each job website
        self.WordDictionaries = [{} for x in self.directoryNames]
        print(self.WordDictionaries)
        # An array which contains the arrays of each job website
        self.JobTexts = {}

    def TextFilesToJobTextArrays(self):

        for fileName in self.directoryNames:
            directoryJobTexts=[]
            for textFilePath in os.listdir(fileName):
                with open(os.path.join(fileName, textFilePath), 'r', encoding="utf-8") as jobDescription:
                    jobDescriptionText = jobDescription.read().lower()
                    jobDescriptionTextByLine = jobDescriptionText.split("\n")
                    directoryJobTexts.append(jobDescriptionTextByLine)
            self.JobTexts[fileName] = directoryJobTexts

        print(self.JobTexts)



    def WordCounterAlgorithm(self):

        for fileName in self.directoryNames:
            for jobText in self.JobTexts[fileName]:
                for sentence in jobText:
                    self.JobTexts[fileName] = self.specialWordFinder(sentence)


        print("boofa")



    def SpecialWordCounterAlgorithm(self):

        for fileName in self.directoryNames:
            for jobText in self.JobTexts[fileName]:
                for sentence in jobText:
                    self.JobTexts[fileName] = self.specialWordFinder(sentence)


        print("boofa")


    def specialWordFinder(self, text):
        textSplitInto = 1
        specialWordsFile = open('SpecialWords.txt', 'r', encoding="utf-8")

        # replacing end splitting the text
        # when newline ('\n') is seen.
        specialWords = specialWordsFile.readlines()
        print(specialWords)

        for word in specialWords:
            splitText = text.split(word)
            wordsRemoved = len(splitText)-1
            newTextWithWordRemoved = ''.join(splitText)
            text=newTextWithWordRemoved
        print(text)
        specialWordsFile.close()
        return text


# check for ____ years of experience and if a "special" word is in the scentence