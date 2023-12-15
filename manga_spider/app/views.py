from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .models import Manga, Genres, Order
from . import spider_tool

spider = spider_tool.MangaHubSpider()


def index(request):
    return render(request, 'index.html')


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    order = request.GET.get('order', 'POPULAR')
    genre = request.GET.get('genre', 'all')
    query = request.GET.get('q', '')
    search_list = spider.search_manga(order, genre, query)
    return JsonResponse(search_list, safe=False)


def pop(request):
    request.encoding = 'utf-8'
    search_list = spider.get_pop_manga()
    return JsonResponse(search_list, safe=False)


def translatable(request):
    manga_list = Manga.objects.all()
    result = []
    for manga in manga_list:
        item = {'name': manga.trans_name,
                'detail_link': manga.detail_link,
                'img': manga.cover_img,
                'latest': manga.latest,
                'status': manga.status,
                'genres': manga.genres,
                }
        result.append(item)
    return JsonResponse(result, safe=False)


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


def classify(request):
    genres_list = Genres.objects.all()
    order_list = Order.objects.all()
    genres_result = []
    order_result = []
    for genre in genres_list:
        item = {
            'name': genre.name,
            'trans_name': genre.trans_name
        }
        genres_result.append(item)

    for order in order_list:
        item = {
            'name': order.name,
            'trans_name': order.trans_name
        }
        order_result.append(item)
    result = {
        'genres': genres_result,
        'orders': order_result
    }
    return JsonResponse(result, safe=False)


def exe_trans(request):
    return JsonResponse("")
