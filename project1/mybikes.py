'''
Eric Nguyen
Github: Nooj45
CS 1656
Professor Alexandros Labrinidis
Assignment 1
'''
import sys
import requests as req
import json
import math
from math import cos, asin, sqrt

def total_bikes():
    sumBikes = 0
    #looking through each dict in the list stationData and summing up num_bikes_available
    for numBikes in stationData:
        count = numBikes['num_bikes_available']
        sumBikes += count
    return sumBikes
# same as total_bikes except with num_docks_available
def total_docks():
    sumDocks = 0
    for numDocks in stationData:
        count = numDocks['num_docks_available']
        sumDocks += count
    return sumDocks
# look through stationData and find the correct stationId given by param
# once found calculate percentage (docks/(docks + bikes)) * 100 and return that value
def percent_avail(stationId):
    percentage = 0
    for isStation in stationData:
        if isStation['station_id'] == stationId:
            percentage = (isStation['num_docks_available'])/(isStation['num_docks_available'] + isStation['num_bikes_available'])
            percentage *= 100
            break
    return math.floor(percentage)

def closest_stations(lat, lon):
    # dictionary of stations to hold (stationIds: distance from given params) (key: values)
    stationDict = {}
    for i in range(len(stationInfo)):
        isClosest = distance(lat, lon, stationInfo[i]['lat'], stationInfo[i]['lon'])
        stationDict[stationInfo[i]['station_id']] = isClosest

    # sorted stationDict so that the top 3 are at the beginning
    # this returns a list of tuples sorted by the second element in the tuple (distance)
    sortedDict = sorted(stationDict.items(), key = lambda i: i[1])

    #returning list of strings w/ top 3 ids and names
    topList = [sortedDict[0][0], sortedDict[1][0], sortedDict[2][0]]
    index = 0
    '''
    topList isn't in order when looping to search for name, we could've 
    skipped it already, so keeping it in a while to keep restarting
    until we find it
    '''
    while True:
        for x in stationInfo:
            if x['station_id'] == topList[index]:
                topList.append(x['name'])
                index += 1
        if index == 3:
            break
    return topList

def closest_bike(lat, lon):
    # getting all data with available bikes
    filteredStationData = []
    for i in range(len(stationData)):
        if stationData[i]['num_bikes_available'] > 0:
            filteredStationData.append(stationData[i])
    
    filteredStationInfo = []
    i = 0
    for stations in stationInfo:
        if stations['station_id'] == filteredStationData[i]['station_id']:
            filteredStationInfo.append(stations)
            i += 1
            if i == len(filteredStationData):
                break
    
    closestAvailBike = {}
    for i in range(len(filteredStationInfo)):
        isClosest = distance(lat, lon, filteredStationInfo[i]['lat'],filteredStationInfo[i]['lon'])
        closestAvailBike[filteredStationInfo[i]['station_id']] = isClosest
    
    sortedBike = sorted(closestAvailBike.items(), key = lambda i: i[1])
    returnedBike = []
    for i in range(len(filteredStationInfo)):
        if filteredStationInfo[i]['station_id'] == sortedBike[0][0]:
            returnedBike.append(filteredStationInfo[i]['station_id'])
            returnedBike.append(filteredStationInfo[i]['name'])
            break
    return returnedBike

# distance function given to us
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))

def printOutput(command, param, outputValue):
    print('Command={0}\nParameters={1}'.format(command, param))
    print('Output=', end = '')

    if command == 'closest_stations':
        print('\n' + outputValue)
    elif command == 'percent_avail':
        print('{0}%'.format(outputValue))
    else:
        print(outputValue)
    return

# getting URLs into string format
baseURL = sys.argv[1]
station_infoURL = baseURL + 'station_information.json'
station_statusURL = baseURL + 'station_status.json'

# request to api to get information
data_request = req.get(station_statusURL)
data_request2 = req.get(station_infoURL)

# 200 = success so load contents as json format
if data_request.status_code == 200 & data_request.status_code == 200:
    jsonData = json.loads(data_request.content)
    jsonData2 = json.loads(data_request2.content)
else: #if failed then exit program
    print("Error with request to API! Exiting...")
    exit()

# setting values into variables to use
# stationData for total_bikes, total_docks, & percent_avail
# stationInfo is for closest_stations & closest_bike
stationData = jsonData['data']['stations']
stationInfo = jsonData2['data']['stations']

# checking command line arguments to decide which func. to run
if len(sys.argv) == 3: # total_bikes() and total_docks() only have 3 arg. in command line
    if sys.argv[2] == 'total_bikes':
        totalBikes = total_bikes()
        printOutput(sys.argv[2], '', totalBikes)
    elif sys.argv[2] == 'total_docks':
        totalDocks = total_docks()
        printOutput(sys.argv[2], '', totalDocks)
    else:
        print('Invalid command-line arguments for total_bikes and total_docks')
elif len(sys.argv) == 4: # percent_avail() takes 1 command line argument (station_id)
    if sys.argv[2] == 'percent_avail':
        percentage = percent_avail(sys.argv[3])
        printOutput(sys.argv[2], sys.argv[3], percentage)
    else:
        print('Invalid command-line arguments for percent_avail')
elif len(sys.argv) == 5: # closest_stations() and closest_bike() take 2 command line arguments (coordinates)
    if sys.argv[2] == 'closest_stations':
        top3 = closest_stations(float(sys.argv[3]), float(sys.argv[4]))
        top3Str = '{0}, {3}\n{1}, {4}\n{2}, {5}'.format(top3[0],top3[1],top3[2],top3[3],top3[4],top3[5])
        combinedParam = sys.argv[3] + ' ' +  sys.argv[4]
        printOutput(sys.argv[2], combinedParam, top3Str)
    elif sys.argv[2] == 'closest_bike':
        closestBike = closest_bike(float(sys.argv[3]), float(sys.argv[4]))
        bikeStr = '{0}, {1}'.format(closestBike[0], closestBike[1])
        combinedParam = sys.argv[3] + ' ' +  sys.argv[4]
        printOutput(sys.argv[2], combinedParam, bikeStr)
    else:
        print('Invalid command-line arguments for closest_stations and closest_bike')
else:
    print("Invalid number of arguments")
