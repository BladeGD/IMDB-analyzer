# -------------------------------------------------------
# Assignment 2
# Written by Teng Zhao 40089560
# For COMP 472 Section AJ-X – Summer 2021
# --------------------------------------------------------

import random

import bs4
import csv
import re
import toDictionary
import model
import test
import infrequentFilter
import operator
import matplotlib.pyplot as plt
import numpy as np
from requests import get
from bs4 import BeautifulSoup
from collections import OrderedDict
from warnings import warn
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from decimal import getcontext, Decimal

# URL to be saved from CSV
urls = []


# Rating class
class Review:
    def __init__(self, text, rating, title):
        self.text = text
        self.rating = rating
        self.title = title

    def __str__(self):
        return "(" + str(self.rating) + ", " + str(self.text) + ", " + str(self.title) + ")"

    def __repr__(self):
        return self.__str__()


# Open CSV file
with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        urls.append(row[3])

# print(urls)
# print(len(urls))

# warn("Warning Simulation")

# List to store data
review_list = []
total = 0

# Loop monitoring
start_time = time()
requests = 0

# For all the url in the list
for url in urls:

    # Make a request
    response = get(url)

    # Pause loop
    sleep(randint(0, 1))

    # Monitor the requests
    requests += 1
    elapsed_time = time() - start_time
    print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
    clear_output(wait=True)

    # Throw a warning for non-200 status codes
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))

    # Parse the content of the request with BeautifulSoup
    page_html = BeautifulSoup(response.text, 'html.parser')

    # Select all the review containers from a single page
    review_containers = page_html.find_all('div', class_='lister-item mode-detail imdb-user-review collapsable')

    # Scrape the title
    title = page_html.h3.a.text

    # print(title)

    for container in review_containers:
        if container.find('span', class_='rating-other-user-rating') is not None:
            # Scrape the text
            text = container.find('div', class_='text show-more__control').text
            text = text.lower()
            text = re.sub("[^a-z'\\s]", '', text)

            # Scrape the rating
            rating = float(container.find('span', class_='rating-other-user-rating').span.text)

        review_list.append(Review(text, rating, title))

# print(review_list)
print("# of Reviews: " + str(len(review_list)))

# randomly shuffle all the reviews
# prevents using overly positive or negative episodes only as training model
random.shuffle(review_list)

# Lists for positive and negative review
positive_list = []
negative_list = []

for review in review_list:
    if review.rating >= 8:
        positive_list.append(review)
    else:
        negative_list.append(review)

print("# of Positive Reviews: " + str(len(positive_list)))
print("# of Negative Reviews: " + str(len(negative_list)))

# Separate positive reviews into model data list and test data list
middle = len(positive_list) // 2
positive_list_model = positive_list[:middle]
positive_list_test = positive_list[middle:]

# Separate negative reviews into model data list and test data list
middle = len(negative_list) // 2
negative_list_model = negative_list[:middle]
negative_list_test = negative_list[middle:]

# Model total review list
review_list_model = (positive_list_model + negative_list_model)

# Test total review list
review_list_test = (positive_list_test + negative_list_test)

print("# of Test Reviews: " + str(len(review_list_test)))
print("# of Positive Test Reviews: " + str(len(positive_list_test)))
print("# of Negative Test Reviews: " + str(len(negative_list_test)))

# print(positive_list_model)
# print(negative_list_model)

# print(review_list_model)
# print(review_list_test)

# print(positive_list)
# print(negative_list)

# hash map for compare no doubles in review before slapping in global hashmap for chance computation

# Dictionaries for positive and negative reviews.
positiveDictModel = {}
negativeDictModel = {}

# Dictionary for total reviews model
reviewDictModel = {}

# Insert words from positive review into positive dictionary
positiveDictModel = toDictionary.review_to_dictionary(positive_list_model, positiveDictModel)

# Insert words from negative review into negative dictionary
negativeDictModel = toDictionary.review_to_dictionary(negative_list_model, negativeDictModel)

# Insert words from all reviews into a total dictionary
reviewDictModel = toDictionary.review_to_dictionary(review_list_model, reviewDictModel)

# print(positiveDictModel)
# print(negativeDictModel)
# print(reviewDictModel)

# Open stop word text file and put in list
stopWords = open("stopword.txt", "r")

stopWordList = []

for line in stopWords:
    word = line.strip()
    stopWordList.append(word)

stopWords.close()

# print(stopWordList)

