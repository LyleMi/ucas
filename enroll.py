#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import logging
import requests


CollegeCode = {
    '01': '数学',
    '02': '物理',
    '03': '天文',
    '04': '化学',
    '05': '材料',
    '06': '生命',
    '07': '地球',
    '08': '资环',
    '09': '计算',
    '10': '电子',
    '11': '工程',
    '12': '经管',
    '13': '公管',
    '14': '人文',
    '15': '外语',
    '16': '中丹',
    '17': '国际',
    '18': '存济',
    '19': '微电',
    '20': '网络',
    '21': '未来',
    '22': '',
    '23': '马克',
    '24': '心理',
    '25': '人工',
    '26': '纳米',
    '27': '艺术',
    'TY': '体育'
}


class Login:
    page = 'http://sep.ucas.ac.cn'
    url = page + '/slogin'
    system = page + '/portal/site/226/821'


class Course:
    base = 'http://jwxk.ucas.ac.cn'
    identify = base + '/login?Identity='
    selected = base + '/courseManage/selectedCourse'
    selection = base + '/courseManage/main'
    category = base + '/courseManage/selectCourse?s='
    save = base + '/courseManage/saveCourse?s='


class Cli(object):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    }

    def __init__(self, user, password):
        super(Cli, self).__init__()
        self.initLogger()
        self.initCourse()
        self.s = requests.Session()
        self.s.headers = self.headers
        self.login(user, password)

    def initCourse(self):
        self.courseid = []
        with open("courseid") as fh:
            for c in fh:
                tmp = c.replace(' ', '').strip()
                if len(tmp):
                    self.courseid.append(tmp)

    def initLogger(self):
        formatStr = '[%(asctime)s] [%(levelname)s] %(message)s'
        logger = logging.getLogger("logger")
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        chformatter = logging.Formatter(formatStr)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(chformatter)
        logger.addHandler(ch)
        self.logger = logger

    def login(self, user, password):
        self.s.get(Login.page)
        data = {
            'userName': user,
            'pwd': password,
            'sb': 'sb'
        }
        self.s.post(Login.url, data=data)
        if 'sepuser' not in self.s.cookies.get_dict():
            return False
        r = self.s.get(Login.system)
        identity = r.content.split('<meta http-equiv="refresh" content="0;url=')
        if len(identity) < 2:
            self.logger.error("login fail")
            return
        identityUrl = identity[1].split('"')[0]
        self.identity = identityUrl.split("Identity=")[1].split("&")[0]
        self.s.get(identityUrl)

    def enroll(self):
        r = self.s.get(Course.selected)
        for cid in self.courseid:
            if cid in r.content:
                self.logger.info("%s already selected" % cid)
                continue
            self.enrollCourse(cid)

    def enrollCourse(self, cid):
        r = self.s.get(Course.selection)
        depRe = re.compile(r'<label for="id_([0-9]{3})">(.*)<\/label>')
        deptIds = depRe.findall(r.content)
        for dep in deptIds:
            if CollegeCode[cid[:2]] in dep[1]:
                deptid = dep[0]
                break
        identity = r.content.split('action="/courseManage/selectCourse?s=')[1].split('"')[0]
        data = {
            'deptIds': deptid,
            'sb': 0
        }
        categoryUrl = Course.category + identity
        r = self.s.post(categoryUrl, data=data)
        codeRe = re.compile(r'<span id="courseCode_([A-F0-9]{16})">' + cid + '<\/span>')
        code = codeRe.findall(r.content)[0]
        data = {
            'deptIds': deptid,
            'sids': code
        }
        self.logger.debug("try %s" % cid)
        self.logger.debug(data)
        courseSaveUrl = Course.save + identity
        r = self.s.post(courseSaveUrl, data=data)
        if 'class="error' not in r.content:
            self.logger.info('[Success] ' + cid)
            return True
        else:
            print('[Fail] ' + cid)
            return False


def main():
    with open("auth", "rb") as fh:
        user = fh.readline().strip()
        password = fh.readline().strip()
    c = Cli(user, password)
    c.enroll()


if __name__ == '__main__':
    main()
