# -*- coding: utf-8 -*-
from requests import get
from lxml import etree
from random import choice

from .models import JokeUrls

user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36')
headers = {'User-Agent': user_agent}


def get_joke_urls(domain):
    try:
        r = get(domain, headers=headers)
        ele = etree.HTML(r.text)
        root = ele.xpath('//div[@class="mx2"]')
        urls = root[0].xpath('.//@href')
        return urls
    except ConnectionError:
        pass


def choice_one_url(urls, user, max_times=180):
    """
    try `max_times` to choice a url from `urls`, the url must never been processed ever,
    if urls have all been processed, finally choice any one.
    """
    qry_sets = JokeUrls.objects.filter(user=user)
    processed_urls = {qry_set.url for qry_set in qry_sets}
    n = 0
    while n < max_times:
        _url = choice(urls)
        if _url not in processed_urls:  # select one never getted
            return _url
        else:
            n += 1
    return choice(urls)  # if all processed, choice one


def parse_joke(_url):
    joke_str = None
    try:
        r = get(_url, headers=headers)
        ele = etree.HTML(r.text)
        root = ele.xpath('//div[@class="content"]/node()')
        lines = [line for line in root if isinstance(line, str)]
        joke_str = '\n'.join(['Dears:工作辛苦,来点笑话轻松一下吧：'] + lines[1:])
    except ConnectionError:
        pass
    finally:
        return joke_str


def gen_joke(from_url, user):
    urls = get_joke_urls(from_url)
    if urls:
        rand_url = choice_one_url(urls, user)
        joke_str = parse_joke(rand_url)
        if joke_str:
            jkurls = JokeUrls()
            jkurls.user = user
            jkurls.url = rand_url
            jkurls.save()
            return joke_str

