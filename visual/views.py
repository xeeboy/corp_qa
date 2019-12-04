import pygal

from pandas import read_excel, read_sql_query, value_counts
from sqlalchemy import create_engine


def fpy_60_days(request):
    fp = r"\\192.168.40.2\质量部\12.质量部数据\PVC质量数据\2019年PVC质量数据\2019年PVC质量数据.xlsx"
    fpy_frame = _excel_data(fp)
    fpy = fpy_frame.values.round(4) * 100  # *100 is for formatting as %.2f%%
    X = list(map(lambda x: str(format(x, '%Y-%m-%d')), fpy_frame.index))
    line = pygal.Line(x_label_rotation=10, show_minor_x_labels=False)
    line.title = '近60日PVC制程FPY'
    line.x_labels = X
    line.x_labels_major = [X[0], X[-1]]
    line.add('合格率', fpy)
    line.value_formatter = lambda x: '%.2f%%' % x if x is not None else '0'
    return line.render_django_response()


def _excel_data(fp):
    """use pandas get data_frame or series"""
    frame = read_excel(fp, usecols=[3, 4, 7],
                       names=['pro_qty', 'pass_qty', '生产日期'])
    frame['生产日期'].ffill(inplace=True)
    frame.fillna(0, inplace=True)
    frame = frame[frame['pro_qty'] != 0]
    grouped = frame.groupby('生产日期').apply(
        lambda x: sum(x.pass_qty)/sum(x.pro_qty))
    lasted = grouped.tail(60)
    return lasted


def up_keys(request):
    h_bar = pygal.HorizontalBar()
    h_bar.title = '近100笔不良关键词前15统计'
    for k, v in _mysql_data().tail(15).items():
        h_bar.add(k, v)
    return h_bar.render_django_response()


def _mysql_data():
    engine = create_engine('mysql+mysqlconnector://root:123456@{}:{}/{}'
                           ''.format('192.168.50.145', 3306, 'qadb'))
    sql = "SELECT 不良关键词 FROM 不合格品登记 where 不良品种类='制程不合格' order by 生产日期"
    frame = read_sql_query(sql, engine)
    series = frame['不良关键词'].dropna().tail(100)
    unpass_kws_str = ','.join([i for i in series if len(i) > 1])
    return value_counts(unpass_kws_str.split(','))
