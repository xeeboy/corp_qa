# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class UnPass(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    up_type = models.CharField(db_column='不良品种类', max_length=10)
    customer = models.CharField(db_column='客户', max_length=30)
    up_name = models.CharField(db_column='不良品名称', max_length=30)
    batch = models.CharField(db_column='批号', max_length=20)
    pro_date = models.DateField(db_column='生产日期')
    pro_qty = models.FloatField(db_column='数量Kg')  # Field name made lowercase.
    up_desc = models.TextField(db_column='不合格描述')
    result_ana = models.TextField(db_column='原因分析')
    correct_act = models.TextField(db_column='纠正措施')
    pre_act = models.TextField(db_column='预防措施')
    tech_idea = models.TextField(db_column='技术部意见')
    process_idea = models.TextField(db_column='工艺部意见')
    qa_idea = models.TextField(db_column='质量部意见')
    serv_idea = models.TextField(db_column='技术支持部意见')

    class Meta:
        managed = False
        db_table = '不合格品登记'


class UpStatus(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)
    caseto_by_qa = models.CharField(db_column='caseto_by_QA', max_length=10)
    case_closed_flag = models.IntegerField(db_column='case_closed_flag')

    class Meta:
        managed = False
        db_table = '状态标记'


class ProInfo(models.Model):
    batch = models.CharField(db_column='批号', primary_key=True, max_length=30)
    customer = models.CharField(db_column='客户', max_length=30)
    pro_type = models.CharField(db_column='产品型号', max_length=30)
    pro_color = models.CharField(db_column='颜色', max_length=10)
    pro_date = models.DateField(db_column='生产日期')
    test_date = models.DateField(db_column='检验日期')

    class Meta:
        managed = False
        db_table = '产品信息'


class Performance(models.Model):
    batch = models.CharField(db_column='批号', max_length=30)
    extruder_skin = models.IntegerField(db_column='表面判定')
    perf = models.CharField(db_column='性能判定', max_length=4)
    rosh = models.IntegerField(db_column='RoSH')
    density = models.FloatField(db_column='密度')
    lsqd = models.FloatField(db_column='拉伸强度')
    dlscl = models.FloatField(db_column='断裂伸长率')
    dcwd = models.IntegerField(db_column='低冲温度')
    dlgs = models.IntegerField(db_column='断裂根数')
    tjdzlwd = models.IntegerField(db_column='体积电阻率温度')
    tjdzl = models.BigIntegerField(db_column='体积电阻率')
    ydbz = models.CharField(db_column='硬度标准', max_length=2)
    yd = models.FloatField(db_column='硬度')
    time200c = models.IntegerField(db_column='200℃热稳定时间')
    jdqd = models.IntegerField(db_column='介电强度')
    yzs = models.FloatField(db_column='氧指数')
    rrzs = models.FloatField(db_column='熔融指数')
    kssfcd = models.FloatField(db_column='快速水分测定')
    rbxwd = models.CharField(db_column='热变形温度', max_length=3)
    rbx = models.FloatField(db_column='热变形')

    class Meta:
        managed = False
        db_table = '常规性能'


class Parts(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    part = models.CharField(db_column='部门', max_length=10)

    class Meta:
        managed = False
        db_table = '部门'
        unique_together = (('id', 'part'),)


class JokeUrls(models.Model):
    user = models.CharField(max_length=32)
    url = models.CharField(max_length=150)

