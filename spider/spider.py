"""A spider for login and transform class schedule for SUSTech Teaching Affair System

"""

import os
import os.path
from random import Random
import datetime
import requests
from bs4 import BeautifulSoup


def MakeString(length):
    """Create a unique string with specific length

    Arguments:
        length {integer} -- specify the string's length

    Returns:
        string -- the specific length string
    """

    return random_str(length) + "&Wycer"


def random_str(randomlength):
    """create a random string

    Arguments:
        randomlength {integer} -- the length of the random string

    Returns:
        string -- the random string
    """

    res = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        res += chars[random.randint(0, length)]
    return res


def save(string):
    """Save a string to class.ics

    Arguments:
        string {string} -- filename
    """

    f = open(os.getcwd() + "/class.ics", 'wb')
    f.write(string.encode("utf-8"))
    f.close()


def between(string, tag1, tag2):
    """Get the string between two specific string in a string

    Arguments:
        string {string} -- the long string
        tag1 {string} -- the string's left tag
        tag2 {string} -- the string's right tag

    Returns:
        string -- the string between left tag and right tag
    """

    index1 = 0
    if string.find(tag1, 0, len(string)) != -1:
        index1 = string.find(tag1, 0, len(string)) + len(tag1)
    index2 = index1
    if string.find(tag2, index1, len(string)) != -1:
        index2 = string.find(tag2, index1, len(string))
    return string[index1:index2]


class Spider():
    """A spider class

    Methods:
        login(username, password) -- login CAS system
        trans(JSESSIONID) -- download class schedule to ics file
    """

    def __init__(self, path):
        """Init Spider

        Arguments:
            path {string} -- specify the runtime path
        """
        file = open(os.path.join(path, 'model/calendar'))
        self.calendar_model = file.read()
        file.close()

        file = open(os.path.join(path, 'model/event'))
        self.event_model = file.read()
        file.close()

        self.time = [['0800', '0950'], ['1020', '1210'], [
            '1400', '1550'], ['1620', '1810'], ['1900', '2050']]
        self.classtime = {'第1 2节': 0, '第3 4节': 1,
                          '第5 6节': 2, '第7 8节': 3, '第9 10节': 4}
        self.reminderList = ["-PT10M", "-PT30M", "-PT1H", "-PT2H", "-P1D"]

    @classmethod
    def login(cls, username, password):
        """login SUSTech CAS system

        Arguments:
            username {string} -- student ID for CAS
            password {string} -- password for CAS

        Returns:
            [integer, string] -- code, res
        """
        session = requests.Session()
        html = session.get(
            'https://cas.sustc.edu.cn/cas/login?service=http://jwxt.sustc.edu.cn/jsxsd/').content
        soup = BeautifulSoup(html, 'lxml')
        form = soup.find('form', id='fm1')

        hidden = form.find_all('input', type='hidden')
        execution = hidden[0].get('value')

        params = {
            "username": username,
            "password": password,
            "_eventId": "submit",
            "geolocation": "",
            "execution": execution
        }
        session.post('https://cas.sustc.edu.cn/cas/login?service=http://jwxt.sustc.edu.cn/jsxsd/framework/xsMain.jsp',
                     data=params)

        try:
            res = session.cookies['JSESSIONID']
        except KeyError:
            return -1, 'login failed'
        return 0, res

    def trans(self, JSESSIONID):
        """Spider the content on teaching system and transform it to ics file

        Arguments:
            JSESSIONID {string} -- can get from login methods. use for cookies.
        """

        base = datetime.datetime.strptime(
            '2018-02-26 12:00:00', '%Y-%m-%d %H:%M:%S')
        delta = datetime.timedelta(days=1)

        _, zc, _ = datetime.datetime.now().isocalendar()
        zc = zc - 8
        params = {
            "sfFD": 1,
            "xnxq01id": '2017-2018-2',
            "zc": zc
        }
        cookies = {
            'JSESSIONID': JSESSIONID
        }
        html = requests.post(
            'http://jwxt.sustc.edu.cn/jsxsd/xskb/xskb_list.do', data=params, cookies=cookies).text
        soup = BeautifulSoup(html, "lxml")
        trs = soup.find_all(name='tr')
        row, col = 1, 0
        _, zc, _ = datetime.datetime.now().isocalendar()
        zc = zc - 8
        res = ""

        for tr in trs:
            soup = BeautifulSoup(str(tr), "lxml")
            tds = soup.find_all(name='td')
            for td in tds:
                div = td.find('div')
                if div != None and div.get_text().strip() != "":
                    tmp = between(str(div), '>', '</div>').split('<font')
                    if len(tmp) != 1:
                        date = base + delta * ((zc - 1) * 7 + col - 1)
                        classname = between('#' + tmp[0], '#', '<br/>')
                        location = between(tmp[2], '>', '<')
                        res += self.event(date.strftime('%Y%m%d'), classname,
                                          self.time[row - 1][0], self.time[row - 1][1], location)
                col = col + 1
                if col == 8:
                    col = 1
                    row = row + 1
        save(self.calendar_model % res)
        return 0, 'class.ics'

    def event(self, date, className, startTime, endTime, location):
        """Return a string describing a lesson's information in ics format

        Arguments:
            date {string} -- The lesson's date
            className {string} -- The lesson's title
            startTime {date.date} -- The lesson's begin time
            endTime {date.date} -- The lesson's end time
            location {string} -- The lesson's location

        Returns:
            [string] -- [event string]
        """

        DONE_CreatedTime = datetime.datetime.now().strftime("%Y%m%dT%H%M%S") + "Z"
        DONE_ALARMUID = MakeString(30)
        DONE_UnitUID = MakeString(20)
        DONE_reminder = self.reminderList[1]
        return self.event_model % (DONE_CreatedTime, MakeString(20),
                                   date + "T" + endTime + "00", className,
                                   date + "T" + startTime + "00", DONE_CreatedTime, location,
                                   DONE_ALARMUID, DONE_UnitUID, DONE_reminder)


if __name__ == '__main__':
    spider = Spider('.')
    spider.trans(spider.login('11711918', '301914'))
