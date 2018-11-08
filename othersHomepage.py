import re
from datetime import datetime
from urllib.parse import urlparse
# from urlparse2 import urlparse

import requests
from bs4 import BeautifulSoup
# from selenium import webdriver

# binary = 'C:\\Users\Administrator\Desktop\PycharmProjects\chromedriver.exe'
to = datetime.now()
this = to.strftime('%Y-%m-%d') # 날짜형식
its = to.strftime('%Y&month=%m&day=%d')
urls = [
    # 예약완료가격모름(레드콩, 오컴즈, 아이넷, 설악닷컴, 강원웹, ?, 씨모하비(디지탈나우), 해랑바다랑(홈피디자인))
    # 우리펜션(select한계), 스테이위드시스템, 민박투어시스템

    # 씨모하비/디지탈나우 예약완료시 가격을 알 수 없음.
    # 해랑바다랑/홈피디자인  예약완료시 가격을 알 수 없음.
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2681&id_room_type=21113&dt_s={0}".format(this), #1번 아미가동
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2682&id_room_type=21115&dt_s={0}".format(this), #2번 아미고동
    # 탑하우스/레드콩 예약완료시 가격을 알 수 없음(5단계구성).
    # 'http://pension.x-y.net/prs/skins/skin-02/reservation.html?pensionId=sulak&year={0}'.format(its), # 설악
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=yedawol3&search_date={0}".format(this), #3번 예다울패밀리
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=yedawol1&search_date={0}".format(this), #4번 예다울커플1
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=yedawol2&search_date={0}".format(this), #5번 예다울커플2
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=syarala&search_date={0}".format(this), #6번 샤랄라
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=ayapension&search_date={0}".format(this), #7번 아야진항
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=hana&search_date={0}".format(this), #8번 또한아의별
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=gamnamu&search_date={0}".format(this), #9번 감나무
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=bluehouse&search_date={0}".format(this), #10번 늘푸른하우스
    "http://gpnew.gpension.kr/reser/room_list.php?room_id=G_1429179858&pension_id=bluestar&search_date={0}".format(this), #11번 푸른별비행사
    # 스피야지/오컴즈(펜션뱅크) 예약완료시 가격을 알 수 없음(5단계구성).
    # 티박스/로고스웹 select() 한계
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=1110&id_room_type=8830&dt_s={0}".format(this), #12번 아라마루
    #"https://www.ddnayo2.com", # 오션뷰
    # 네르하쏠/오컴즈(펜션뱅크) 예약완료시 가격을 알 수 없음(5단계구성).
    # 페블비치펜션/아이넷 예약완료시 가격을 알 수 없음(5단계구성).
    "http://rev.yapen.co.kr/external?ypIdx=19842", #13번 갈매기나는꿈
    # 해맞이하우스/설악닷컴 예약완료시 가격을 알 수 없음(5단계구성).
    # 모닝뷰/우리펜션 select() 한계
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2131&dt_s={0}".format(this), #14번 메이플펜션
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2128&dt_s={0}".format(this), #15번 메이플플라워펜
    # 화포리/우리펜션 select() 한계
    # "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=1921&dt_s={0}".format(this), #마르쏠펜션 > 3월20일바껴서 뻼
    "http://rev.yapen.co.kr/external?ypIdx=23746", #16번 리안펜션
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2090&dt_s={0}".format(this), #17번 씨랜드펜션
    "http://rev.yapen.co.kr/external?ypIdx=21396", #18번 씨오브하트펜션
    #"http://rev.yapen.co.kr/external?ypIdx=23977", # 아지로펜션 -> 4월 5일 홈페이지 변화
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2150&dt_s={0}".format(this), #19번 고성 추억만들기
    # 봉포플라트/스테이위드
    # 씨엘178/스테이위드
    # 라헨느풀빌라/스테이위드
    # 휴/스테이위드
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=741&dt_s={0}".format(this), #20번 파인로그
    # 설악의정원 실시간못봄
    "http://rev.yapen.co.kr/external?ypIdx=20280",  #21번 나폴리하우스
    # 오즈/스테이위드
    # 라코스타/오컴즈(펜션뱅크) 예약완료시 가격을 알 수 없음(5단계구성).
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=1222&dt_s={0}".format(this), #22번 코코앤루루
    # 소담/민박투어
    # 히솝/오컴즈(펜션뱅크) 예약완료시 가격을 알 수 없음(5단계구성).
    # 씨스파/민박투어
    # 두플렉스+트로이스/레드콩 예약완료시 가격을 알 수 없음(5단계구성).
    # 네이플하우스/? 예약완료시 가격을 알 수 없음(5단계구성).
    # 천진낭만/오컴즈(펜션뱅크) 예약완료시 가격을 알 수 없음(5단계구성).
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=1794&dt_s={0}".format(this), #23번 로미엣펜션
    "http://seamorning.co.kr/pension/reserve.html?reserve_days=&reserve_form=list&sdate={0}".format(this), #24번 바다애아침펜션
    # 씨엔스타/강원웹 예약완료시 가격을 알 수 없음(5단계구성).
    "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2203&dt_s={0}".format(this),  #25번 코스트하우스
    "https://rev.yapen.co.kr/external?ypIdx=24199",  #26번 고성 하얀파도 펜션
    # "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2384&dt_s={0}",  # 고성 오즈펜션
    # "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2151&dt_s={0}",  # 보노보노
    # "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=1921&dt_s={0}",  # 마르쏠펜션
    # "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2674&dt_s={0}",  # 고성 오션뷰
]

def get_uri(_url):
    return urlparse(_url)[0] + '://' + urlparse(_url)[1]

class HompageParser:
    def __init__(self, func=None):
        if func:
            self.parse_url = func
    def parse_url(self, _url):
        print("구현 필요")
        print(_url)

