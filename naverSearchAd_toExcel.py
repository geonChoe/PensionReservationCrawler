from datetime import datetime
from urllib.parse import urlparse
# from par import urlparse

import requests
import xlsxwriter
from bs4 import BeautifulSoup

to = datetime.now()
file_path = datetime.strftime(to, './%Y-%m-%d PensionSeachAd (%H-%M-%S).xlsx')
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet()
urls = [
    "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=스파펜션&pagingIndex=1",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=스파펜션&pagingIndex=2",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=스파펜션&pagingIndex=3",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=스파펜션&pagingIndex=4",
    "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성바닷가펜션&pagingIndex=1",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성바닷가펜션&pagingIndex=2",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성바닷가펜션&pagingIndex=3",
    "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성펜션&pagingIndex=1",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성펜션&pagingIndex=2",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성펜션&pagingIndex=3",
    "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도바다보이는펜션&pagingIndex=1",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도바다보이는펜션&pagingIndex=2",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도바다보이는펜션&pagingIndex=3",
    "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성가족펜션&pagingIndex=1",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성가족펜션&pagingIndex=2",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=강원도고성가족펜션&pagingIndex=3",
    "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=속초바다가보이는스파펜션&pagingIndex=1",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=속초바다가보이는스파펜션&pagingIndex=2",
    # "http://ad.search.naver.com/search.naver?where=ad&ie=utf8&sm=svc_nrs&query=속초바다가보이는스파펜션&pagingIndex=3",
]

row = 0
col = 0
number = 0
for _url in urls:
    response = requests.get(_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    keyword = soup.select_one('input.box_window')['value']
    list = soup.select('li.lst')
    worksheet.write(row, col, keyword)
    row += 1
    for li in list:
        no = li.find("em").text.rstrip('.')  # 순위
        name = li.find('a').find('img')['alt']  # 상호명
        link = li.select_one('div.inner').select_one('a.url').text  # 사이트주소
        period = li.select_one('div.inner').select_one('em.txt').text  # 광고집행기간
        description = li.select_one('div.inner').select_one('p.ad_dsc').text  # 소재
        worksheet.write(row, col, no)
        worksheet.write(row, col + 1, name)
        worksheet.write(row, col + 2, period)
        worksheet.write(row, col + 3, description)
        worksheet.write(row, col + 4, link)
        row += 1
    number += 1
    print("{0}번 검색어".format(number))
workbook.close()
