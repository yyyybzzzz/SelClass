import requests
from bs4 import BeautifulSoup
import re


class Login(object):
    def __init__(self, uname, pwd, url):
        self.uname = uname
        self.pwd = pwd
        self.url = url
        # print(self.url)

    # 获取LT等参数
    def getLT(self):
        res = requests.get(self.url)
        inputs = BeautifulSoup(
            res.text, features="html5lib").findAll('input', {'type': 'hidden'})
        d = {}
        for it in inputs:
            d[it.attrs['name']] = it.attrs['value']
        return res.cookies, d

    # 获取 cookies
    def getCookies(self):
        cookies, data = self.getLT()
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            'Cookie':
            'JSESSIONID=' + cookies['JSESSIONID']
        }

        data['username'] = self.uname
        data['password'] = self.pwd
        res = requests.post(self.url, data=data, headers=headers)
        return res.history[1].cookies

    # 获取Eid
    def getEID(self):
        url = 'http://yjxt.bupt.edu.cn/Gstudent/leftmenu.aspx?UID=' + self.uname
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            'Cookie':
            self.cookies
        }
        res = requests.get(url, headers=headers)
        html = res.text
        patern = r'Course/PlanCourseOnlineSel.aspx\?EID=[a-z|A-Z|0-9|=]*'
        eid = re.findall(re.compile(patern), html)[0][36:]
        return eid

    # 返回eid和cookies
    def login(self):

        # 获取 cookie
        cookie = self.getCookies()
        self.cookies = 'DropDownListYx_xsbh=DropDownListYx_xsbh=; DropDownListXqu=DropDownListXqu=1; ASP.NET_SessionId=' + cookie['ASP.NET_SessionId']
        # 获取eid
        self.EID = self.getEID()
        print(self.cookies, self.EID)


l = Login(
    '2018110704', '06042415',
    'https://auth.bupt.edu.cn/authserver/login?service=http://yjxt.bupt.edu.cn/ULogin.aspx'
)
l.login()