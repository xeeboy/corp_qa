# Generated by Django 2.2.6 on 2019-12-03 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('part', models.CharField(blank=True, db_column='部门', max_length=10, null=True)),
                ('user_name', models.CharField(db_column='用户名', max_length=10, primary_key=True, serialize=False)),
                ('password', models.CharField(db_column='密码', default='123456', max_length=16)),
                ('email', models.CharField(blank=True, db_column='邮箱', max_length=50, null=True)),
                ('is_prev', models.IntegerField(blank=True, db_column='评审权限', null=True)),
            ],
            options={
                'db_table': '用户',
                'managed': False,
            },
        ),
    ]
