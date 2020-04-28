import numpy as np
from tokenizer import computeWordFrequencies, tokenize 
import scraper
BITS = 200

global maxNum
maxNum = 0
# Input:  dict with <word, frequency>
# Output: dict with <word, 200Binary>
# Action: transform word dictionary to binary dictionary
def toBinaryMap(wordFreqMap):
    global maxNum
    binaryMap = {}
    for item in wordFreqMap:
        if item not in binaryMap:
            convertedBinary = ''.join(format(ord(x), 'b') for x in item)
            convertedBinaryArr = [int(x) for x in convertedBinary] # transform to array
            res = np.zeros(BITS)
            index = 0
            arrSize = len(convertedBinaryArr)
            while index < BITS:
                if convertedBinaryArr[index % arrSize] == 1 :
                    res[index] = 1
                else:
                    res[index] = -1
                index += 1
            binaryMap[item] = res
    return binaryMap

# Input:    wordFreqMap: dict with <word, frequency>; bNumOfUrl: dict with <word, 200Binary>
# Output:   fingerprint for input url
def senHash(wordFreqMap, bNumOfUrl):
    key = np.zeros(BITS)
    for item in wordFreqMap:  
        key += wordFreqMap[item] * bNumOfUrl[item]
    # key is loaded with all numbers
    for i in range(BITS):
        if key[i] > 1:
            key[i] = 1
        else:
            key[i] = 0
    return key

def createFingerprint(wordFreqMap):
    return senHash(wordFreqMap, toBinaryMap(wordFreqMap))

# Input:    fingerprint1: fingerprint of url1; fingerprint2: fingerprint of url2
# Output:   true if two webpages have a high similarity; otherwise return false
def getSimilarity(fingerprint1,fingerprint2):
    diff = 0
    for i in range(BITS):
        if fingerprint1[i]!=fingerprint2[i]:
            diff += 1
    print('diff is:', diff)
    return diff < 4

# Input:    Word Frequency Map of a webpage
# Output:   true if similar to any webpage in scraper.urlFingers list; false otherwise
# Action:   Return true means similarity is high to one of webpage in scraper.urlFingers.
#           If return false, also adding current fingerprint to scraper.urlFingers list.
def isSimilarToOtherPage(wordFreqMap):
    fingerprint = createFingerprint(wordFreqMap)
    for savedFingerprint in scraper.urlFingers:
        if(getSimilarity(fingerprint, savedFingerprint)):
            return true
    return false

# import sys

# if __name__ == '__main__':
#     fileName1 = sys.argv[1]
#     fileName2 = sys.argv[2]
#     wordFreqMap1 = computeWordFrequencies(tokenize(fileName1))
#     wordFreqMap2 = computeWordFrequencies(tokenize(fileName2))
#     fingerprint1 = senHash(wordFreqMap1, toBinaryMap(wordFreqMap1))
#     fingerprint2 = senHash(wordFreqMap2, toBinaryMap(wordFreqMap2))
#     print('These two files similar situation is:', getsimilarity(fingerprint1, fingerprint2))