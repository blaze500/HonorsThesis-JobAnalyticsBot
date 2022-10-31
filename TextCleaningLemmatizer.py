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
import html2text
import nltk
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords.words('english')
import re
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet


class TextCleaningLemmatizer:

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def nltk_pos_tagger(self, nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:
            return None


    def lemmatize_sentence(self, sentence):
        nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
        wordnet_tagged = map(lambda x: (x[0], self.nltk_pos_tagger(x[1])), nltk_tagged)
        lemmatized_sentence = []

        for word, tag in wordnet_tagged:
            if tag is None:
                lemmatized_sentence.append(word)
            else:
                lemmatized_sentence.append(self.lemmatizer.lemmatize(word, tag))
        return " ".join(lemmatized_sentence)

    def nounKeeper(self, sentence):
        nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))
        print(nltk_tagged)
        wordnet_tagged = map(lambda x: (x[0], self.nltk_pos_tagger(x[1])), nltk_tagged)
        lemmatized_sentence = []

        for word, tag in wordnet_tagged:
            if tag is wordnet.NOUN:
                lemmatized_sentence.append(word)
        return " ".join(lemmatized_sentence)
