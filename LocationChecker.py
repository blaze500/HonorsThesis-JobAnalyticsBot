import os
import csv

#https://stackoverflow.com/questions/17308872/check-whether-string-is-in-csv

def isCity(city):

    reader = csv.reader(open('US_City_And_States/' + city[0].upper() + '_Cities_PlusTheirStates.csv', 'rt'), delimiter=',')
    for row in reader:
        if city == row[0]:
            return True
    return False

def isState(state):
    reader = csv.reader(open('US_City_And_States/US_States.csv', 'rt'), delimiter=',')
    for row in reader:
        if state == row[0]:
            return True
    return False

def isLocation(location):
    reader = csv.reader(open('US_City_And_States/' + location[0].upper() + '_Cities_PlusTheirStates.csv', 'rt'), delimiter=',')
    for row in reader:
        if location == row:
            return True
    return False
