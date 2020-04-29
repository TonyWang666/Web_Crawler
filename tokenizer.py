import os
import re
import sys
import time
import scraper
from itertools import islice

STOP_WORDS = set(["a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was", "will", "with"])
# O(n*logn)

# O(n)
# this function reads a text file and return a list of the tokens in the file
def tokenize(filename: str) -> [str]:
    tokens = []
    with open(filename, 'r') as file:  # handle open and close file
        whole_file = file.read()  # read file
        tokens += [token.lower() for token in re.split('[^a-zA-Z0-9]', whole_file) if len(token) > 3 and token not in STOP_WORDS]
        # split the line by non-alphanumeric characters, and add tokens (len > 1) to the list
    return tokens


# O(n)
# take a list and return the word counts
def computeWordFrequencies(tokens: [str]) -> {str: int}:
    scraper.maxWordLock.acquire()
    token_map = {}
    for token in tokens:
        if token in token_map:
            token_map[token] += 1
        else:
            token_map[token] = 1
        if token in scraper.totalWordFreq:
            scraper.totalWordFreq[token] += 1
        else:
            scraper.totalWordFreq[token] = 1
    scraper.maxWordLock.release()
    return token_map

# 
# get 50 most frequent words over all the pages
def get50MostWords(token_map: {str: int}):
    sort_tokens = sorted(token_map.items(), key=lambda x: x[1], reverse=True)
    return list(islice(token_map.keys(), 50))

# O(n*logn)
# sort the dict by values and print
def printFrequencies(token_map: {str: int}):
    sort_tokens = sorted(token_map.items(), key=lambda x: x[1], reverse=True)
    for token, count in sort_tokens:
        print(token, "-", count)


# O(n)
# main function. 
def main():
    if len(sys.argv) == 2:
        f_name = sys.argv[1]
        if os.path.isfile(f_name):
            try:
                tok = tokenize(f_name)
                word_frequencies = computeWordFrequencies(tok)
                printFrequencies(word_frequencies)
            except:
                print('please enter a valid file')
                sys.exit()
        else:
            print('Error: file does not exist')
            sys.exit()
    else:
        print('Please enter one file name')
        sys.exit()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
