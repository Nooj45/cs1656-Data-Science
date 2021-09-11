import re
import sys
import csv
import math
from itertools import combinations
from itertools import permutations
from string import punctuation

# Eric Nguyen
# Assignment 4 - Association Mining Rule
# For some reason mine prints out not in the same order, but it prints all the sets and then the rules
# i tried sorted() but it doesn't seem like it's working so I gave up on sorting it

#Get the command line arguments
input = sys.argv[1]
output = sys.argv[2]
min_support_percentage = sys.argv[3]
min_confidence = sys.argv[4]

#Read in line by line
with open(input) as f:
    content = f.readlines()

#Format the series of letters
result = ''.join(i for i in content if not i.isdigit())
output = re.sub(r'\d+', '', result)
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''

# putting them together w/o any punctuations
no_punct = ""
for char in output:
    if char not in punctuations:
        no_punct = no_punct + char

letters = []
for c in no_punct:
    if c not in letters:
        letters.insert(len(letters), c)

letters.remove('\n')

cfi = []
#Get the different combinations
for i in range(len(letters)):
    if i is not 0:
        for p in combinations(letters, i):
            cfi.insert(len(cfi), p)

versusLine = []
#Insert each no_punct line in
for line in no_punct.splitlines():
    versusLine.insert(len(versusLine), line)

calculate = {}
against = 0
#loop to check if our set is exisiting and calculate. then put in list calculate
for line in versusLine:
    sizeLine = len(line)

    for k in cfi:
        against = 0
        sizeK = len(k)

        if sizeK <= sizeLine:
            for c in k:
                if c in line:
                    against += 1

            if against == sizeK:
                add = "".join([str(c) for c in k])

                if add not in calculate:
                    calculate[add] = 1
                elif add in calculate:
                    calculate[add] += 1

#Output to .csv file with formatting
outputFile = 'output.sup=%s,conf=%s.csv' % (min_support_percentage, min_confidence)
with open(outputFile, 'w') as csvfile:
    outputwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE, escapechar=' ')

    vfi = {}
    for i in calculate:
        support_percentage = float(calculate[i] / float(len(versusLine)))
        if support_percentage >= float(min_support_percentage):
            i = sorted(i)
            i = str(i)
            
            # this line basically says to translate nothing to nothing (1st 2 params) and then translate
            # any punctuation or numbers to None, so basically removing puncuations, appears in other parts later on
            i = i.translate(str.maketrans('','','''!()-[]{};:'"\,<>/?@#$%^&*_~ '''))
            vfi[i] = support_percentage

            # rounding to 4 decimal places, converts to str as well
            support_percentage = '%.4f' % (support_percentage)
            #print("S, %s, %s" % (support_percentage, i))

            y = ",".join(map(str, i))
            # outputting the sets
            outputwriter.writerow(['S'] + [support_percentage] + [y])

    catchDouble = []

    #Go through and get our different permutations, then check against each case then output to .csv file
    for i in vfi:
        if len(i) > 1:
            for p in permutations(i):
                add = "".join([str(c) for c in p])
                sizeAdd = len(add)

                partition = math.floor(float(sizeAdd) / 2)
                items1 = (add[0:int(partition)])
                items1 = sorted(items1)
                items2 = (add[int(partition):int(sizeAdd)])
                items2 = sorted(items2)
                items1 = str(items1)
                items1 = items1.translate(str.maketrans('','','''!()-[]{};:'"\,<>/?@#$%^&*_~ '''))
                items2 = str(items2)
                items2 = items2.translate(str.maketrans('','','''!()-[]{};:'"\,<>/?@#$%^&*_~ '''))
                # doing these for catching doubles later
                combineItems = items1 + '.' + items2
                combineItems2 = items2 + '.' + items1

                partition2 = math.ceil(float(sizeAdd) / 2)
                items3 = (add[0:int(partition2)])
                items3 = sorted(items3)
                items3 = str(items3)
                items3 = items3.translate(str.maketrans('','','''!()-[]{};:'"\,<>/?@#$%^&*_~ '''))
                items4 = (add[int(partition2):int(sizeAdd)])
                items4 = sorted(items4)
                items4 = str(items4)
                items4 = items4.translate(str.maketrans('','','''!()-[]{};:'"\,<>/?@#$%^&*_~ '''))
                combineItems3 = items3 + '.' + items4
                combineItems4 = items4 + '.' + items3

                #The combine items are to ensure that no repeats go into output
                if items1 in vfi:
                    if items2 in vfi:
                        if i in vfi:
                            # if not repeated then add it to the output
                            if combineItems not in catchDouble:
                                left = vfi[i] / vfi[items1]
                                # if greater than the minimum confidence then add to output, repeated for the others
                                if left >= float(min_confidence):
                                    left = '%.4f' % left
                                    support_percentage = '%.4f' % (vfi[i])
                                    x = ",".join(map(str, items1))
                                    y = ",".join(map(str, items2))
                                    outputwriter.writerow(['R'] + [support_percentage] + [left] + [x] + ['=>'] + [y])
                                # add to list of catchDoubles to check for other doubles
                                catchDouble.append(combineItems)

                            if combineItems2 not in catchDouble:
                                right = vfi[i] / vfi[items2]
                                if right >= float(min_confidence):
                                    right = '%.4f' % right
                                    support_percentage = '%.4f' % (vfi[i])
                                    x = ",".join(map(str, items1))
                                    y = ",".join(map(str, items2))
                                    outputwriter.writerow(['R'] + [support_percentage] + [right] + [y] + ['=>'] + [x])
                                catchDouble.append(combineItems2)

                            if combineItems3 not in catchDouble:
                                if items3 in vfi:
                                    left2 = vfi[i] / vfi[items3]
                                    if left2 >= float(min_confidence):
                                        left2 = '%.4f' % left2
                                        support_percentage = '%.4f' % (vfi[i])
                                        x = ",".join(map(str, items3))
                                        y = ",".join(map(str, items4))
                                        outputwriter.writerow(['R'] + [support_percentage] + [left2] + [x] + ['=>'] + [y])
                                        catchDouble.append(combineItems3)

                            if combineItems4 not in catchDouble:
                                if items4 in vfi:
                                    right2 = vfi[i] / vfi[items4]
                                    if right2 >= float(min_confidence):
                                        right2 = '%.4f' % right2
                                        support_percentage = '%.4f' % (vfi[i])
                                        x = ",".join(map(str, items3))
                                        y = ",".join(map(str, items4))
                                        outputwriter.writerow(['R'] + [support_percentage] + [right2] + [y] + ['=>'] + [x])
                                        catchDouble.append(combineItems4)