# -------------------------------------------------------
# Assignment 2
# Written by Teng Zhao 40089560
# For COMP 472 Section AJ-X – Summer 2021
# --------------------------------------------------------

def build_model(pDictModel, nDictModel, wDictModel):
    # P(Wi|Positive)
    wordPositiveProbabilityDictModel = {}
    # P(Wi|Negative)
    wordNegativeProbabilityDictModel = {}
    # P(Positive) || P(Ci), Ci = Positive
    positive_probability = None
    # P(Negative) || P(Ci), Ci = Negative
    negative_probability = None

    # Count total of words in each dictionary type
    totalWordCountPositiveModel = sum(pDictModel.values())
    totalWordCountNegativeModel = sum(nDictModel.values())

    # Count total number of keys in each dictionary type
    totalKeyCountPositiveModel = len(pDictModel)
    totalKeyCountNegativeModel = len(nDictModel)

    # Count total of words in dictionary
    totalWordCountModel = sum(wDictModel.values())

    # P(Positive) || P(Ci), Ci = Positive
    positive_probability = totalWordCountPositiveModel / totalWordCountModel
    # print(positive_probability)
    # P(Negative) || P(Ci), Ci = Negative
    negative_probability = totalWordCountNegativeModel / totalWordCountModel
    # print(negative_probability)

    smoothingC = 1

    for word in wDictModel:

        if word in pDictModel:
            wordPositiveProbabilityDictModel[word] = \
                (int(pDictModel[word]) + smoothingC) / (totalWordCountPositiveModel
                                                        + (totalKeyCountPositiveModel * smoothingC))
        else:
            wordPositiveProbabilityDictModel[word] = smoothingC / (totalWordCountPositiveModel
                                                                   + (totalKeyCountPositiveModel * smoothingC))

        if word in nDictModel:
            wordNegativeProbabilityDictModel[word] = \
                (int(nDictModel[word]) + smoothingC) / (totalWordCountNegativeModel
                                                        + (totalKeyCountNegativeModel * smoothingC))
        else:
            wordNegativeProbabilityDictModel[word] = smoothingC / (totalWordCountPositiveModel
                                                                   + (totalKeyCountPositiveModel * smoothingC))

    return wordPositiveProbabilityDictModel, wordNegativeProbabilityDictModel\
        , positive_probability, negative_probability
