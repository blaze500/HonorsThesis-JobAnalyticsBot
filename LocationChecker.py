import csv

#https://stackoverflow.com/questions/17308872/check-whether-string-is-in-csv


def isCity(city):
    if city[0].isalpha() is False or city[0] == ' ':
        return False
    reader = csv.reader(open('US_City_And_States/' + city[0].upper() + '_Cities_PlusTheirStates.csv', 'rt'), delimiter=',')
    for row in reader:
        if city == row[0]:
            return True
    return False

def isState(state):
    if state[0].isalpha() is False or state[0] == ' ':
        return False
    reader = csv.reader(open('US_City_And_States/US_States.csv', 'rt'), delimiter=',')
    for row in reader:
        if state == row[0]:
            return True
    return False

def isLocation(location):
    if location[0].isalpha() is False or location[0] == ' ':
        return False
    reader = csv.reader(open('US_City_And_States/' + location[0].upper() + '_Cities_PlusTheirStates.csv', 'rt'), delimiter=',')
    for row in reader:
        cityAndStateLocation = row[0] +',' + row[1]
        if location == cityAndStateLocation:
            return True
    return False