# Delete stop words from Dictionaries
removedWords = []
for word in stopWordList:
    deleted = False
    if word in positiveDictModel:
        del positiveDictModel[word]
        deleted = True
    if word in negativeDictModel:
        del negativeDictModel[word]
        deleted = True
    if word in reviewDictModel:
        del reviewDictModel[word]
        deleted = True
    if deleted:
        removedWords.append(word)

removeFile = open("remove.txt", "w")
for word in removedWords:
    removeFile.write(word + "\n")
removeFile.write("\n" + "------------------------------" + "\n")

# Sort dictionaries in alphabetical order

positiveDictModel = OrderedDict(sorted(positiveDictModel.items()))
negativeDictModel = OrderedDict(sorted(negativeDictModel.items()))
reviewDictModel = OrderedDict(sorted(reviewDictModel.items()))

# print(positiveDictModel)
# print(negativeDictModel)
# print(reviewDictModel)

# Build the naive bayes classifier model
modelReturn = model.build_model(positiveDictModel, negativeDictModel, reviewDictModel)
wordPosProbDictModel = modelReturn[0]
wordNegProbDictModel = modelReturn[1]
pos_probability = modelReturn[2]
neg_probability = modelReturn[3]

# print(model.wordPositiveProbabilityDictModel)
# print(model.wordNegativeProbabilityDictModel)

# Write model to model.txt
modelFile = open("model.txt", "w")
modelCounter = 1

for word in reviewDictModel:
    tempString = "No." + str(modelCounter) + " " + word + "\n"
    if word in positiveDictModel:
        tempString = tempString + str(positiveDictModel[word]) + ", " \
                     + str(wordPosProbDictModel[word]) + ", "
    else:
        tempString = tempString + str(0) + ", " + str(wordPosProbDictModel[word]) + ", "
    if word in negativeDictModel:
        tempString = tempString + str(negativeDictModel[word]) + ", " \
                     + str(wordNegProbDictModel[word]) + "\n"
    else:
        tempString = tempString + str(0) + ", " + str(wordNegProbDictModel[word]) + "\n"
    modelFile.write(tempString)
    modelCounter += 1

modelFile.close()

# Test the reviews with the naive bays classifier model
resultFile = open("result.txt", "w")
resultCounter = 1
precisionCounter = 0
recallCounter = 0

for review in review_list_test:
    # Add title
    tempString = "No. " + str(resultCounter) + " " + review.title + "\n"
    scores = test.test_scores(review, wordPosProbDictModel, wordNegProbDictModel, pos_probability, neg_probability)
    # Add P(ri|positive), P(ri|negative)
    tempString = tempString + str(scores[0]) + ", " + str(scores[1]) + ", "

    # Compute my Result from scores
    if scores[0] > scores[1]:
        myResult = "positive"
    else:
        myResult = "negative"

    # Get actual result
    if review.rating >= 8:
        correctResult = "positive"
    else:
        correctResult = "negative"

    # Prediction is right or wrong
    if myResult == correctResult and myResult == "positive":
        prediction = "right"
        precisionCounter += 1
    elif myResult == correctResult and myResult == "negative":
        prediction = "right"
        recallCounter += 1
    else:
        prediction = "wrong"

    # Add myResult, correctResult, and prediction to string
    tempString = tempString + myResult + ", " + correctResult + ", " + prediction + "\n"
    resultFile.write(tempString)
    resultCounter += 1

# Computer and print prediction correctness
if ((1 * precisionCounter) + recallCounter) == 0:
    predictionCorrectness = "undefined"
else:
    predictionCorrectness  = ((1 + 1) * precisionCounter * recallCounter) / ((1 * precisionCounter) + recallCounter)
resultFile.write("\n" + "The prediction correctness (F measure) is " + str(predictionCorrectness))

resultFile.close()

print("-----------------------------------")
print("Done!")
print("Prediction F Measure: " + str(predictionCorrectness))
print("# of words in model: " + str(modelCounter - 1))

# ----------------------------------------------------------------------------------------------------------------------
# Open Frequency txt files
modelFile = open("frequency-model.txt", "w")
resultFile = open("frequency-result.txt", "w")
# ----------------------------------------------------------------------------------------------------------------------
# Remove word Frequency = 1
m1FDictModel = reviewDictModel.copy()
m1FPosDictModel = positiveDictModel.copy()
m1FNegDictModel = negativeDictModel.copy()

