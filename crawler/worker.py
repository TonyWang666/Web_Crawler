from threading import Thread

from utils.download import download
from utils import get_logger
import scraper
import time
import tokenizer


class Worker(Thread):
    def __init__(self, worker_id, config, frontier):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")
                # Task 1: Write unique pages number
                outUniquePage = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/output_unique_page.txt', 'w')
                outUniquePage.write("Number of unique url is: ")
                outUniquePage.write(str(scraper.uniqueUrlNum))
                outUniquePage.write("\n")

                # Task 2: Write longest Page in terms of number of words
                outUniquePage.write("Longest Page in terms of numbers of words is: ") 
                outUniquePage.write(scraper.maxWordsPage)

                #Task 3: Write 50 most common words in the entire set of pages
                outMostFreqWord = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/output_50_most_freq_word.txt', 'w')
                for token in tokenizer.get50MostWords(scraper.totalWordFreq):
                    outMostFreqWord.write(token)
                    outMostFreqWord.write("\n")

                #Task 4: write targetUrlDict
                outPagesPerUrl = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/target_url_with_unique_page.txt', 'a')
                for targetKey in sorted (scraper.targetUrlDict):
                    outPagesPerUrl.write(targetKey)
                    outPagesPerUrl.write(', ')
                    outPagesPerUrl.write(str(scraper.targetUrlDict[targetKey]))
                    outPagesPerUrl.write('\n')
                outUniquePage.close()
                outMostFreqWord.close()
                outPagesPerUrl.close()
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            scraped_urls = scraper.scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)
            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
