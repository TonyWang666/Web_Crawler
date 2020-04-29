from threading import Thread
from urllib.parse import urlparse
from utils.download import download
from utils import get_logger
import scraper
import time
import tokenizer

global domainLocks
domainLocks = {".ics.uci.edu": 0, ".cs.uci.edu": 0, ".informatics.uci.edu": 0, "today.uci.edu/department/information_computer_sciences": 0, ".stat.uci.edu": 0}

class Worker(Thread):

    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.workerId = worker_id
        self.frontier = frontier
        super().__init__(daemon=True)
        
    def run(self):
        global domainLocks
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                # Task 1: Write unique pages number
                # outUniquePage = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/output_unique_page.txt', 'w', encoding="utf-8")
                outUniquePage = open('output_unique_page.txt', 'w', encoding="utf-8")
                outUniquePage.write("Number of unique url is: ")
                outUniquePage.write(str(scraper.uniqueUrlNum))
                outUniquePage.write("\n")

                # Task 2: Write longest Page in terms of number of words
                outUniquePage.write("Longest Page in terms of numbers of words is: ") 
                outUniquePage.write(scraper.maxWordsPage)
                outUniquePage.close()

                #Task 3: Write 50 most common words in the entire set of pages
                # outMostFreqWord = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/output_50_most_freq_word.txt', 'w', encoding="utf-8")
                outMostFreqWord = open('output_50_most_freq_word.txt', 'w', encoding="utf-8")
                for token in tokenizer.get50MostWords(scraper.totalWordFreq):
                    outMostFreqWord.write(token)
                    outMostFreqWord.write("\n")
                outMostFreqWord.close()

                #Task 4: write targetUrlDict
                # outPagesPerUrl = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/target_url_with_unique_page.txt', 'a', encoding="utf-8")
                outPagesPerUrl = open('target_url_with_unique_page.txt', 'a', encoding="utf-8")
                for targetKey in sorted (scraper.targetUrlDict):
                    outPagesPerUrl.write(targetKey)
                    outPagesPerUrl.write(', ')
                    outPagesPerUrl.write(str(scraper.targetUrlDict[targetKey]))
                    outPagesPerUrl.write('\n')
                outPagesPerUrl.close()
                break
            
            #  check tbd_url' domain locked or not           
            parsed = urlparse(tbd_url)
            netloc = parsed.netloc
            for domain in domainLocks:
                if domain in netloc and domainLocks[domain] == 1:
                    self.frontier.add_url(tbd_url)
                    return
            for domain in domainLocks:
                if domain in netloc:
                    domainLocks[domain] = 1
                    print(f'workerId: {self.workerId} with domain {domain} is set to 1')
                    break

            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            try:
                scraped_urls = scraper.scraper(tbd_url, resp, self.workerId)

                for scraped_url in scraped_urls:
                    print('add url:', scraped_url)
                    self.frontier.add_url(scraped_url)
                self.frontier.mark_url_complete(tbd_url)

                #   unlock the corresponding domain lock
                for domain in domainLocks:
                    if domain in netloc and domainLocks[domain] == 1:
                        time.sleep(self.config.time_delay)
                        domainLocks[domain] = 0
                        print(f'workerId: {self.workerId} with domain {domain} is set to 0')
                        break
            except Exception as e:
                print('Exception in worker with error:', e)
            # time.sleep(self.config.time_delay)