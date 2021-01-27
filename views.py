from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
import json
from django.views import View
# Create your views here.
from django.conf import settings
import datetime
import operator
import itertools
import datetime
import time

def write_json(data, filename='news.json'):
    with open(filename, 'w') as f:
        json.dump(data, f)


def index(request):
    return render(request, 'news_feed.html')

def news(request, link=0):
    with open(settings.NEWS_JSON_PATH, 'r') as news_json_file:
        news_feed = json.load(news_json_file)
        news_dict = {}
        if request.GET.get('q') is None:
            for news_item in news_feed:
                news_date = news_item['created'].split()
                news_dict.setdefault(news_date[0], []).append(news_item)
                if news_item['link'] == link:
                    return render(request, 'news_item.html', news_item)
            return render(request, 'news_feed.html', {'news_feed': {k: news_dict[k] for k in sorted(news_dict, reverse=True)}})

        else:
            search_news_term = str(request.GET.get('q')).lower()
            for news_item in news_feed:
                news_title = news_item['title'].split()
                news_title = [x.lower() for x in news_title]
                news_date = news_item['created'].split()
                if search_news_term in news_title:
                    news_dict.setdefault(news_date[0], []).append(news_item)
            return render(request, 'news_feed.html', {'news_feed': {k: news_dict[k] for k in sorted(news_dict, reverse=True)}})


def createnews(request):
    if request.method == "GET":
        return render(request, 'news_create.html')
    elif request.method == "POST":
        with open(settings.NEWS_JSON_PATH, 'r+') as news_json_file:
            news_feed = json.load(news_json_file)
            new_news_title = request.POST.get('title')
            new_news_text = request.POST.get('text')
            new_news_timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            max_link = [int(news_item["link"]) for news_item in news_feed]
            new_news_link = max(max_link) + 1
            new_json_data = {"created": str(new_news_timestamp),
                             "text": str(new_news_text),
                             "title": str(new_news_title),
                             "link": str(new_news_link)}
            news_feed.append(new_json_data)
            write_json(news_feed)
            return redirect('/news/')
