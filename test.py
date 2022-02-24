# -------------------------------------------------------
# Assignment 2
# Written by Teng Zhao 40089560
# For COMP 472 Section AJ-X – Summer 2021
# --------------------------------------------------------

import math


# score(Ci) = log(P(Ci)) + sum all (log(P(Wi|Ci)) || log is based 10
def test_scores(review, posDictModel, negDictModel, posProb, negProb):

    # score(Positive) = log(P(Positive)) + log(P(Wi|Positive)
    score_positive = math.log10(float(posProb))
    # score(Negative) = log(P(Negative)) + log(P(Wi|Negative)
    score_negative = math.log10(float(negProb))

    for word in review.text:

        if word in posDictModel:
            score_positive = score_positive + math.log10(posDictModel[word])

        if word in negDictModel:
            score_negative = score_negative + math.log10(negDictModel[word])

    return score_positive, score_negative
