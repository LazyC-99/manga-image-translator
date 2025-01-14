from django.test import TestCase

from app.models import Genres, Order
from app.spider_tool import MangaHubSpider
import subprocess
from googletrans import Translator
from httpcore._exceptions import ReadTimeout


def ImportGenres():
    # 手动获取:https://mangahub.io/search
    # xpath: //ul[@class='dropdown-menu dropdown-menu-right']//li//text()
    genres_list = [
        "Action", "Adventure", "Comedy", "Adult", "Drama", "Historical", "Martial Arts",
        "Romance", "Ecchi", "Supernatural", "Webtoons", "Manhwa", "Fantasy", "Harem",
        "Shounen", "Manhua", "Mature", "Seinen", "Sports", "School Life", "Smut",
        "Mystery", "Psychological", "Shounen ai", "Slice of life", "Shoujo ai",
        "Cooking", "Horror", "Tragedy", "Doujinshi", "Sci-Fi", "Yuri", "Yaoi", "Shoujo",
        "Gender bender", "Josei", "Mecha", "Medical", "Magic", "4-Koma", "Music",
        "Webtoon", "Isekai", "Game", "Award Winning", "Oneshot", "Demons", "Military",
        "Police", "Super Power", "Food", "Kids", "Magical Girls", "Wuxia", "Superhero",
        "Thriller", "Crime", "Philosophical", "Adaptation", "Full Color", "Crossdressing",
        "Reincarnation", "Manga", "Cartoon", "Survival", "Comic", "English", "Harlequin",
        "Time Travel", "Traditional Games", "Reverse Harem", "Animals", "Aliens", "Loli",
        "Video Games", "Monsters", "Office Workers", "System", "Villainess", "Zombies",
        "Vampires", "Violence", "Monster Girls", "Anthology", "Ghosts", "Delinquents",
        "Post-Apocalyptic", "Xianxia", "Xuanhuan", "R-18", "Cultivation", "Rebirth",
        "Gore", "Russian", "Samurai", "Ninja", "Revenge", "Cheat Systems", "Dungeons",
        "Overpowered"
    ]

    order_list = [
        "POPULAR", "LATEST", "ALPHABET", "NEW", "COMPLETED"
    ]
    translator = Translator()
    Genres.objects.all().delete()
    for index, genre_name in enumerate(genres_list):
        genre_name = genre_name.replace(' ', '-')

        translation_attempt = 0
        translation = None

        while translation_attempt < 3:  # 最大重试次数
            try:
                # TODO 多线程翻译
                translation = translator.translate(genre_name, dest='zh-cn')
                translation = translation.text  # 获取翻译文本
                break  # 如果成功翻译，跳出循环
            except ReadTimeout as e:
                print(f"请求超时: {e}")
                translation_attempt += 1
                # 在此处添加处理超时的代码，例如等待一段时间后重试

        if translation is not None:
            Genres.objects.create(id=index + 1, name=genre_name.lower(), trans_name=translation)
            print(f'insert genres:{index + 1}/{len(genres_list)}')
        else:
            print(f'无法翻译 {genre_name}，已达到最大重试次数')

    Order.objects.all().delete()
    for index, order_name in enumerate(order_list):
        translation = translator.translate(order_name, dest='zh-cn').text
        Order.objects.create(id=index + 1, name=order_name, trans_name=translation)
        print(f'insert order:{index + 1}/{len(order_list)}')


def CallTranslator():
    # 指定要执行的Python程序文件
    # python_program = "E:/workspace_py/hello.py"
    python_program = "manga_translator"
    # 定义命令行参数
    args = [
        "-v",
        "--translator=google",
        "-l", "CHS",
        "-m", "batch",
        "--use-cuda",
        "--detector", "ctd",
        "-i", r"C:/Users/Administrator/Desktop/image/test"
    ]

    # 使用 subprocess.run 调用，并捕获输出
    # result = subprocess.run(["python", "-m", python_program] + args, capture_output=True)
   # result = subprocess.run(['python', '-m manga_translator -v --translator=google -l CHS -m batch --use-cuda --detector ctd  -i C:/Users/Administrator/Desktop/image/test'], capture_output=True, text=True)
    result = subprocess.run(["python", "-m", python_program] + args, capture_output=True, text=True, cwd="E:/workspace_py/manga-image-translator")
    # 获取标准输出结果
    print(result.stderr)
    print(result.stdout)

# 爬虫程序
# class Spider(TestCase):
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
#             choose = int(input("choose manga:"))
#             manga = manga_list[choose - 1]
#             print(manga)
#             while 1:
#                 down = int(input("1.download 2.cancel"))
#                 if down == 1:
#                     spider.down_manga(manga)
#                 if down == 2:
#                     break
#         if choose == 0:
#             break
