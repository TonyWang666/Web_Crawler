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
                # write the glboal uniqueUrlNum, maxWordPage, and maxHeapWordFreq into text file
                outMostFreqWord = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/output_most_req_word.txt', 'w')
                outUniquePage = open('/Users/jiaxiangwang/Downloads/UCI/spring2020/CS121/HW2/spacetime-crawler4py/output_unique_page.txt', 'w')
                for token in tokenizer.get50MostWords(scraper.totalWordFreq):
                    outMostFreqWord.write(token)
                    outMostFreqWord.write("\n")
                outUniquePage.write(str(scraper.uniqueUrlNum))
                outUniquePage.write("\n")
                # self.logger.info("The number of unique Url is:", scraper.uniqueUrlNum)
                for url in scraper.visitedUrl:
                    outUniquePage.write(url)
                    outUniquePage.write("\n")
                    # self.logger.info('url is:', url)
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
