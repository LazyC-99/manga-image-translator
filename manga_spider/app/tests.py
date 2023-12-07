from django.test import TestCase

from app.spider_tool import MangaHubSpider
import subprocess


class Translator(TestCase):
    # 指定要执行的Python程序文件
    python_program = "manga_translator"

    # 定义命令行参数
    args = [
        "-v",
        "--translator=google",
        "-l", "CHS",
        "-m", "batch",
        "--use-cuda",
        "--detector", "ctd",
        "-i", r"C:\Users\Administrator\Desktop\image\test"
    ]

    # 使用 subprocess.run 调用，并捕获输出
    result = subprocess.run(["python", "-m", python_program] + args, capture_output=True)

    # 获取标准输出结果
    output = result.stdout.decode("utf-8")
    print("Output:", output)


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
