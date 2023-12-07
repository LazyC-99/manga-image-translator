from django.test import TestCase

from app.spider_tool import MangaHubSpider


# 爬虫程序
class Spider(TestCase):
    spider = MangaHubSpider()
    while 1:
        choose = int(input("1.pop manga 2.search manga 0.exit"))
        if choose == 1:
            manga_list = spider.get_pop_manga()
            for i, manga in enumerate(manga_list, start=1):
                print(f'{i}.{manga["name"]}')
            choose = int(input("choose manga:"))
            manga = manga_list[choose - 1]
            print(manga)
            while 1:
                down = int(input("1.download 2.cancel"))
                if down == 1:
                    spider.down_manga(manga)
                if down == 2:
                    break

        if choose == 2:
            keyword = input("input key words:").strip()
            manga_list = spider.search_manga(keyword)
            for i, manga in enumerate(manga_list, start=1):
                print(f'{i}.{manga["name"]}')
            choose = int(input("choose manga:"))
            manga = manga_list[choose - 1]
            print(manga)
            while 1:
                down = int(input("1.download 2.cancel"))
                if down == 1:
                    spider.down_manga(manga)
                if down == 2:
                    break
        if choose == 0:
            break
