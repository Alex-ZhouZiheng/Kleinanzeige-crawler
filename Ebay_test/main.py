"""
抓取kleinanzeige上的慕尼黑租房信息（0-2Zimmer）
"""
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import time
#from utils import url_manager
def get_kleinanzeige():
    url1 = "https://www.kleinanzeigen.de/s-wohnung-mieten/muenchen/c203l6411+wohnung_mieten.zimmer_d:0%2C2"
    url2 = "https://www.kleinanzeigen.de/s-wohnung-mieten/muenchen/seite:2/c203l6411+wohnung_mieten.zimmer_d:0%2C2"
    urls = [url1, url2]
    htmls = []
    for i in range(len(urls)):
        url = urls[i]
        driver = webdriver.Chrome()
        driver.get(urls[i])
        page_source = driver.page_source
        htmls.append(page_source)
        print(f"Page {i + 1} done")
        driver.quit()
    return htmls
def parse_single_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.find_all('article', class_='aditem')
    data = []
    #new_urls = url_manager.UrlManager()
    for article in articles:
        title_tag = article.find('h2', class_='text-module-begin')
        price_tag = article.find('p', class_='aditem-main--middle--price-shipping--price')
        time_tag = article.find('div', class_='aditem-main--top--right')
        post_id_tag = article.find('div', class_='aditem-main--top--left')
        href = article.find('a', class_='ellipsis')['href']
        title = title_tag.get_text().strip() if title_tag else 'No Title Found'
        price = price_tag.get_text().strip() if price_tag else 'No Price Available'
        time = time_tag.get_text().strip() if time_tag else 'No Time Available'
        post_id = post_id_tag.get_text().strip() if post_id_tag else 'No Post ID Found'
        list_lokal = post_id.split(" ")
        post_id = list_lokal[-0]
        lokal = list_lokal[1]
        #new_urls.add_new_url('https://www.kleinanzeigen.de'.join(href))

        if '.' in price:
            price = price.replace('.', ',')
        data.append({
            'title': title,
            'price': price,
            'time': time,
            'Postleitzahl': post_id,
            'lokal': lokal,
            'Link': f'https://www.kleinanzeigen.de{href}'
        })

    # while new_urls.has_new_url():
    #     new_url = new_urls.get_new_url()
    #     driver = webdriver.Chrome()
    #     driver.get(new_url)
    #     page_source = driver.page_source
    #     soup = BeautifulSoup(page_source, 'html.parser')
    return data

def immousout_crawler():
    driver = webdriver.Chrome()
    driver.get('https://www.immobilienscout24.de/Suche/de/bayern/muenchen/wohnung-mieten?enteredFrom=result_list#/')
    time.sleep(5)
    # 提取地址
    driver.find_elements(By.CLASS_NAME, 'result-list-entry__map-link link-text-secondary font-normal font-ellipsis').get_attribute('textContent')
    # 提取价格
    driver.find_elements(By.CLASS_NAME, 'font-highlight font-tabular').get_attribute('textContent')






if __name__ == '__main__':
    res = []
    htmls = get_kleinanzeige()
    for i in range(len(htmls)):
        data = parse_single_html(htmls[i])
        res.append(data)
    df = pd.DataFrame(res[0] + res[1])
    df.to_excel('output.xlsx', index=False)


