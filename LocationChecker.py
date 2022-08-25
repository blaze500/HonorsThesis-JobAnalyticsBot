import os
import csv

#https://stackoverflow.com/questions/17308872/check-whether-string-is-in-csv
reader = csv.reader(open('CitiesAndStates.csv', 'rt'), delimiter=',')

def isCity(city):
    for row in reader:
        if city == row[0]:
            return True
    return False

def isState(state):
    for row in reader:
        if state == row[1]:
            return True
    return False

def isLocation(location):
    for row in reader:
        if location == row:
            return True
    return False
