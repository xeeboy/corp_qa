# Generated by Django 2.2.6 on 2019-11-18 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audittopic',
            name='from_user',
            field=models.CharField(default='余西保', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='entry',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/entries/%Y%m%d'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/entries/%Y%m%d'),
        ),
    ]
