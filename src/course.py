import requests
import re
from bs4 import BeautifulSoup


class Course(object):
    def __init__(self, url, cookies):
        self.url = url
        self.cookies = cookies

    def getCourses(self):
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            'Cookie':
            self.cookies
        }
        res = requests.get(self.url, headers=headers)
        trs = BeautifulSoup(res.text, features="html5lib").findAll('tr')
        l = {}
        for tr in trs:
            tmp = str(tr).replace(' ', '').replace('\n', '')
            if '正在选课' in tmp and '退选课程' not in tmp:
                course = {}
                pid = r'<tdalign="center"style="white-space:nowrap;">([0-9]*)</td>'
                id = re.findall(re.compile(pid), tmp)[0]
                purl = r'selClass\(\'([\s\S]*),\'selClass\'\)'
                url = re.findall(re.compile(purl), tmp)[0]

                course[
                    'url'] = 'http://yjxt.bupt.edu.cn/Gstudent/Course/PlanSelClass.aspx' + url.replace(
                        '&amp;', '&')
                course['class'] = {}
                l[id] = course
        return l

    def getClass(self, courseId, className):
        payload = {}
        d = self.getCourses()
        self.url = d[courseId]['url']
        headers = {
            'Content-Type':
            'application/x-www-form-urlencoded',
            'User-Agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
            'Cookie':
            self.cookies
        }
        res = requests.get(self.url, headers=headers)
        html5 = BeautifulSoup(res.text, features="html5lib")
        trs = html5.findAll('tr')
        for tr in trs[3:]:
            tmp = str(tr).replace(' ', '').replace('\n', '')
            pname = r'<aclass=\"none\"href=\"javascript:void\(0\)\"id=\"contentParent_dgData_hykClass_[0-9]+[\s\S]*\">([\s\S]*)<\/a>'
            classname = re.findall(re.compile(pname), tmp)[0]
            # print(classname)
            if className != classname:
                continue
            else:
                form = html5.findAll('form')[0]
                payload['__VIEWSTATE'] = form.findAll(
                    'input', {'id': '__VIEWSTATE'})[0]['value']
                payload['__LASTFOCUS'] = form.findAll(
                    'input', {'id': '__LASTFOCUS'})[0]['value']
                payload['__EVENTTARGET'] = form.findAll(
                    'input', {'id': '__EVENTTARGET'})[0]['value']
                payload['__EVENTARGUMENT'] = form.findAll(
                    'input', {'id': '__EVENTARGUMENT'})[0]['value']
                payload['__VIEWSTATEGENERATOR'] = html5.findAll(
                    'input', {'name': '__VIEWSTATEGENERATOR'})[0]['value']
                payload['__VIEWSTATEENCRYPTED'] = html5.findAll(
                    'input', {'name': '__VIEWSTATEENCRYPTED'})[0]['value']
                payload['__EVENTVALIDATION'] = html5.findAll(
                    'input', {'name': '__EVENTVALIDATION'})[0]['value']
                payload['_ASYNCPOST'] = True
                btn = tr.findAll('input', {'type': 'image'})[0]['name']
                payload['ctl100$ScriptManager1'] = btn
                self.url = 'http://yjxt.bupt.edu.cn/Gstudent/Course/' + form['action']
                payload['ctl00$contentParent$dgData$ctl02$ImageButton1.x'] = 13
                payload['ctl00$contentParent$dgData$ctl02$ImageButton1.y'] = 8
                res = requests.post(self.url, headers=headers, data=payload)
                print("选课完成")

