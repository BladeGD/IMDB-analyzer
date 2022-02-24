# -------------------------------------------------------
# Assignment 2
# Written by Teng Zhao 40089560
# For COMP 472 Section AJ-X – Summer 2021
# --------------------------------------------------------

def review_to_dictionary(review_list, dictionary):
    for review in review_list:
        paragraph = review.text.split()

        # Strip apostrophes from beginning and end of words
        i = 0
        for word in paragraph:
            if word.startswith("'") and word.endswith("'"):
                paragraph[i] = word[1:-1]
            elif word.startswith("'"):
                paragraph[i] = word[1:len(word)]
            elif word.endswith("'"):
                paragraph[i] = word[len(word):-1]
            i += 1

        # Repeat twice for double quotes
        i = 0
        for word in paragraph:
            if word.startswith("'") and word.endswith("'"):
                paragraph[i] = word[1:-1]
            elif word.startswith("'"):
                paragraph[i] = word[1:len(word)]
            elif word.endswith("'"):
                paragraph[i] = word[len(word):-1]
            i += 1

        # Eliminate duplicate words in same review
        paragraph = list(dict.fromkeys(paragraph))

        # print(paragraph)

        for word in paragraph:
            if word != '':
                if word in dictionary:
                    dictionary[word] += 1
                else:
                    dictionary[word] = 1

    return dictionary
