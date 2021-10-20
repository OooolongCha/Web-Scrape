import requests
from bs4 import BeautifulSoup
from stream_function import get_data, write_upload_file

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

#---------------Executer------------------------------------------------------
import schedule
import time

def data_scrape_upload():
    print('Data Scraping and Uploading......')
    gameInfo_all, streamInfo_all = get_data(LinksCollection)
    write_upload_file(gameInfo_all, streamInfo_all)

schedule.every(2).hours.do(data_scrape_upload)

while True:
    schedule.run_pending()
    time.sleep(True)
