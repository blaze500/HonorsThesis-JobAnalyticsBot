import os
import shutil

def DeleteJobFiles(deleteStopWords):

    fileNames=['HandshakeJobsStopWordsText', 'HandshakeJobsText', 'IndeedJobsStopWordsText', 'IndeedJobsText', 'LinkedinJobsStopWordsText', 'LinkedinJobsText', 'HandshakeJobs.csv', 'HandshakeJobsStopWords.csv', 'IndeedJobs.csv', 'IndeedJobsStopWords.csv', 'LinkedinJobs.csv', 'LinkedinJobsStopWords.csv', 'SpecialWords.txt']
    for file in fileNames:
        if os.path.exists(file):
            # Due to windows giving a "[WinError 5] Access is denied python" for os.remove in python
            # due to it needing permissions, sometimes the folders need to be deleted by shutil.rmtree
            try:
                os.remove(file)
            except:
                shutil.rmtree(file)

    if deleteStopWords:
        if os.path.exists('stopwords.txt'):
            os.remove('stopwords.txt')
