import re
from urllib.parse import urlparse
from urllib.parse import urldefrag
from bs4 import BeautifulSoup
import tokenizer
from lxml import html

global uniqueUrlNum
global visitedUrl
global maxWordsPage
global maxWordPerPage
global totalWordFreq
global targetUrlDict
visitedUrl = set()
maxWordsPage = ''
maxWordPerPage = 10000
uniqueUrlNum = 0
totalWordFreq = {}
targetUrlDict = {}

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    global uniqueUrlNum
    global maxWordsPage
    global maxWordPerPage
    res = list()

    if(resp.status > 600 or not is_valid(url)):
        print(url, 'is not a valid url')
        return res
    try:
        visitedUrl.add(url)
        # Task 1: count unique page
        uniqueUrlNum += 1
        parsedUrl = urlparse(url) # change here due to only 4, rerun tomorrow
        hostName = parsedUrl.hostname
        print('current Url is:', url)
        
        textForHuman = BeautifulSoup(resp.raw_response.content, "lxml").text
        output = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/output_for_scraper.txt', 'w', encoding="utf-8")
        output.write(textForHuman.lower())
        output.close()

        wordList = tokenizer.tokenize('output_for_scraper.txt')
        # Task 3: computeWordFrequencies implement totalWordFreq while computing the word frequncies
        wordMap = tokenizer.computeWordFrequencies(wordList)

        # Task 2: update unique page
        if(len(wordList) > maxWordPerPage):
            maxWordsPage = url
            maxWordPerPage = len(wordList)

        element_tree = html.fromstring(resp.raw_response.content) 

        for link in element_tree.xpath('//a/@href'):
            link = urldefrag(link)[0]
            res.append(link)

        # Task 4: output subdomains did in the ics.uci.edu domain with number of unique pages in each subdomain
        if '.ics.uci.edu' in hostName:
            if(hostName in targetUrlDict):
                targetUrlDict[hostName] += 1
            else:
                targetUrlDict[hostName] = 1
            # hostName sample is: "www.informatics.uci.edu"
        return res
    except:
        return res

def is_valid(url):
    try:
        parsed = urlparse(url)
        netloc = parsed.netloc
        path = parsed.path
        if ".ics.uci.edu" not in netloc and ".cs.uci.edu" not in netloc and ".informatics.uci.edu" not in netloc and "today.uci.edu/department/information_computer_sciences" not in netloc:
            return False
        if "wics.ics.uci.edu/events" in url: 
            return False #calender page is invalid
        if parsed.scheme not in set(["http", "https"]) or url in visitedUrl:
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise