from selenium import webdriver
from time import sleep


class ArticleCrawler():
    def __init__(self, storage):
        self.storage = storage
        self.browser = self.createBrowser()
    
    def createBrowser(self):
        """
            Khởi tạo browser
        """
        browser = webdriver.Chrome('chromedriver.exe')
        browser.get('https://thanhnien.vn/')
        sleep(5)

        return browser
    
    def getArticleLink(self):
        """
            Lấy đường dẫn và tiêu đề của các bài báo có trên trang web
        """
        linkList = []
        titleList = []
        for article in self.browser.find_elements_by_xpath("//a[@class='story__title cms-link']"):
            link = article.get_attribute('href')
            title = article.get_attribute('title')
            if link != None and title != None and link.find('https://thanhnien.vn/') == 0:
                linkList.append(link)
                titleList.append(title)
        
        return linkList, titleList
    
    def crawlArticle(self, linkList, titleList):
        for i in range(len(linkList)):
            try:
                # Truy cập vào từng bài báo
                self.browser.get(linkList[i])
                sleep(5)

                # Bỏ đi những kí hiệu không hợp khi đặt tên file
                title = "".join(x for x in titleList[i] if x.isalnum() or x == ' ') + '.txt'
            
                with open(self.storage + title, 'w', encoding = 'utf-8') as f:
                    # Tên tác giả
                    arthur = self.browser.find_element_by_xpath("//*[@class='details__author__ava']").get_attribute('title')
                    f.write('Author: ' + arthur + '\n')

                    # Nội dung bài viết
                    body = self.browser.find_element_by_id('abody')
                    contents = body.find_elements_by_tag_name('p')
                    for content in contents:
                        f.write(content.text + '\n')
            except:
                continue

    def crawl(self):
        linkList, titleList = self.getArticleLink()
        self.crawlArticle(linkList, titleList)
        self.browser.close()

if __name__ == '__main__':
    crawler = ArticleCrawler('./files/')
    crawler.crawl()