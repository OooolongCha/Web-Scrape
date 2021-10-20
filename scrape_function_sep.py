import requests
from bs4 import BeautifulSoup
import re

def google_web_scrape_basic(url, appInfo):
    '''
    collection basic information of the game
    '''
    result = requests.get(url)

    # web source of the page
    src = result.content
    soup = BeautifulSoup(src, 'lxml', from_encoding='utf-8')

    # for header part

    title = soup.find_all('h1', {'class': 'AHFaub'}) 
    appInfo['title'] = title[0].text

    description = soup.find_all('div', {'jsname': 'sngebd' })
    appInfo['description'] = description[0].text

    grene = soup.find_all('span', {'T32cc UAO9ie'})
    appInfo['grene'] = grene[1].text

    AgeRating = soup.find_all('div', {'KmO8jd'})
    appInfo['AgeRating'] = AgeRating[0].text

    AdPurchase = soup.find_all('div', {'class': 'bSIuKf'})
    if AdPurchase == []:
        appInfo['ContainAds'] = 'False'
        appInfo['offerIAP'] = 'False'
    else: 
        if 'Contains Ads' in AdPurchase[0].text: 
            appInfo['ContainAds'] = 'True'
        else: appInfo['ContainAds'] = 'False'

        if 'Offers in-app purchases' in AdPurchase[0].text: 
            appInfo['offerIAP'] = 'True'
        else: appInfo['offerIAP'] = 'False'

    price= soup.find_all('span', {'class': 'oocvOe'})
    if price[0].text == 'Install':
        appInfo['price'] = float(0.00)
    else: appInfo['price'] = float(re.sub(r"[ ,+$a-zA-Z]", "", price[0].text))

    if appInfo['price'] > 0:
        appInfo['free'] = 'False'
    else: appInfo['free'] ='True'

    try:
        people_rate = soup.find_all('span', {'class': 'AYi5wd TBRnV'})
        appInfo['NumberOfRate'] = int(re.sub(r"[ ,.+]", "", people_rate[0].text))
    except: IndexError
    pass
    
    # Total rate (x out of 5)
    Rate = soup.find('div', {'class':'BHMmbe'})
    appInfo['Rate'] = Rate.text
    
    # Calculate the rate distribution
    # 网页上没有直接显示每个星级有多少人评分，所以需要计算。
    # 网页上有的数据是柱状图的比例，通过这个比例来计算总数即可
    RateDistribute = soup.find_all('div', {'class': 'mMF0fd'})
    percent = []
    for rate in RateDistribute: # 提取柱状图百分比
        result = str(rate.find_all('span')[1])
        number = float(re.findall(r'width:(.*)%',result)[0])
        percent.append(number/100)

    stars = []
    for element in percent: # 根据百分比计算总数
        result = (appInfo['NumberOfRate']/sum(percent)) * element
        stars.append(round(result))
    
    appInfo['histogram'] = stars
    return appInfo


def google_web_scrape_additional(url, appInfo):
    '''
    Collection additional information of the game
    '''
    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, 'lxml', from_encoding='utf-8')
    
    add_title = soup.find_all('div', {'class': 'hAyfc'})
    useless_key = ['Permissions', 'Report', 'Developer', 'Content Rating']

    for element in add_title:
        key = element.find('div', {'class': 'BgcNfc'})
        value = element.find('span', {'class': 'htlgb'})
        appInfo[key.text] = value.text


    for title in useless_key:
        try: del appInfo[title]
        except: KeyError
        pass

    try:
        appInfo['miniInstalls'] = int(re.sub(r"[a-zA-Z+,]", "", appInfo['Installs']))
        appInfo['Android'] = float(re.sub(r"[a-zA-Z+,]","", appInfo['Requires Android']))
    except: ValueError
    pass

    return(appInfo)  


def google_web_scrape(url, appInfo):
    google_web_scrape_basic(url, appInfo)
    google_web_scrape_additional(url, appInfo)
    return appInfo
