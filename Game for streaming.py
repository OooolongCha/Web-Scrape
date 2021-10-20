import requests
from bs4 import BeautifulSoup
from scrape_function_sep import google_web_scrape_basic

'''
我的想法是，只对New & Updates分类做stream processing，只爬取（1）评分人数；（2）总评分；（3）最新的几条评论
这样做的话，首先我们需要持续导入数据库的数据量不大，毕竟GCP应该是有上限的吧
其次，做实时监控dashborad的时候也不会太复杂
而且应该只有新发售和有大更新的游戏需要做一下监控，不更新的老游戏没有必要关注
'''


NewUpdates = requests.get('https://play.google.com/store/apps/collection/cluster?clp=SjYKKgokcHJvbW90aW9uXzMwMDA3OTFfbmV3X3JlbGVhc2VzX2dhbWVzEEoYAxIER0FNRToCCAI%3D:S:ANO1ljJYK2k&gsr=CjhKNgoqCiRwcm9tb3Rpb25fMzAwMDc5MV9uZXdfcmVsZWFzZXNfZ2FtZXMQShgDEgRHQU1FOgIIAg%3D%3D:S:ANO1ljICr10')

# collect web links
src = NewUpdates.content
soup = BeautifulSoup(src, 'lxml', from_encoding='utf-8')

LinksCollection = []
weblink = soup.find_all('div', {'class': 'b8cIId ReQCgd Q9MA7b'})
for web in weblink:
    link = web.find('a')
    urls = link.attrs['href']
    LinksCollection.append(urls)


# data scrape from these web links
stream = ['title', 'NumberOfRate', 'histogram', 'Rate']
gameInfo_all = [] # 用来放不需要实时更细的游戏基本信息，只需要上传一次数据库
streamInfo_all = [] # 用来放需要实时更新的rate类，并上传到数据库


for path in LinksCollection:
    gameInfo = {}
    streamInfo = {}
    url = 'https://play.google.com' + path
    info = google_web_scrape_basic(url, gameInfo)
    
    for ele in stream:
        '''
        这步是把收集到的信息分为两部分，一个是需要实时更新的rate类，一个是不需要更新的游戏基本信息类
        '''
        streamInfo[ele] = info[ele]
        streamInfo_all.append(streamInfo)
        del info[ele]
    
    gameInfo_all.append(info)

# get the cuurent time to name the file
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%d%m%Y%H%M%S")
file_name = 'streamInfo ' + dt_string +'.txt'


# 写成json文件
import json
import os 
os.chdir('S:\\NUS\\EBAC5006 Project\\GCP Streaming\\data')

with open(file_name, 'w') as json_file:
  json.dump(streamInfo_all, json_file)

with open('GameInfo.txt', 'w') as json_file:
  json.dump(gameInfo_all, json_file)
  
# 上传数据库
import os 
from google.cloud import storage 

os.chdir('S:\\NUS\\EBAC5006 Project\\GCP Streaming')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'ServiceKey.json'

storage_client = storage.Client()

def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket('data5006')
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False

file_path = r'S:\\NUS\\EBAC5006 Project\\GCP Streaming\\data'
upload_to_bucket(file_name, os.path.join(file_path, file_name), 'data5006')
upload_to_bucket('GameInfo.txt', os.path.join(file_path, 'GameInfo.txt'), 'data5006')


# https://www.youtube.com/watch?v=Gs5jGDROx1M
