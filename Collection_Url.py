#!/usr/bin/env python
# coding : utf8
import sys
import requests
from bs4 import BeautifulSoup
import queue
import threading
import re


class UrlSpider(threading.Thread):
    def __init__(self, qwing):
        threading.Thread.__init__(self)
        self._qwing = qwing

    def run(self):
        while not self._qwing.empty():
            url = self._qwing.get()
            try:
                self.spider(url)
            except Exception:
                pass

    def spider(self, url):
        r = requests.get(url=url)
        req = BeautifulSoup(r.content.decode(), 'lxml')
        link = req.find_all(name='a', attrs={'target': '_blank', 'rel': 'noopener'})
        for i in link:
            # if str('data-url') in i:
            #     print(i)
            # print(i)
            linkplus = requests.get(url=i['data-url'], timeout=6)
            if linkplus.status_code == 200:
                link1 = linkplus.url
                print(link1)
                url_output = open('url.txt', 'a+')
                url_output.write(link1+'\n')
                url_output.close()


def main(key):
    qwing = queue.Queue()
    for i in range(0, 640, 10):
        qwing.put('https://www.so.com/s?q=%s&pn=%s' % (key, str(i)))
    threads = []
    thread_count = 8
    for t in range(thread_count):
        threads.append(UrlSpider(qwing))
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please Input Your Url Address")
        sys.exit(-1)
    else:
        print('Author:wing')
        print('My Bolg:hackerwing.com')
    main(sys.argv[1])







