from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib.error import HTTPError
from urllib.request import urlretrieve
from time import sleep

def crawl(search_key, save_file):

    # Truy cập trang web
    browser = webdriver.Chrome('chromedriver.exe')
    tempBrowser = webdriver.Chrome('chromedriver.exe')
    browser.get('https://images.google.com/')
    sleep(5)

    # Tìm ảnh
    txtFind = browser.find_element_by_xpath('//*[@id="sbtc"]/div/div[2]/input')
    txtFind.send_keys(search_key)
    txtFind.send_keys(Keys.ENTER)
    sleep(5)

    # Tải ảnh
    count = 0
    for image in browser.find_elements_by_tag_name('a'):
        if image.get_attribute('jsaction') == 'J9iaEb;mousedown:npT2md; touchstart:npT2md;':
            image.click() # Để hiện ra đường dẫn có dạng /imgres?imgurl
            sleep(3)

            src = image.get_attribute('href')
            tempBrowser.get(src)
            sleep(5)

            downloadableLink = tempBrowser.find_element_by_tag_name('img').get_attribute('src')
            try:
                urlretrieve(downloadableLink, save_file + str(count) + '.jpg')
            except HTTPError:
                continue
            
            count += 1
            sleep(1)

    tempBrowser.close()
    browser.close()

if __name__ == '__main__':
    crawl('mèo', './files/')
