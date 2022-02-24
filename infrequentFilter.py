# -------------------------------------------------------
# Assignment 2
# Written by Teng Zhao 40089560
# For COMP 472 Section AJ-X – Summer 2021
# --------------------------------------------------------

import model
import test


def freq_filter(modFile, resFile, revDictModel, posDictModel, negDictModel, revList):
    # Build the naive bayes classifier model for minus X Frequency

    modelReturn = model.build_model(posDictModel, negDictModel, revDictModel)
    posProbDictModel = modelReturn[0]
    negProbDictModel = modelReturn[1]
    pos_prob = modelReturn[2]
    neg_prob = modelReturn[3]
    precision_counter = 0
    recall_counter = 0

    modCounter = 1

    for word in revDictModel:
        tempString = "No." + str(modCounter) + " " + word + "\n"
        if word in posDictModel:
            tempString = tempString + str(posDictModel[word]) + ", " \
                         + str(posProbDictModel[word]) + ", "
        else:
            tempString = tempString + str(0) + ", " + str(posProbDictModel[word]) + ", "
        if word in negDictModel:
            tempString = tempString + str(negDictModel[word]) + ", " \
                         + str(negProbDictModel[word]) + "\n"
        else:
            tempString = tempString + str(0) + ", " + str(negProbDictModel[word]) + "\n"
        modFile.write(tempString)
        modCounter += 1

    modFile.write("\n" + "--------------------------------------------------" + "\n")

    resCounter = 1

    for review in revList:
        # Add title
        tempString = "No. " + str(resCounter) + " " + review.title + "\n"
        scoresRes = test.test_scores(review, posProbDictModel, negProbDictModel, pos_prob, neg_prob)
        # Add P(ri|positive), P(ri|negative)
        tempString = tempString + str(scoresRes[0]) + ", " + str(scoresRes[1]) + ", "
        # Compute my Result from scores
        if scoresRes[0] > scoresRes[1]:
            myRes = "positive"
        else:
            myRes = "negative"
        # Get actual result
        if review.rating >= 8:
            corrRes = "positive"
        else:
            corrRes = "negative"
        # Prediction is right or wrong
        if myRes == corrRes and myRes == "positive":
            pred = "right"
            precision_counter += 1
        elif myRes == corrRes and myRes == "negative":
            pred = "right"
            recall_counter += 1
        else:
            pred = "wrong"
        # Add myResult, correctResult, and prediction to string
        tempString = tempString + myRes + ", " + corrRes + ", " + pred + "\n"
        resFile.write(tempString)
        resCounter += 1

    # Computer and print prediction correctness in F measure with weight = 1
    if ((1 * precision_counter) + recall_counter) == 0:
        predCorr = "undefined"
    else:
        predCorr = ((1 + 1) * precision_counter * recall_counter) / ((1 * precision_counter) + recall_counter)
    resFile.write("\n" + "The prediction correctness (F measure) is " + str(predCorr))
    resFile.write("\n" + "--------------------------------------------------" + "\n")

    return predCorr, (modCounter - 1)