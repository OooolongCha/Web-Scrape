import requests
from bs4 import BeautifulSoup
from scrape_function import google_web_scrape

'''
这个是用来搜集游戏数据，搜集了1000+游戏，方便做recommender system的。
是batch processing，收集一次即可
stream processing请看Game for streaming.py
'''

'''
运行时间较长，按run了后去喝杯茶吧
速度应该取决于网速
'''


result = requests.get('https://play.google.com/store/apps/category/GAME')

# check validation
# print(result.status_code)
# print(result.headers)

cate_paths = []
game_paths = []
AppInfo = []

# web source of the page
src = result.content
soup = BeautifulSoup(src, 'lxml', from_encoding='utf-8')

catelink = soup.find_all('li', {'class': 'KZnDLd'})
for cate in catelink:
    link = cate.find('a')
    path = link.attrs['href']
    cate_paths.append(path)

cate_paths = cate_paths[36:]


# 根据收集到的不同category的路径，搜集游戏的路径链接
for category in cate_paths:
    url = 'https://play.google.com' + category
    web = requests.get(url)
    
    src = web.content
    soup = BeautifulSoup(src, 'lxml', from_encoding='utf-8')
    
    gamelinks = soup.find_all('div', {'class': 'b8cIId ReQCgd Q9MA7b'})
    for gamelink in gamelinks:
        link = gamelink.find('a')
        path = link.attrs['href']
        game_paths.append(path)


# 根据游戏的路径，提取信息
for path in game_paths:
    url = 'https://play.google.com' + path
    appInfo = google_web_scrape(url)
    AppInfo.append(appInfo)
    
    
import json
with open('AppInfo.txt', 'w') as json_file:
  json.dump(AppInfo, json_file)