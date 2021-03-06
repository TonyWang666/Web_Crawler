import os
import shelve

from threading import Thread, RLock
from queue import Queue, Empty

from utils import get_logger, get_urlhash, normalize
from scraper import is_valid


class Frontier(object):
    queueLock = RLock()
    def __init__(self, config, restart):
        self.logger = get_logger("FRONTIER")
        self.config = config
        self.to_be_downloaded = Queue()
        
        if not os.path.exists(self.config.save_file) and not restart:
            # Save file does not exist, but request to load save.
            self.logger.info(
                f"Did not find save file {self.config.save_file}, "
                f"starting from seed.")
        elif os.path.exists(self.config.save_file) and restart:
            # Save file does exists, but request to start from seed.
            self.logger.info(
                f"Found save file {self.config.save_file}, deleting it.")
            os.remove(self.config.save_file)
        # Load existing save file, or create one if it does not exist.
        self.save = shelve.open(self.config.save_file)
        if restart:
            self.logger.info('restart...')
            for url in self.config.seed_urls:
                self.add_url(url)
        else:
            self.logger.info('Set the frontier state with contents of save file.')
            # Set the frontier state with contents of save file.
            self._parse_save_file()
            if not self.save:
                self.logger.info('add seed_urls...')
                for url in self.config.seed_urls:
                    self.add_url(url)

    def _parse_save_file(self):
        ''' This function can be overridden for alternate saving techniques. '''
        total_count = len(self.save)
        tbd_count = 0
        try:
            Frontier.queueLock.acquire()
            for url, completed in self.save.values():
                if not completed and is_valid(url):
                    self.to_be_downloaded.put(url)
                    tbd_count += 1
            self.logger.info(
                f"Found {tbd_count} urls to be downloaded from {total_count} "
                f"total urls discovered.")
            Frontier.queueLock.release()
        except Exception as e:
            print('Exception in _parse_save_file Error is:', e)
            Frontier.queueLock.release()

    def get_tbd_url(self):
        try:
            Frontier.queueLock.acquire()
            popedUrl = self.to_be_downloaded.get()
            Frontier.queueLock.release()
            return popedUrl
        except Exception as e:
            print('Exception in get_tbd_url and Eror is:', e)
            Frontier.queueLock.release()
            return None

    def add_url(self, url):
        try:
            url = normalize(url)
            urlhash = get_urlhash(url)
            if urlhash not in self.save:
                self.save[urlhash] = (url, False)
                self.save.sync()
                self.to_be_downloaded.put(url)
        except Exception as e:
            print('Exception in add_url and Error is:', e)
            Frontier.queueLock.release()
    
    def mark_url_complete(self, url):
        urlhash = get_urlhash(url)
        if urlhash not in self.save:
            # This should not happen.
            self.logger.error(
                f"Completed url {url}, but have not seen it before.")

        self.save[urlhash] = (url, True)
        self.save.sync()
