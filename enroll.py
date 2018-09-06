#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import time
import random
import pickle
import logging
import requests

from config import Config

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


class NetworkSucks(Exception):
    pass


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
        self.logger = logging.getLogger("logger")
        self.s = requests.Session()
        self.s.headers = self.headers
        self.s.timeout = Config.timeout
        self.login(user, password)
        self.initCourse()

    def get(self, url, *args, **kwargs):
        r = self.s.get(url, *args, **kwargs)
        if r.status_code != requests.codes.ok:
            if r.status_code == requests.codes.moved_permanently:
                raise NetworkSucks
        return r

    def post(self, url, *args, **kwargs):
        r = self.s.post(url, *args, **kwargs)
        if r.status_code != requests.codes.ok:
            raise NetworkSucks
        return r

    def initCourse(self):
        self.courseid = []
        with open("courseid") as fh:
            for c in fh:
                tmp = c.replace(' ', '').strip()
                if len(tmp):
                    self.courseid.append(tmp)

    def login(self, user, password):
        if os.path.exists('cookie.pkl'):
            self.load()
        else:
            self.get(Login.page)
            data = {
                'userName': user,
                'pwd': password,
                'sb': 'sb'
            }
            self.post(Login.url, data=data)
            if 'sepuser' not in self.s.cookies.get_dict():
                return False
            self.save()
        r = self.get(Login.system)
        identity = r.content.split('<meta http-equiv="refresh" content="0;url=')
        if len(identity) < 2:
            self.logger.error("login fail")
            return
        identityUrl = identity[1].split('"')[0]
        self.identity = identityUrl.split("Identity=")[1].split("&")[0]
        self.get(identityUrl)

    def save(self):
        self.logger.debug("save cookie...")
        with open('cookie.pkl', 'wb') as f:
            pickle.dump(self.s.cookies, f)

    def load(self):
        self.logger.debug("loading cookie...")
        with open('cookie.pkl', 'rb') as f:
            cookies = pickle.load(f)
            self.s.cookies = cookies

    def enroll(self):
        r = self.get(Course.selected)
        courseid = []
        self.logger.debug(self.courseid)
        for cid in self.courseid:
            if cid in r.content:
                self.logger.info("%s already selected" % cid)
                continue
            if not self.enrollCourse(cid):
                self.logger.debug("try %s fail" % cid)
                courseid.append(cid)
            else:
                self.logger.debug("try %s suc" % cid)
        return courseid

    def enrollCourse(self, cid):
        r = self.get(Course.selection)
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
        r = self.post(categoryUrl, data=data)
        codeRe = re.compile(r'<span id="courseCode_([A-F0-9]{16})">' + cid + '<\/span>')
        code = codeRe.findall(r.content)[0]
        data = {
            'deptIds': deptid,
            'sids': code
        }
        courseSaveUrl = Course.save + identity
        r = self.post(courseSaveUrl, data=data)
        if 'class="error' not in r.content:
            return True
        else:
            return False


def initLogger():
    formatStr = '[%(asctime)s] [%(levelname)s] %(message)s'
    logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    chformatter = logging.Formatter(formatStr)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(chformatter)
    logger.addHandler(ch)


def main():
    initLogger()
    with open("auth", "rb") as fh:
        user = fh.readline().strip()
        password = fh.readline().strip()
    c = Cli(user, password)
    while True:
        try:
            courseid = c.enroll()
            if not courseid:
                break
            c.courseid = courseid
            time.sleep(random.randint(Config.minIdle, Config.maxIdle))
        except KeyboardInterrupt as e:
            c.logger.info("user abored")
            break
        except (
            NetworkSucks, 
            requests.exceptions.ConnectionError, 
            requests.exceptions.ConnectTimeout
        ) as e:
            c.logger.debug("network error")
            c.login(user, password)
        except Exception as e:
            c.logger.error(repr(e))
            c.login(user, password)


if __name__ == '__main__':
    main()
