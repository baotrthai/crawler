from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import urllib.request

def crawl(save_dir, arthur_name):
    # Tùy chỉnh browser để có thể tải files
    options = webdriver.ChromeOptions()
    prefs = {'download.default_directory' : save_dir}
    options.add_experimental_option("prefs", prefs)

    # Truy cập trang web
    browser = webdriver.Chrome('chromedriver.exe', chrome_options=options)
    browser.get('https://scholar.google.com/')
    sleep(3)

    # Tìm kiếm bài báo của tác giả
    txtFind = browser.find_element_by_xpath('/html/body/div/div[7]/div[1]/div[2]/form/div/input')
    txtFind.send_keys(arthur_name + ' paper')
    txtFind.send_keys(Keys.ENTER)
    sleep(3)

    # Tải các bài báo
    paperList = browser.find_elements_by_xpath("//*[@class='gs_r gs_or gs_scl']")
    for paper in paperList:
        # Chỉ tải file pdf được ở trang arxiv.org
        paperLink = paper.find_element_by_class_name('gs_or_ggsm')
        if paperLink.text.find('arxiv.org') == -1: 
            continue
        # Lấy đường dẫn bài báo
        link = paper.find_element_by_tag_name('a').get_attribute('href')
        # Lấy tên bài báo
        paperName = paper.find_element_by_class_name('gs_rt')
        name = paperName.text

        # Lưu bài báo theo tên
        response = urllib.request.urlopen(link)
        file_name = "./files/" + "".join(x for x in name if x.isalnum() or x in [' ', '-']) + ".pdf"
        file = open(file_name, 'wb')
        file.write(response.read())
        file.close()

    sleep(3)
    browser.close()

if __name__ == '__main__':
    crawl('D:\Workspace\crawler\files',
            'ian goodfellow')