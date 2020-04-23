import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import tokenizer
from lxml import html

global uniqueUrlNum
global visitedUrl
global maxWordsPage
global totalWordFreq
visitedUrl = set()
uniqueUrlNum = 0
totalWordFreq = {}

def scraper(url, resp):
    links = extract_next_links(url, resp)
    print('links is:', links)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    global uniqueUrlNum
    res = list()

    if(resp.status > 600 or not is_valid(url)):
        return res

    parsedUrl = urlparse(url)
    hostName = parsedUrl.hostname
    if hostName not in visitedUrl:
        uniqueUrlNum += 1
        visitedUrl.add(hostName)
    

    soup = BeautifulSoup(resp.raw_response.content, "lxml")
    output = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/output_for_scraper.txt', 'w')
    output.write(soup.prettify())
    outPagesPerUrl = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/out_pages_per_url.txt', 'w')
    wordList = tokenizer.tokenize('output_for_scraper.txt')
    wordMap = tokenizer.computeWordFrequencies(wordList)
    output.close()

    element_tree = html.fromstring(resp.raw_response.content) 

    newUrlNum = 0
    for link in element_tree.xpath('//a/@href'):
        res.append(link)
        newUrlNum += 1
    # dom = lxml.html.fromstring(resp.raw_response.content)
    # for tag in soup.find_all('a'):
    #     outUniquePagesPerUrl.write(tag)
    # Task5: output subdomains did in the ics.uci.edu domain with number of unique pages
    if 'ics.uci.edu' in url:
        outPagesPerUrl.write(url)
        outPagesPerUrl.write(', ')
        outPagesPerUrl.write(str(newUrlNum))
        # outPagesPerUrl.write()
    
    # Implementation requred.
    return res

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.netloc not in set(["www.ics.uci.edu", "www.cs.uci.edu", "www.informatics.uci.edu", "www.stat.uci.edu", "www.today.uci.edu/department/information_computer_sciences"]):
            print('netloc: ', parsed.netloc, ' is not valid!')
            print('its hostname is:', parsed.hostname)
            return False
        if parsed.scheme not in set(["http", "https"]):
            print('not valid')
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