def army_parser(_url):
    response = requests.get(_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        pName = soup.select_one('h2.pname').text.strip()
    except:
        pName = soup.select_one('h2.pname').text
    list = soup.select_one('table.listroom').select('tr')
    list = list[1:]
    txt = ''
    for li in list:
        rName = li.select_one('td.nm_room').select_one('span').text
        charge = li.select_one('td.won.drate').text
        charges = re.sub('[^0-9, ,]', '', charge).split()[-1]

        stateNumber = li.text.find('예약가능')
        if stateNumber != -1:
            # stateNumber = li.text.find('예약가능')
            stateNumber = 'X'
        else:
            stateNumber = li.text.find('예약완료')
            stateNumber = 'O'
        # state = li.text[stateNumber:stateNumber + 4]
        state = stateNumber
        txt += '{0}/{1}/{2}/{3}\n'.format(pName, rName, charges, state)
    return txt

# def xy_parser(_url):
#     # binary = 'C:\\Users\Administrator\Desktop\PycharmProjects\chrome\chromedriver.exe'
#     driver = webdriver.Chrome(binary)
#     driver.get(_url)
#     pName = "설악펜션"
#     html = driver.page_source
#     soup = BeautifulSoup(html, 'html.parser')
#     list = soup.select_one('tbody').select('tr')
#     txt = ''
#     for li in list:
#         rName = li.select('td')[2].text
#         charge = li.select('td')[5].text
#         charges = re.sub('[^0-9, ,]', '', charge).split()[-1]
#         state = li.select_one('input').text.find('disabled')
#         if state != -1:
#             states = 'O'
#         else:
#             states = 'X'
#         txt += '{0}/{1}/{2}/{3}\n'.format(pName, rName, charges, states)
#     driver.close()
#     return txt

def gpension_parser(_url):
    pName = _url.split('&')[1].split('=')[-1]
    response = requests.get(_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list = soup.select_one('tbody').select('tr')
    txt = ''
    for li in list:
        rName = li.select_one('label').text
        charge = li.select('td')[3].text.strip().split()[-1]
        charges = re.sub('[^0-9, ,]', '', charge).split()[-1]
        state = li.text.find('예약완료')
        if state != -1:
            states = "O"
        else:
            states = 'X'
        txt += '{0}/{1}/{2}/{3}\n'.format(pName, rName, charges, states)
    return txt

def res_yapen_parser(_url):
    response = requests.get(_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pName = soup.select_one('div.headerPensionName').text.strip()
    list1 = soup.select_one('td.todayBg').select('li.roomNameLayer') # 자동으로 날짜가 지나면 todayBg가 넘어갈듯
    list2 = soup.select_one('td.todayBg').select('li.roomPriceLayer')
    txt = ''
    for li1 in list1:
        rName = li1.select_one('div.roomName').text

        n = list1.index(li1)
        charge = list2[n].select_one('div.roomResultPrice').text

        stateNumber = li1.text.find('가')
        if stateNumber != -1:
            stateNumbers = 'X'
        else:
            stateNumbers = 'O'
        txt += '{0}/{1}/{2}/{3}\n'.format(pName, rName, charge, stateNumbers)
    return txt

def osean_parser(_url):
    pName = "고성 오션뷰펜션"
    rooms_name = ['501(스파)', '502(스파)', '301(스파)', '302(스파)', '201(스파)', '202(스파)']
    to = datetime.now()
    this = to.strftime('%Y-%m-%d')  # 날짜형식
    rooms_id = [33103, 33104, 33105, 33106, 33107, 33108]
    txt = ''
    for li in rooms_id:
        n = rooms_id.index(li)
        rName = rooms_name[n]
        url = "https://www.ddnayo.com/Common/Rsv.ashx?act=GetRoomRate&id_hotel=2674&id_room={0}&idate={1}&su_adult=2&su_child=0&su_baby=0&is_agent=False&su_day=1".format(
            li, this)
        response = requests.get(url)
        charge = BeautifulSoup(response.text, 'html.parser')

        url2 = "https://www.ddnayo.com/RsvSys/Select.aspx?id_hotel=2674&id_room=33106&dt_s={0}".format(this)
        responses = requests.get(url2)
        soups = BeautifulSoup(responses.text, 'html.parser')
        state = soups.text.find(rName)
        if state != -1:
            state = "X"
        else:
            state = "O"

        txt += '{0}/{1}/{2}/{3}\n'.format(pName, rName, charge, state)
    return txt

def seamorning_parser(_url):
    pName = "바다애아침펜션"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    list = soup.select_one('table.pension').select('tr')[1:-1]
    txt = ''
    for li in list:
        rName = li.select_one('label b').text
        charge = li.select('td')[3].text.split("/")[1].split("원")[0]
        state = li.select_one('label span').text
        if state == '완료':
            states = 'O'
        else:
            states = 'X'
        txt += '{0}/{1}/{2}/{3}\n'.format(pName, rName, charge, states)
    return txt

parser_select_dict = {
    'www.ddnayo.com' : army_parser,
    'gpnew.gpension.kr' : gpension_parser,
    'rev.yapen.co.kr' : res_yapen_parser,
    'www.ddnayo2.com' : osean_parser,
    # 'pension.x-y.net' : xy_parser,
    'seamorning.co.kr' : seamorning_parser,
}

file_path = datetime.strftime(to, './%Y-%m-%d PensionHompage (%H-%M-%S).txt')

txt =''
f = open(file_path, 'w', encoding='utf-8')
for url in urls:
    parsed_url = urlparse(url)
    print(parsed_url[1])

    func = parser_select_dict[parsed_url[1]]
    parser = HompageParser(func)
    f.write(parser.parse_url(url))
    print(parser.parse_url(url))
f.close()
