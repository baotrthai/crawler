# Ref: https://viblo.asia/p/lam-the-nao-crawl-1-trieu-comments-tren-facebook-Qpmle1NVlrd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

# Truy cập trang web
browser = webdriver.Chrome('chromedriver.exe')
browser.get('https://vi-vn.facebook.com/')
sleep(5)

# Đăng nhập facebook
txtEmail = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[1]/input')
txtEmail.send_keys('strawb0314@gmail.com')
txtPass = browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[1]/div[2]/div/input')
txtPass.send_keys('Fabao_13579')
txtPass.send_keys(Keys.ENTER)
sleep(10)

# Truy cập page cần thiết
pageId = 'bikipyeu'
browser.get("https://touch.facebook.com/" + pageId)
sleep(5)

# Lấy id của các bài post
amountOfPost = 3
idList = []
while len(idList) < amountOfPost:
    sleep(5)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    shareBtn = browser.find_elements_by_xpath('//a[contains(@href, "/story.php")]')
    if (len(shareBtn)):
        for link in shareBtn:
            postId = link.get_attribute('href').split('fbid=')[1].split('&')[0]
            if postId not in idList:
                idList.append(postId)

# Lấy dữ liệu của từng post
def getComment(browser):
    commentList = []
    links = browser.find_elements_by_xpath('//a[contains(@href, "comment/replies")]')
    if (len(links)):
            for link in links:
                takeLink = link.get_attribute('href').split('ctoken=')[1].split('&')[0]
                textCommentElement = browser.find_element_by_xpath(('//*[@id="' + takeLink.split('_')[1] + '"]/div/div[1]'))
                commentList.append(textCommentElement.text)
    return commentList

count = 0
amountOfComment = 3
for id in idList:
    browser.get("https://mbasic.facebook.com/" + id)
    sleep(5)
    commentList = []
    with open('./files/' + str(count) + '.txt', 'w', encoding='utf-8') as f:
        content = browser.find_element_by_xpath('//*[@class="bb"]/div[1]').text
        f.write(content + '\n\n')
        print(content)
        commentList += getComment(browser)
        while len(commentList) < amountOfComment:
            nextBtn = browser.find_elements_by_xpath('//*[contains(@id,"see_next")]/a')
            if (len(nextBtn)):
                nextBtn[0].click()
                sleep(5)
                commentList += getComment(browser)
                
            else:
                break
        for comment in commentList:
            f.writelines(str(comment) + '\n')
    count += 1

sleep(5)
browser.close()
