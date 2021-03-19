import requests
from bs4 import BeautifulSoup
import json

from collections import deque
job_queue = deque()
job_queue.append('https://health.ltn.com.tw/article/breakingnews/3451348')

def f(url, wf):
    output_dict = {}
    #print(url)
    #要抓資料，先把html頁面語法下載下來，存入res變數中
    res = requests.get(url)
    #print(res.text)

    #用beautifulsoup套件來解析html頁面
    soup = BeautifulSoup(res.text, 'html.parser')
    #print(soup)
    #用beatifulsoup的功能，把標題擷取出來
    title_elem = soup.find('title')
    #print(title_elem)
    #print(title_elem.string)
    output_dict['title'] = title_elem.string

    #抓取時間
    time_elem_list = soup.select('span.time')
    #print(time_elem_list[0])
    #print(time_elem_list[0].string.strip())
    output_dict['post_time'] = time_elem_list[0].string.strip()

    #抓取圖片的url
    image_elem = soup.select('a.image-popup-vertical-fit')
    #print(image_elem[0])
    #print(image_elem[0]['href'])
    #print(image_elem[0]['title'])
    if len(image_elem) > 0:
        output_dict['image_url'] = image_elem[0]['href']
        output_dict['image_title'] = image_elem[0]['title']

    #抓取文章內容
    article_elem = soup.select('div.text > p')
    del article_elem[-1]
    del article_elem[2:4]
    output_content = ''
    for x in article_elem:
        #print(x.string)
        if x.string is None:
            continue
        output_content += x.string
    output_dict['content'] = output_content

    #抓取相關新聞
    #print("相關新聞：")
    related_news_elem = soup.select('ul.related > li > a')
    output_related_news = []
    #print(related_news_elem)
    for x in related_news_elem:
        #print(x["data-desc"])
        #print(x["href"])
        output_related_news.append({'title': x['data-desc'], 'href': x['href']})
    output_dict['related_news'] = output_related_news

    wf.write(json.dumps(output_dict, ensure_ascii=False)+'\n')

    #將相關新聞的網址存在queue list裡面
    for x in related_news_elem:
        url1 = x["href"]
        job_queue.append(url1)

with open('data.json', 'wt', encoding='utf8') as wf:
    while 1:
        url = job_queue.popleft()
        f(url, wf)
