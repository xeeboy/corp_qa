from urllib.parse import urljoin

from django.views.decorators.csrf import csrf_exempt

from . import BizWxUtil, jokes
from . import models, serial
from audit.models import AuditTopic

from django.db import connection
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    upstatus = models.UpStatus.objects.filter(
        caseto_by_qa__isnull=False).order_by('-id')[:3]
    ids = [upstatu.id for upstatu in upstatus]
    ups = models.UnPass.objects.filter(id__in=ids)

    topics = AuditTopic.objects.all().order_by('-date_added')[:3]
    ids = [topic.unpass_id for topic in topics]
    ups_topics = models.UnPass.objects.filter(id__in=ids)

    context = {'upstatus': upstatus, 'ups': ups, 'topics': topics, 'ups_topics': ups_topics}
    return render(request, 'dw_query/index.html', context=context)


@login_required
def all_suggestion(request):
    up_id = request.GET.get('up_id', '')
    to_part = request.GET.get('to_part', '')
    customer = request.GET.get('customer', '')
    proname = request.GET.get('proname', '')
    uptype = request.GET.get('uptype', '')

    to_part = '' if to_part == '--select--' else to_part
    uptype = '' if uptype == '全部类型' or uptype is None else uptype

    if any([up_id, to_part]):
        topics = AuditTopic.objects.filter(
            to_part__contains=to_part).order_by('-date_added')
        if up_id:
            topics = topics.filter(
                unpass_id=up_id).order_by('-id')
        ids = [topic.unpass_id for topic in topics]
        ups = models.UnPass.objects.filter(id__in=ids)
        params = ['{}={}'.format(k, v) for k, v in
                  {'up_id': up_id,
                   'to_part': request.GET.get('to_part', '')
                   }.items()]
    else:
        ups = models.UnPass.objects.filter(
            up_type__contains=uptype).filter(
            customer__contains=customer).filter(
            up_name__contains=proname)
        ids = [up.id for up in ups]
        topics = AuditTopic.objects.filter(
            unpass_id__in=ids).order_by('-date_added')
        params = ['{}={}'.format(k, v) for k, v in
                  {'customer': customer,
                   'proname': proname,
                   'uptype': request.GET.get('uptype', '')
                   }.items()]

    paginator = Paginator(topics, 4)
    page = request.GET.get('page')
    topics_pgd = paginator.get_page(page)

    parts = (part.part for part in models.Parts.objects.all())
    context = {'parts': parts, 'topics': topics_pgd, 'ups_topics': ups, 'params': params}
    return render(request, 'dw_query/all_suggestion.html', context=context)


@login_required
def all_unpass(request):
    customer = request.GET.get('customer', '')
    proname = request.GET.get('proname', '')
    uptype = request.GET.get('uptype', '')
    uptype = '' if uptype == '全部类型' else uptype

    params = ['{}={}'.format(k, v) for k, v in
              {'customer': customer, 'proname': proname,
               'uptype': request.GET.get('uptype', '')}.items()]

    ups = models.UnPass.objects.filter(
        up_type__contains=uptype).filter(
        customer__contains=customer).filter(
        up_name__contains=proname)
    ids = [up.id for up in ups]
    upstatus = models.UpStatus.objects.filter(id__in=ids).order_by('-id')

    paginator = Paginator(upstatus, 4)
    page = request.GET.get('page')
    upstatus_pgd = paginator.get_page(page)

    context = {'upstatus': upstatus_pgd, 'ups': ups, 'params': params}
    return render(request, 'dw_query/all_unpass.html', context=context)


@login_required
def unpass(request, batch):
    uplist = models.UnPass.objects.filter(batch__contains=batch)
    cols = ['ID', '类型', '客户', '产品名称', '批号', '生产日期', '数量KG', '不合格原因']
    serializer = serial.DwQuerySerializer(uplist, many=True)
    data = [dic.values() for dic in serializer.data]  # serializer.data is a list comps of OrderDict
    context = {'serializer': data, 'cols': cols}
    return render(request, 'dw_query/showtbl.html', context=context)