removedWords = []
i = 0
for word in list(reviewDictModel):
    if m1FDictModel[word] == 1:
        del m1FDictModel[word]
        if word in m1FPosDictModel:
            del m1FPosDictModel[word]
        if word in m1FNegDictModel:
            del m1FNegDictModel[word]
        removedWords.append(word)

removeFile.write("\n" + "Remove word Frequency = 1" + "\n")

for word in removedWords:
    removeFile.write(word + "\n")
removeFile.write("\n" + "------------------------------" + "\n")

resultFile.write("\n" + "Remove word Frequency = 1" + "\n")

m1Result = infrequentFilter.freq_filter(modelFile, resultFile, m1FDictModel,
                                        m1FPosDictModel, m1FNegDictModel, review_list_test)

print("-----------------------------------")
print("Done Minus 1 Frequency!")
print("Prediction Prediction F Measure: " + str(m1Result[0]))
print("# of words in model: " + str(m1Result[1]))

# ----------------------------------------------------------------------------------------------------------------------
# Remove word Frequency <= 10
m10FDictModel = reviewDictModel.copy()
m10FPosDictModel = positiveDictModel.copy()
m10FNegDictModel = negativeDictModel.copy()

removedWords = []
i = 0
for word in list(reviewDictModel):
    if m10FDictModel[word] <= 10:
        del m10FDictModel[word]
        if word in m10FPosDictModel:
            del m10FPosDictModel[word]
        if word in m10FNegDictModel:
            del m10FNegDictModel[word]
        removedWords.append(word)

removeFile.write("\n" + "Remove word Frequency <= 10" + "\n")

for word in removedWords:
    removeFile.write(word + "\n")
removeFile.write("\n" + "------------------------------" + "\n")

resultFile.write("\n" + "Remove word Frequency <= 10" + "\n")

m10Result = infrequentFilter.freq_filter(modelFile, resultFile, m10FDictModel,
                                         m10FPosDictModel, m10FNegDictModel, review_list_test)

print("-----------------------------------")
print("Done Minus 10 or less Frequency!")
print("Prediction Prediction F Measure: " + str(m10Result[0]))
print("# of words in model: " + str(m10Result[1]))

# ----------------------------------------------------------------------------------------------------------------------
# Remove word Frequency <= 20
m20FDictModel = reviewDictModel.copy()
m20FPosDictModel = positiveDictModel.copy()
m20FNegDictModel = negativeDictModel.copy()

removedWords = []
i = 0
for word in list(reviewDictModel):
    if m20FDictModel[word] <= 20:
        del m20FDictModel[word]
        if word in m20FPosDictModel:
            del m20FPosDictModel[word]
        if word in m20FNegDictModel:
            del m20FNegDictModel[word]
        removedWords.append(word)

removeFile.write("\n" + "Remove word Frequency <= 20" + "\n")

for word in removedWords:
    removeFile.write(word + "\n")
removeFile.write("\n" + "------------------------------" + "\n")

resultFile.write("\n" + "Remove word Frequency <= 20" + "\n")

m20Result = infrequentFilter.freq_filter(modelFile, resultFile, m20FDictModel,
                                         m20FPosDictModel, m20FNegDictModel, review_list_test)

print("-----------------------------------")
print("Done Minus 20 or less Frequency!")
print("Prediction Prediction F Measure: " + str(m20Result[0]))
print("# of words in model: " + str(m20Result[1]))

# ----------------------------------------------------------------------------------------------------------------------
# Order reviewDictModel by descending values
perDictModel = reviewDictModel.copy()
sorted_tuples = sorted(perDictModel.items(), key=operator.itemgetter(1), reverse=True)
sorted_dict = OrderedDict()
for k, v in sorted_tuples:
    sorted_dict[k] = v
perDictModel = sorted_dict

# print(perDictModel)

# ----------------------------------------------------------------------------------------------------------------------
# Remove word Frequency top 5%
p5DictModel = perDictModel.copy()
p5PosDictModel = positiveDictModel.copy()
p5NegDictModel = negativeDictModel.copy()

