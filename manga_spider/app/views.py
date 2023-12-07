import os

from django.http import HttpResponse, JsonResponse
import json
from django.conf import settings
from django.shortcuts import render

from . import spider_tool

spider = spider_tool.MangaHubSpider()


def index(request):
    return render(request, 'index.html')


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        query = request.GET['q']
    else:
        query = ' '
    search_list = spider.search_manga(query)
    return JsonResponse(search_list, safe=False)


def pop(request):
    request.encoding = 'utf-8'
    search_list = spider.get_pop_manga()
    return JsonResponse(search_list, safe=False)


def get_chapters(request):
    request.encoding = 'utf-8'
    if 'url' in request.GET and request.GET['url']:
        url = request.GET['url']
    else:
        url = ' '
    chapters = spider.get_manga_chapters(url)
    return JsonResponse(chapters, safe=False)


def get_chapters_img(request):
    request.encoding = 'utf-8'
    if 'url' in request.GET and request.GET['url']:
        url = request.GET['url']
    else:
        url = ' '
    chapters = spider.get_chapter_img(url)
    return JsonResponse(chapters, safe=False)


def get_trans_img(request):
    tans_img_list = []
    # 获取指定目录下的所有文件名

    # 基础路径+漫画名+章节数 = 图片路径
    img_path = os.path.join(settings.MANGA_TRANS_DIR, "tales", "453.6")
    files = os.listdir(img_path)
    # 输出所有文件名
    for file in files:
        tans_img_list.append(f"static/tales/453.6/{file}")
    return JsonResponse(tans_img_list, safe=False)
