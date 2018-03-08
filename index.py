from bs4 import BeautifulSoup
from random import Random
import requests
import datetime
import os

time = [['0800', '0950'], ['1020', '1210'], [
    '1400', '1550'], ['1620', '1810'], ['1900', '2050']]
classtime = {'第1 2节': 0, '第3 4节': 1, '第5 6节': 2, '第7 8节': 3, '第9 10节': 4}
reminderList = ["-PT10M", "-PT30M", "-PT1H", "-PT2H", "-P1D"]


def random_str(randomlength):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


def bet(str, tag1, tag2):
    index1 = 0
    if (str.find(tag1, 0, len(str)) != -1):
        index1 = str.find(tag1, 0, len(str)) + len(tag1)
    index2 = index1
    if (str.find(tag2, index1, len(str)) != -1):
        index2 = str.find(tag2, index1, len(str))
    return str[index1:index2]


def save(string):
    f = open(os.getcwd() + "/class.ics", 'wb')
    f.write(string.encode("utf-8"))
    f.close()


def event(date, className, startTime, endTime, location):
    DONE_CreatedTime = datetime.datetime.now().strftime("%Y%m%dT%H%M%S") + "Z"
    DONE_ALARMUID = random_str(30) + "&Wycer"
    DONE_UnitUID = random_str(20) + "&Wycer"
    DONE_reminder = reminderList[1]
    # eventString = "BEGIN:VEVENT\n"
    # eventString = eventString + "CREATED:" + DONE_CreatedTime
    # eventString = eventString + "\nUID:" + MakeString(20)
    # eventString = eventString + "\nDTEND;TZID=Asia/Shanghai:" + \
    #     date + "T" + endTime + "00"
    # eventString = eventString + \
    #     "\nTRANSP:OPAQUE\nX-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\nSUMMARY:" + className
    # eventString = eventString + "\nDTSTART;TZID=Asia/Shanghai:" + \
    #     date + "T" + startTime + "00"
    # eventString = eventString + "\nDTSTAMP:" + DONE_CreatedTime
    # eventString = eventString + "\nLOCATION:" + location
    # eventString = eventString + "\nSEQUENCE:0\nBEGIN:VALARM\nX-WR-ALARMUID:" + DONE_ALARMUID
    # eventString = eventString + "\nUID:" + DONE_UnitUID
    # eventString = eventString + "\nTRIGGER:" + DONE_reminder
    # eventString = eventString + \
    #     "\nDESCRIPTION:该上课啦\nACTION:DISPLAY\nEND:VALARM\n"
    # eventString = eventString + "END:VEVENT\n"

    eventString = """
    BEGIN:VEVENT
    CREATED:%s
    UID:%s
    DTEND;TZID=Asia/Shanghai:%s
    TRANSP:OPAQUE
    X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC
    SUMMARY:%s
    DTSTART;TZID=Asia/Shanghai:%s
    DTSTAMP:%s
    LOCATION:%s
    SEQUENCE:0
    BEGIN:VALARM
    X-WR-ALARMUID:%s
    UID:%s
    TRIGGER:%s
    ACTION:DISPLAY
    END:VALARM
    END:VEVENT
    """ % (DONE_CreatedTime, MakeString(20), \
        date + "T" + endTime + "00", className, \
        date + "T" + startTime + "00", DONE_CreatedTime, location, \
        DONE_ALARMUID, DONE_UnitUID, DONE_reminder)

    return eventString


def MakeString(length):
    return random_str(length) + "&Wycer"

session = requests.Session()
html = session.get(
    'https://cas.sustc.edu.cn/cas/login?service=http://jwxt.sustc.edu.cn/jsxsd/').content
soup = BeautifulSoup(html, 'lxml')
form = soup.find('form', id='fm1')

hidden = form.find_all('input', type='hidden')
execution = hidden[0].get('value')

params = {
    "username": 'id',
    "password": 'password',
    "_eventId": "submit",
    "geolocation": "",
    "execution": execution
}

session.post('https://cas.sustc.edu.cn/cas/login?service=http://jwxt.sustc.edu.cn/jsxsd/framework/xsMain.jsp',
             data=params)
try:
    print(session.cookies['JSESSIONID'])
except KeyError:
    print('登录失败')
else:
    print('qwq')
exit(0)

base = datetime.datetime.strptime('2018-02-26 12:00:00', '%Y-%m-%d %H:%M:%S')
delta = datetime.timedelta(days=1)

params = {
    "sfFD": 1,
    "xnxq01id": '2017-2018-2',
    "zc": i
}
html = session.post(
    'http://jwxt.sustc.edu.cn/jsxsd/xskb/xskb_list.do', data=params).text
soup = BeautifulSoup(html, "lxml")
trs = soup.find_all(name='tr')
row, col = 1, 0
res = ""

for tr in trs:
    soup = BeautifulSoup(str(tr), "lxml")
    tds = soup.find_all(name='td')
    for td in tds:
        div = td.find('div')
        if div != None and div.get_text().strip() != "":
            print(div.get_text())
            tmp = bet(str(div), '>', '</div>').split('<font')
            if len(tmp) != 1:
                date = base + delta * ((i - 1) * 7 + col - 1)
                classname = bet('#' + tmp[0], '#', '<br/>')
                location = bet(tmp[2], '>', '<')
                res += event(date.strftime('%Y%m%d'), classname,
                                time[row - 1][0], time[row - 1][1], location)
                print(classname)
        col = col + 1
        if (col == 8):
            col = 1
            row = row + 1
icsString = """
BEGIN:VCALENDAR
METHOD:PUBLISH
VERSION:2.0
X-WR-CALNAME:课程表
PRODID:-//Apple Inc.//Mac OS X 10.12//EN
X-APPLE-CALENDAR-COLOR:#FC4208
X-WR-TIMEZONE:Asia/Shanghai
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Asia/Shanghai
BEGIN:STANDARD
TZOFFSETFROM:+0900
RRULE:FREQ=YEARLY;UNTIL=19910914T150000Z;BYMONTH=9;BYDAY=3SU
DTSTART:19890917T000000
TZNAME:GMT+8
TZOFFSETTO:+0800
END:STANDARD
BEGIN:DAYLIGHT
TZOFFSETFROM:+0800\nDTSTART:19910414T000000
TZNAME:GMT+8
TZOFFSETTO:+0900
RDATE:19910414T000000
END:DAYLIGHT
END:VTIMEZONE
%s
END:VCALENDAR
""" % res
#save(icsString)
#print("icsCreateAndSave")
os.chdir(os.getcwd())
