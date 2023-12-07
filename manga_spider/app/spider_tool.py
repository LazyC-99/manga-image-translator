from time import sleep

import requests
from fake_useragent import UserAgent
from googletrans import Translator
from lxml import etree
import os
import concurrent.futures

from .models import Manga


# from manga_spider.manga_spider.apps import db


class MangaHubSpider(object):
    BASE_URL = 'https://mangahub.io/'
    IMAGE_DIRECTORY = 'C:/Users/Administrator/Desktop/image/'
    MAX_RETRIES = 5
    MAX_IMG_GUESSED = 30

    def __init__(self):
        self.cur_pop_page = 1
        self.ua = UserAgent()
        self.headers = {'User-Agent': self.ua.random}
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

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
                        'latest': float(div.xpath(".//div[@class=\'media-body\']/span/a/text()")[1]),
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
        # 每部分前4话|后面部分
        url_list = parse_html.xpath("//div[@class='tab-content']//li[position()<=4]//a[1]/@href|//div["
                                    "@class='tab-content']//li[position()>4]//a[2]/@href")
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
    def get_chapter_img(self, url):
        result = {}
        img_list = []
        trans_list = []
        # 使用 requests模块得到响应对象
        html = self.repeat_request(url).text
        parse_html = etree.HTML(html)
        name = parse_html.xpath("//div[@id='mangareader']//h3//a/text()")[0]
        # 解析图片地址模板 尝试获取最新图片
        # img_url_template: https://imgx.mghubcdn.com/solo-leveling/1/1.jpg
        img_url_template = parse_html.xpath("//div[@id='mangareader']//img/@src")[0]
        index = img_url_template.rfind('/')
        pre = img_url_template[:index + 1]
        suf = img_url_template[index + 2:]
        chapter = img_url_template.split('/')[-2]

        for i in range(1, self.MAX_IMG_GUESSED):
            # 组装原网站图片路径
            img_link = f'{pre}{i}{suf}'
            # 替换掉空格 否则访问不到
            name_dir = name.replace(" ", "-") + "-translated"
            # 组装翻译图片路径 static为setting中设置的翻译图片根目录路径
            trans_link = f'/static/{name_dir}/{chapter}/{i}{suf}'
            # 直到响应404之前都是有图片的
            # response = requests.get(img_link, headers=self.headers, stream=True)
            # if response.status_code == 404:
            #     print("下载完成")
            #     break
            # else:
            #     img_list.append(img_link)
            img_list.append(img_link)
            trans_list.append(trans_link)
        result = {
            "imgs": img_list,
            "trans_imgs": trans_list
        }
        # 存储图片的url链接
        return result

    # 下载单章节图片
    # url: chapters地址
    # word: manga名字
    def down_single_chapter_img(self, url, name):
        # 使用 requests模块得到响应对象
        html = self.repeat_request(url).text
        parse_html = etree.HTML(html)
        # 解析图片地址模板 尝试获取最新图片
        # img_url_template: https://imgx.mghubcdn.com/solo-leveling/1/1.jpg
        img_url_template = parse_html.xpath("//div[@id='mangareader']//img/@src")[0]
        index = img_url_template.rfind('/')
        chapter = img_url_template.split('/')[-2]
        pre = img_url_template[:index + 1]
        suf = img_url_template[index + 2:]

        for i in range(1, self.MAX_IMG_GUESSED):
            img_link = f'{pre}{i}{suf}'
            # 直到响应404之前都是有图片的
            response = requests.get(img_link, headers=self.headers, stream=True)
            if response.status_code == 404:
                # TODO 多线程下保证最新章节正确
                Manga.objects.filter(name=name).update(download=chapter)
                print(f'第{chapter}话下载完成')
                break
            else:
                # 保存路径 替换掉空格
                name_dir = name.replace(" ", "-")
                directory = os.path.join(self.IMAGE_DIRECTORY, name_dir, chapter)
                os.makedirs(directory, exist_ok=True)
                img_filename = os.path.join(directory, f'{i}.jpg')
                with open(img_filename, 'wb') as f:
                    f.write(response.content)
                    print(f'第{chapter}话已下载: {i}张')

    # 获取全章图片
    # cps: 章节列表
    # word: manga名字
    def down_manga(self, item):
        print(f'开始下载-----------{item}')
        # 查询数据库是否下载过
        comic_db = Manga.objects.filter(name=item["name"]).first()
        download = 0
        if comic_db is None:
            # 数据库没有  新插入
            # 翻译漫画名
            translator = Translator()
            translation = translator.translate(item['name'], dest='zh-cn').text
            Manga.objects.create(name=item['name'], trans_name=translation, detail_link=item['detail_link'],
                                 cover_img=item['img'],
                                 latest=item['latest'], status=item['status'], styles=', '.join(item['styles']))

        else:
            # 有了 判断需不需要更新
            # 1.判断latest是否最新
            # 2.判断download是否最新
            if comic_db.latest == item["latest"]:
                Manga.objects.filter(name=item["name"]).update(latest=item["latest"])

            if comic_db.download == item["latest"]:
                print(f"{item['name']}已是最新")
                return
            else:
                download = comic_db.download
        cps = self.get_manga_chapters(item["detail_link"])
        name = item["name"]
        # 创建一个任务列表
        download_tasks = []
        # 创建线程池任务
        with self.executor as executor:
            for chapter in reversed(cps):
                if float(chapter["chapter_id"]) > float(download):
                    # 使用 submit 方法将任务提交给线程池
                    task = executor.submit(self.down_single_chapter_img, chapter["chapter_link"], name)
                    download_tasks.append(task)
                else:
                    print(f"第{chapter['chapter_id']}已下载过")
            # 等待所有下载任务完成
            concurrent.futures.wait(download_tasks)

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
                retries += 1
                print(f"repeat...{retries}", e)
                sleep(1)


# if __name__ == '__main__':
#     spider = MangaHubSpider()
#
#     manga_list = spider.get_pop_manga()
#     spider.down_manga(manga_list[1])

# manga_list = spider.get_pop_manga()
# chapters = spider.get_manga_chapters(manga_list[1]["detail_link"])
# img = spider.get_chapter_img(chapters[0]["chapter_link"])
# print(img)
