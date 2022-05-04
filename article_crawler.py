from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

# Truy cập trang web
browser = webdriver.Chrome('chromedriver.exe')
browser.get('https://thanhnien.vn/')
sleep(5)

# Lấy link của các bài viết
linkList = [link.get_attribute('data-vr-contentbox-url') \
            for link in browser.find_elements_by_tag_name('article')]

# Truy cập vào từng link
for link in linkList:
    if link != None and link.find('https://thanhnien.vn/') == 0:
        browser.get(link)
        sleep(5)
        title = browser.find_element_by_xpath("//*[@class='details__headline cms-title']").text
        title = "".join(x for x in title if x.isalnum() or x == ' ') + '.txt'
        with open('./files/' + title, 'w', encoding = 'utf-8') as f:
            # Tên tác giả
            arthur = browser.find_element_by_xpath("//*[@class='details__author__ava']").get_attribute('title')
            f.write('Arthur: ' + arthur + '\n')

            # Nội dung bài viết
            body = browser.find_element_by_id('abody')
            contents = body.find_elements_by_tag_name('p')
            for content in contents:
                f.write(content.text + '\n')

browser.close()