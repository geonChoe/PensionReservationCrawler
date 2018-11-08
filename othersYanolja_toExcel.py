import re

import requests
import xlsxwriter
from bs4 import BeautifulSoup
from urllib.parse import urlparse
# from urlparse2 import urlparse
from datetime import datetime

to = datetime.now()
file_path = datetime.strftime(to, './%Y-%m-%d PensionYanolja (%H-%M-%S).xlsx')
workbook = xlsxwriter.Workbook(file_path)
worksheet = workbook.add_worksheet()
this = to.strftime('%Y-%m-%d')
urls = [
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24081&revDate={0}&revDay=1".format(this), #1 씨모하비
    "http://www.yapen.co.kr/pensionReserve?ypIdx=19865&revDate={0}&revDay=1".format(this), #2 해마루펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24210&revDate={0}&revDay=1".format(this), #3 돈방석펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24057&revDate={0}&revDay=1".format(this), #4 빌라드아야펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=21396&revDate={0}&revDay=1".format(this), #5 씨오브하트펜션 -> 전화예약으로 -> 2월9일 수정 다시추가
    "http://www.yapen.co.kr/pensionReserve?ypIdx=23975&revDate={0}&revDay=1".format(this), #6 샤랄라펜션 -> 2월 24일 전화예약으로 바뀜 > 3월20전화예약
    "http://www.yapen.co.kr/pensionReserve?ypIdx=23977&revDate={0}&revDay=1".format(this), #7 아지로펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=23746&revDate={0}&revDay=1".format(this), #8 리안펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=22672&revDate={0}&revDay=1".format(this), #9 리틀스퀘어펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24080&revDate={0}&revDay=1".format(this), #10 아야진 -> 2월24일 전화예약으로 바뀜 > 3월20전화예약
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24334&revDate={0}&revDay=1".format(this), #11 다오리
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24333&revDate={0}&revDay=1".format(this), #12 국화꽃향기
    "http://www.yapen.co.kr/pensionReserve?ypIdx=22095&revDate={0}&revDay=1".format(this), #13 크리스마스하우스펜션 -> 4월4일 전화예약
    "http://www.yapen.co.kr/pensionReserve?ypIdx=22345&revDate={0}&revDay=1".format(this), #14 마르쏠펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=22917&revDate={0}&revDay=1".format(this), #15 1박2일펜션 -> 2월 21일 전화예약으로 됨 -># 수정 다시 추가
    "http://www.yapen.co.kr/pensionReserve?ypIdx=21932&revDate={0}&revDay=1".format(this), #16 예다울커플1펜션 -> 2월 24일 전화예약으로 됨 > 3월20전화예약
    "http://www.yapen.co.kr/pensionReserve?ypIdx=21939&revDate={0}&revDay=1".format(this), #17 예다울커플2펜션 -> 2월 24일 전화예약으로 됨 > 3월20전화예약
    "http://www.yapen.co.kr/pensionReserve?ypIdx=21917&revDate={0}&revDay=1".format(this), #18 예다울패밀리펜션 -> 2월24일 전화예약으로 바뀜 > 3월20전화예약
    "http://www.yapen.co.kr/pensionReserve?ypIdx=21348&revDate={0}&revDay=1".format(this), #19 감나무펜션 -> 2월 24일 전화예약으로 바뀜
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24055&revDate={0}&revDay=1".format(this), #20 살리펜션 -> 2월 24일 전화예약으로 바뀜 -> 5월 29일 야놀자나감
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24105&revDate={0}&revDay=1".format(this), #21 늘푸른하우스펜션 -> 2월24일 전화예약으로 바뀜 > 3월14일 전화예약>3월22일 전화예약
    # "http://www.yapen.co.kr/pensionReserve?ypIdx=24157&revDate={0}&revDay=1".format(this), # 푸른별비행사펜션 -> 2월 24일 전화예약으로바뀜 > 3월8일 야놀자 나감
    #"http://www.yapen.co.kr/pensionReserve?ypIdx=21943&revDate={0}&revDay=1".format(this), # 또한아의별펜션 -> 전화예약으로 -> 2월9일 수정 다시추가 -> 2월 24일 전화예약으로 바뀜
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24407&revDate={0}&revDay=1".format(this), #22 수자별펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=19987&revDate={0}&revDay=1".format(this), #23 고성펜션화포리
    "http://www.yapen.co.kr/pensionReserve?ypIdx=19852&revDate={0}&revDay=1".format(this), #24 오리엔트펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=25017&revDate={0}&revDay=1".format(this), #25 네츄럴하우스펜션 -> 전화예약으로 -> 2월12일 수정 다시추가, 2월 21일 전화예약으로 바뀜 -> 수정 다시추가
    # "http://www.yapen.co.kr/pensionReserve?ypIdx=24017&revDate={0}&revDay=1".format(this), # 발리하우스펜션 -> 야놀자나감
    "http://www.yapen.co.kr/pensionReserve?ypIdx=24056&revDate={0}&revDay=1".format(this), #26 나이아스펜션 -> 2월 24일 전화예약으로바뀜
    "http://www.yapen.co.kr/pensionReserve?ypIdx=22476&revDate={0}&revDay=1".format(this), #27 봉포파도소리펜션 -> 2월 24일 전화예약으로 바뀜 -> 5월 29일 야놀자 나감
    "http://www.yapen.co.kr/pensionReserve?ypIdx=22982&revDate={0}&revDay=1".format(this), #28 오늘멋진날펜션
    "http://www.yapen.co.kr/pensionReserve?ypIdx=19842&revDate={0}&revDay=1".format(this), #29 갈매기나는꿈펜션 -> 2월9일 수정 추가
]

row = 0
col = 0
number = 0
for _url in urls:
    try:
        response = requests.get(_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        pName = soup.select_one('b.name').text
        list = soup.select('tr.selectRoom')
        for li in list:
            rName = li.find('label').text
            bgNumber = li.text.find('예약가능')
            if bgNumber != -1:
                bgNumbers = "X"
            else:
                bgNumbers = "O"
            charge = li.text.split()[-1]
            charges = re.sub('[^0-9, ,]', '', charge).split()[-1]
            discount = int(re.sub('[^0-9]', '', charge).split()[-1])
            yanolja_discount = discount-(discount*2/100)
            worksheet.write(row, col, pName)
            worksheet.write(row, col + 1, rName)
            worksheet.write(row, col + 2, charges)
            worksheet.write(row, col + 3, yanolja_discount)
            worksheet.write(row, col + 4, bgNumbers)
            row += 1
        number += 1
        print("{0}번 펜션".format(number))
    except:
        number += 1
        print("{0}번 펜션 오류".format(number))
workbook.close()

