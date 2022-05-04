from urllib.error import HTTPError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import urllib.request

class PaperCrawler():
    def __init__(self, storage):
        self.storage = storage
        self.browser = self.createBrowser()
    
    def createBrowser(self):
        """ 
            Khỏi tạo browser
        """
        browser = webdriver.Chrome('chromedriver.exe')
        browser.get('https://scholar.google.com/')
        sleep(3)

        return browser

    def searchPaper(self, author):
        """
            Tìm thanh tìm kiếm và nhập từ khóa cần tìm
        """
        txtFind = self.browser.find_element_by_xpath('/html/body/div/div[7]/div[1]/div[2]/form/div/input')
        txtFind.send_keys(author + ' paper')
        txtFind.send_keys(Keys.ENTER)
        sleep(3)
    
    def crawlPaper(self):
        """
            1. Tìm những khối <div>..</div> có class là 'gs_r gs_or gs_scl' vì chúng sẽ chưa link truy cập đến bài báo
            2. Lọc ra những link đến từ trang arxiv.org để tải không cần đăng nhập
            3. Thực hiện lấy tên và đường dẫn.
            4. Lưu bài báo tên tìm được.
        """
        paperList = self.browser.find_elements_by_xpath("//*[@class='gs_r gs_or gs_scl']") 
        for paper in paperList:
            # Tải pdf ở trang arxiv.org
            paperLink = paper.find_element_by_class_name('gs_or_ggsm')
            if paperLink.text.find('arxiv.org') == -1:
                continue

            # Lấy đường dẫn bài báo
            link = paper.find_element_by_tag_name('a').get_attribute('href')

            # Lấy tên bài báo
            paperName = paper.find_element_by_class_name('gs_rt')
            name = paperName.text

            # Lưu bài báo theo tên
            try:
                response = urllib.request.urlopen(link)
                file_name = self.storage + "".join(x for x in name if x.isalnum() or x in [' ', '-']) + ".pdf"
                with open(file_name, 'wb') as f:
                    f.write(response.read())
            except HTTPError:
                continue

            sleep(3)

    def crawl(self, author):
        self.searchPaper(author)
        self.crawlPaper()
        self.browser.close()


if __name__ == '__main__':
    crawler = PaperCrawler('./files/')
    crawler.crawl('ian goodfellow')