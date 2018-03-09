"""test spider
"""

from spider.spider import Spider

spider = Spider('./spider')
_, jsessionid = spider.login('11711918', '301914')
spider.trans(jsessionid)
