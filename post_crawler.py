# Ref: https://viblo.asia/p/lam-the-nao-crawl-1-trieu-comments-tren-facebook-Qpmle1NVlrd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class PostCrawler():
    def __init__(self, storage):
        self.storage = storage
        self.browser = self.createBrowser()
    
    def createBrowser(self):
        """
            Khởi tạo browser
        """
        browser = webdriver.Chrome('chromedriver.exe')
        browser.get('https://vi-vn.facebook.com/')
        sleep(5)
        
        return browser

    def loginFacebook(self, email, password):
        """
            Đăng nhập vào facebook
        """
        txtEmail = self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input')
        txtEmail.send_keys(email)
        txtPass = self.browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input')
        txtPass.send_keys(password)
        txtPass.send_keys(Keys.ENTER)
        sleep(10)
    
    def getPage(self, pageId):
        """
            Truy cập vào page cần thiết
        """
        self.browser.get("https://touch.facebook.com/" + pageId)
        sleep(5)
    
    def getPostId(self, amountOfPost):
        """
            Lấy ID của các bài post
        """
        idList = []
        while len(idList) < amountOfPost:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            # Thực hiện lấy khối <a>..</a> có đường dẫn chứa "/story.php" vì chúng chứa id cần tìm
            postList = self.browser.find_elements_by_xpath('//a[contains(@href, "/story.php")]')
            if (len(postList)):
                for link in postList:
                    # VD: story.php?story_fbid=5196438273712196&id=108804609142280
                    # id của post sẽ nằm giữa 'fbid=' và '&' đầu tiên
                    postId = link.get_attribute('href').split('fbid=')[1].split('&')[0]
                    if postId not in idList:
                        idList.append(postId)
            sleep(5)

        return idList
    
    def getComment(self):
        """
            Lấy nội dung các comment trên post
        """
        commentList = []
        links = self.browser.find_elements_by_xpath('//a[contains(@href, "comment/replies")]')
        if (len(links)):
                for link in links:
                    takeLink = link.get_attribute('href').split('ctoken=')[1].split('&')[0]
                    textCommentElement = self.browser.find_element_by_xpath(('//*[@id="' + takeLink.split('_')[1] + '"]/div/div[1]'))
                    commentList.append(textCommentElement.text)
        return commentList

    def crawlPost(self, amountOfComment, postIdList):
        """
            Thực hiện crawl nội dung và comment cho từng post
        """
        count = 0
        for id in postIdList:
            self.browser.get("https://mbasic.facebook.com/" + id)
            sleep(5)

            with open(self.storage + str(count) + '.txt', 'w', encoding='utf-8') as f:
                # Nội dung của bài post sẽ có trong khối có thuộc tính class = "bb"
                content = self.browser.find_element_by_xpath('/html/body/div/div/div[2]/div/div[1]/div[1]/div/div/div[1]').text #('//*[@class="bb"]/div[1]').text
                f.write(content + '\n\n')

                commentList = self.getComment()
                while len(commentList) < amountOfComment:
                    # Nếu chưa đủ comment thì sẽ mở thêm comment mới
                    newComment = self.browser.find_elements_by_xpath('//*[contains(@id,"see_next")]/a')
                    if (len(newComment)):
                        newComment[0].click()
                        sleep(5)
                        commentList += self.getComment()   
                    else:
                        # Nếu chưa đủ mà đã hết comment thì sẽ thoát vòng lặp
                        break

                for comment in commentList:
                    f.write(str(comment) + '\n')

            count += 1

    def crawl(self, email, password, pageId, amountOfPost, amountOfComment):
        self.loginFacebook(email, password)
        self.getPage(pageId)
        postIdList = self.getPostId(amountOfPost)
        self.crawlPost(amountOfComment, postIdList)
        self.browser.close()

if __name__ == '__main__':
    email = ''
    password = ''
    pageId = 'ThuyTiennOfficial'
    amountOfPost = 10
    amountOfComment = 10
    crawler = PostCrawler('./files/')
    crawler.crawl(email, password, pageId, amountOfPost, amountOfComment)

