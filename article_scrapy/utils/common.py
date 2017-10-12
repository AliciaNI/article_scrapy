#coding:utf-8
__author__ = 'nj'

import hashlib

def get_md5(url):
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest

if __name__ == '__main__':
    print(get_md5("https://www.jobbole.com".encode('utf-8')))
