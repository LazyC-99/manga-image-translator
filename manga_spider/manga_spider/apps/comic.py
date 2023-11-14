from django.http import HttpResponse, JsonResponse
import json

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
