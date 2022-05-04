from tkinter import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.error import HTTPError
from urllib.request import urlretrieve
from time import sleep

class ImageCrawler():
    def __init__(self, storage):
        self.storage = storage
        self.browser = self.createBrowser()
        self.subBrowser = self.createBrowser()
    
    def createBrowser(self):
        """
            Khởi tạo browser
        """
        browser = webdriver.Chrome('chromedriver.exe')
        browser.get('https://images.google.com/')
        sleep(5)
        
        return browser
    
    def searchImage(self, searchKey):
        """
            Tìm kiếm ảnh qua searchKey
        """
        # Tìm thanh tìm kiếm và điền từ khóa
        txtFind = self.browser.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
        txtFind.send_keys(searchKey)
        txtFind.send_keys(Keys.ENTER)
        sleep(5)
    
    def crawlImage(self):
        count = 0

        for image in self.browser.find_elements_by_tag_name('a'):
            if image.get_attribute('jsaction') == 'J9iaEb;mousedown:npT2md; touchstart:npT2md;':
                # Thì hiện chạm vào ảnh để có đường dẫn có dạng /imgres?imgurl=...
                image.click()
                sleep(3)

                # Truy cập và đường dẫn có ảnh
                src = image.get_attribute('href')
                self.subBrowser.get(src)
                sleep(5)

                # Tải ảnh
                downloadableLink = self.subBrowser.find_element_by_tag_name('img').get_attribute('src')
                try:
                    urlretrieve(downloadableLink, self.storage + str(count) + '.jpg')
                except HTTPError:
                    continue
                
                count += 1
                sleep(1)

    def crawl(self, searchKey):
        self.searchImage(searchKey)
        self.crawlImage()
        self.subBrowser.close()
        self.browser.close()

if __name__ == '__main__':
    crawler = ImageCrawler('./files/')
    crawler.crawl('mèo')