removedWords = []
i = 0
dictSize = len(p5DictModel)
topRemove = (dictSize // 100) * 5
toRemove = list(perDictModel.keys())[:topRemove]

for word in toRemove:
    del p5DictModel[word]
    if word in p5PosDictModel:
        del p5PosDictModel[word]
    if word in p5NegDictModel:
        del p5NegDictModel[word]
    removedWords.append(word)

removeFile.write("\n" + "Remove word percentage top 5%" + "\n")

for word in removedWords:
    removeFile.write(word + "\n")
removeFile.write("\n" + "------------------------------" + "\n")

resultFile.write("\n" + "Remove word percentage top 5%" + "\n")

p5Result = infrequentFilter.freq_filter(modelFile, resultFile, p5DictModel,
                                        p5PosDictModel, p5NegDictModel, review_list_test)

print("-----------------------------------")
print("Done minus Top 5 most frequent!")
print("Prediction Prediction F Measure: " + str(p5Result[0]))
print("# of words in model: " + str(p5Result[1]))

# ----------------------------------------------------------------------------------------------------------------------
# Remove word Frequency top 10%
p10DictModel = perDictModel.copy()
p10PosDictModel = positiveDictModel.copy()
p10NegDictModel = negativeDictModel.copy()

removedWords = []
i = 0
dictSize = len(p10DictModel)
topRemove = (dictSize // 100) * 10
toRemove = list(perDictModel.keys())[:topRemove]

for word in toRemove:
    del p10DictModel[word]
    if word in p10PosDictModel:
        del p10PosDictModel[word]
    if word in p10NegDictModel:
        del p10NegDictModel[word]
    removedWords.append(word)

removeFile.write("\n" + "Remove word percentage top 10%" + "\n")

for word in removedWords:
    removeFile.write(word + "\n")
removeFile.write("\n" + "------------------------------" + "\n")

resultFile.write("\n" + "Remove word percentage top 10%" + "\n")

p10Result = infrequentFilter.freq_filter(modelFile, resultFile, p10DictModel,
                                         p10PosDictModel, p10NegDictModel, review_list_test)

print("-----------------------------------")
print("Done minus Top 10 most frequent!")
print("Prediction Prediction F Measure: " + str(p10Result[0]))
print("# of words in model: " + str(p10Result[1]))

# ----------------------------------------------------------------------------------------------------------------------
# Remove word Frequency top 20%
p20DictModel = perDictModel.copy()
p20PosDictModel = positiveDictModel.copy()
p20NegDictModel = negativeDictModel.copy()

removedWords = []
i = 0
dictSize = len(p20DictModel)
topRemove = (dictSize // 100) * 20
toRemove = list(perDictModel.keys())[:topRemove]

for word in toRemove:
    del p20DictModel[word]
    if word in p20PosDictModel:
        del p20PosDictModel[word]
    if word in p20NegDictModel:
        del p20NegDictModel[word]
    removedWords.append(word)

removeFile.write("\n" + "Remove word percentage top 20%" + "\n")

for word in removedWords:
    removeFile.write(word + "\n")
removeFile.write("\n" + "------------------------------" + "\n")

resultFile.write("\n" + "Remove word percentage top 20%" + "\n")

p20Result = infrequentFilter.freq_filter(modelFile, resultFile, p20DictModel,
                                         p20PosDictModel, p20NegDictModel, review_list_test)

print("-----------------------------------")
print("Done minus Top 20 most frequent!")
print("Prediction Prediction F Measure: " + str(p20Result[0]))
print("# of words in model: " + str(p20Result[1]))

# ----------------------------------------------------------------------------------------------------------------------
removeFile.close()
modelFile.close()
resultFile.close()
# ----------------------------------------------------------------------------------------------------------------------
# Plotting the graph of correctness vs # of words left in vocabulary
# pip install matplotlib
# pip install numpy

Decimal
# set precision
getcontext().prec = 4

# x axis values
x1 = np.array([Decimal(modelCounter - 1)])
x2 = np.array([Decimal(m1Result[1]), Decimal(m10Result[1]), Decimal(m20Result[1])])
x3 = np.array([Decimal(p5Result[1]), Decimal(p10Result[1]), Decimal(p20Result[1])])
# corresponding y axis values
y1 = np.array([int(predictionCorrectness)])
y2 = np.array([int(m1Result[0]), int(m10Result[0]), int(m20Result[0])])
y3 = np.array([int(p5Result[0]), int(p10Result[0]), int(p20Result[0])])

# scatter plot
plt.scatter(x1, y1, label="Basic Model")
plt.scatter(x2, y2, label="Least Frequency Removed")
plt.scatter(x3, y3, label="Top Frequency Percentage Removed")

# x axis name
plt.xlabel('Words left in Vocabulary')
# y axis name
plt.ylabel('Correctness Percentage (%)')

# graph title
plt.title('Correctness % Vs Vocabulary Size')

# display legend
plt.legend()

# show plot
plt.show()
