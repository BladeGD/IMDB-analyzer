# IMDB Review Analyzer
Fulfilled in the schope of COEN472 Artificial Intelligence at Concordia University

### Goal
Scrap dataset from IMDB and create a Naïve Bays Classifier model to predict if a review is positive (=< 8/10) or a negative review (> 8/10) based on the words within the review body.

### Features
* Infrequent word filtering for frequency = 1, =< 10, =< 20, and most frequent top 5%, 10%, 20%, found in  frequency-result.txt
* Word Smoothing Filtering 𝛿 = 1.6 in smooth-result.txt
* Word Length Filtering gradually remove all words with length ≤ 2, length ≤ 4, and all words with length ≥ 9 in length-result.txt