@login_required
def performance(request, keyword):
    pro_info = ('客户', '产品型号', '颜色', '生产日期')
    test_items = (
        '批号', '表面判定', 'RoSH', '性能判定', '密度', '拉伸强度', '断裂伸长率', '低冲温度',
        '断裂根数', '体积电阻率温度', '体积电阻率', '硬度标准', '硬度', '200℃热稳定时间',
        '介电强度', '氧指数', '熔融指数', '快速水分测定', '热变形温度', '热变形')
    cursor = connection.cursor()
    sql = "SELECT {0},a.批号,IF(表面判定=TRUE,'PASS',IF(表面判定 IS NULL,NULL,'UNPASS'))," \
          "IF(RoSH=TRUE,'PASS',IF(RoSH IS NULL,NULL,'UNPASS'))," \
          "{1} FROM 产品信息 a INNER JOIN 常规性能 b ON a.批号=b.批号 " \
          "WHERE CONCAT(客户,产品型号,颜色,b.批号) like '%{2}%' order by 生产日期 DESC" \
          "".format(','.join(pro_info),
                    ','.join(test_items[3:]), keyword)
    cursor.execute(sql)
    results = cursor.fetchall()
    serializer = []
    for line in results:
        new_line = []
        for v in line:
            if isinstance(v, int) and len(str(v)) > 5:
                v = '%.2e' % v
            new_line.append('/' if v is None else str(v))
        serializer.append(new_line)
    context = {'serializer': serializer, 'cols': pro_info + test_items}
    return render(request, 'dw_query/showtbl.html', context=context)


@login_required
def home_search(request):
    keyword = request.GET.get('keyword')
    if keyword.lower().startswith('up') and len(keyword) > 2:
        return HttpResponseRedirect(reverse('dw_query:unpass', args=[keyword[2:]]))
    elif keyword.lower().startswith('p') and len(keyword) > 1:
        return HttpResponseRedirect(reverse('dw_query:performance', args=[keyword[1:]]))
    else:
        return render(request, 'dw_query/key_error.html')


@csrf_exempt
def chat_reply(request):
    if 'echostr' in request.GET:  # 响应微信验证url
        return BizWxUtil.responseEcho(request)
    if request.method == 'POST':
        message = BizWxUtil.parseMessage(request)
        keyword = message.get('Content', '').lower()
        resp_dict = {'to_user': message['FromUserName'],
                     'from_user': message['ToUserName'],
                     'type': 'text'}
        content = ''
        if message.get('EventKey') == 'how_query':
            content = '''(1) p + “<客户名>或<产品名>或<批号>”: 获取检测数据查询网址；\n(2) up + “<批号>”: 获取该批次不良信息；\nTips：如果微信浏览器不能打开，请选择其它浏览器打开！'''
        elif message.get('EventKey') == 'get_joke':
            url = r'http://xiaodiaodaya.cn/wapindex.aspx?classid=602'
            content = jokes.gen_joke(url, user=resp_dict['to_user'])
        elif keyword:
            if any([keyword.startswith('p') and len(keyword) > 1,
                    keyword.startswith('up') and len(keyword) > 2]):
                query_url = 'http://%s/search?keyword=' % request.META['HTTP_HOST']
                query_url = urljoin(query_url, keyword)
                pic_url = urljoin('http://%s' % request.META['HTTP_HOST'],
                                  'static/dw_query/query_pic.jpg')
                resp_dict['type'] = 'news'
                resp_dict['data'] = [
                    {'title': '您正在查询检测数据 + 关键字<%s>' % keyword[1:] if keyword.startswith('p') else '您正在查询不良品记录 + 关键字<%s>' % keyword[2:],
                     'description': '请点击进入网页查看结果！',
                     'pic_url': pic_url,
                     'url': query_url},
                ]
        else:
            pass
        resp_dict['content'] = content
        return BizWxUtil.parseResponse(resp_dict)
