from django.db import models


# Create your models here.
class User(models.Model):
    part = models.CharField(db_column='部门', max_length=10, blank=True, null=True)
    user_name = models.CharField(db_column='用户名', primary_key=True, max_length=10)
    password = models.CharField(db_column='密码', max_length=16, default='123456')
    email = models.CharField(db_column='邮箱', max_length=50, blank=True, null=True)
    is_prev = models.IntegerField(db_column='评审权限', blank=True, null=True)

    class Meta:
        managed = False
        db_table = '用户'
