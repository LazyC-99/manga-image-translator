from time import sleep

import requests
from fake_useragent import UserAgent
from lxml import etree
import random
import os
from urllib import parse


class MangaHubSpider(object):
    BASE_URL = 'https://mangahub.io/'
    IMAGE_DIRECTORY = 'C:/Users/Administrator/Desktop/image/'
    MAX_RETRIES = 5
    MAX_IMG_GUESSED = 30

    def __init__(self):
        self.cur_pop_page = 1
        self.ua = UserAgent()
        self.headers = {'User-Agent': self.ua.random}

    # 获取manga对象
    def get_manga_list(self, url):
        html = self.repeat_request(url).text
        parse_html = etree.HTML(html)
        item_div_list = parse_html.xpath("//div[@class='row']/div")
        pop_list = []
        try:
            for div in item_div_list:
                item = {'name': div.xpath(".//h4[@class=\'media-heading\']/a/text()")[0],
                        'detail_link': div.xpath(".//div[@class=\'media-left\']/a/@href")[0],
                        'img': div.xpath(".//div[@class=\'media-left\']/a/img/@src")[0],
                        'latest': div.xpath(".//div[@class=\'media-body\']/span/a/text()")[1],
                        'status': div.xpath(".//div[@class=\'media-body\']/span/text()")[2],
                        'styles': div.xpath(".//div[@class=\'media-body\']/p/a/text()"),
                        }
                pop_list.append(item)
        finally:
            return pop_list

    # 流行排行
    def get_pop_manga(self):
        pop_url = f'{self.BASE_URL}popular/page/{self.cur_pop_page}'
        return self.get_manga_list(pop_url)

    # 搜索
    def search_manga(self, manga_name):
        search_url = f'{self.BASE_URL}search?order=POPULAR&genre=all&q={manga_name}'
        return self.get_manga_list(search_url)

    # 获取章节和地址
    # url: manga详细地址
    def get_manga_chapters(self, url):
        html = self.repeat_request(url).text
        parse_html = etree.HTML(html)
        url_list = parse_html.xpath("//div[@class='tab-content']//li//a[2]/@href")
        chapters_url_list = []
        for chapters in url_list:
            # "https://mangahub.io/chapter/martial-peak/chapter-3596"
            chapter_number = chapters.split("-")[-1]
            item = {
                'chapter_id': chapter_number,
                'chapter_link': chapters
            }
            chapters_url_list.append(item)
        return chapters_url_list

    # 获取当章节图片
    # url: chapters地址
    # word: manga名字
    def get_chapter_img(self, url):
        img_list = []
        # 使用 requests模块得到响应对象
        html = self.repeat_request(url).text
        parse_html = etree.HTML(html)
        # 解析图片地址模板 尝试获取最新图片
        # img_url_template: https://imgx.mghubcdn.com/solo-leveling/1/1.jpg
        img_url_template = parse_html.xpath("//div[@id='mangareader']//img/@src")[0]
        index = img_url_template.rfind('/')
        pre = img_url_template[:index + 1]
        suf = img_url_template[index + 2:]
        # 直到响应404之前都是有图片的
        for i in range(1, self.MAX_IMG_GUESSED):
            img_link = f'{pre}{i}{suf}'
            # response = requests.get(img_link, headers=self.headers, stream=True)
            # if response.status_code == 404:
            #     print("下载完成")
            #     break
            # else:
            #     img_list.append(img_link)
            img_list.append(img_link)
        # 存储图片的url链接
        return img_list

    def down_single_chapter_img(self, url, word):
        # 使用 requests模块得到响应对象
        html = self.repeat_request(url).text
        parse_html = etree.HTML(html)
        # 正则解析
        img_link_list = parse_html.xpath("//div[@id='mangareader']//img/@src")
        # 存储图片的url链接
        print(img_link_list)
        # 从链接末尾获取章节号
        chapters = url.split("-")[-1]
        # 保存路径
        directory = os.path.join(self.IMAGE_DIRECTORY, word, chapters)
        os.makedirs(directory, exist_ok=True)

        for i, img_link in enumerate(img_link_list, start=1):
            img_filename = os.path.join(directory, f'{i}.jpg')
            self.save_image(img_link, img_filename)
            print(f'已下载 {i}/{len(img_link_list)}')

    # 获取全章图片
    # cps: 章节列表
    # word: manga名字
    def down_manga(self, manga_item):
        cps = self.get_manga_chapters(manga_item)
        name = manga_item["name"]
        for chapter in reversed(cps):
            self.down_single_chapter_img(chapter["chapter_link"], name)

    # 下载图片
    def save_image(self, img_link, filename):
        response = requests.get(img_link, headers=self.headers, stream=True)
        if response.status_code == 404:
            print("下载完成")
            return True
        else:
            with open(self.IMAGE_DIRECTORY + filename, 'wb') as f:
                f.write(response.content)
                print(filename, f'下载成功{filename}')
                return False

    def repeat_request(self, url):
        retries = 0
        while retries < self.MAX_RETRIES:
            try:
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print("repeat...", e)
                sleep(1)


if __name__ == '__main__':
    spider = MangaHubSpider()
    imgs = spider.get_chapter_img("https://mangahub.io/chapter/solo-leveling_105/chapter-1")
    print(imgs)
    # for i in range(0, 3):
    #     if spider.save_image(f'https://imgx.mghubcdn.com/solo-leveling/1/{i}.jpg', f'{i}.jpg'):
    #         break

# if __name__ == '__main__':
#     spider = MangaHubSpider()
#     while 1:
#         choose = int(input("1.pop manga 2.search manga 0.exit"))
#         if choose == 1:
#             manga_list = spider.get_pop_manga()
#             for i, manga in enumerate(manga_list, start=1):
#                 print(f'{i}.{manga["name"]}')
#             choose = int(input("choose manga:"))
#             manga = manga_list[choose - 1]
#             print(manga)
#             while 1:
#                 down = int(input("1.download 2.cancel"))
#                 if down == 1:
#                     spider.down_manga(manga)
#                 if down == 2:
#                     break
#
#         if choose == 2:
#             keyword = input("input key words:").strip()
#             manga_list = spider.search_manga(keyword)
#             for i, manga in enumerate(manga_list, start=1):
#                 print(f'{i}.{manga["name"]}')
#         if choose == 0:
#             break
