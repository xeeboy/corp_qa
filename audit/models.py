from django.db import models
from dw_query.models import UnPass


class AuditTopic(models.Model):
    unpass = models.ForeignKey(to=UnPass, to_field='id', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    from_user = models.CharField(max_length=10)
    to_part = models.CharField(max_length=10)
    sugg_act = models.TextField()
    file = models.FileField(upload_to='files/topics/%Y%m%d', null=True, blank=True)
    image = models.ImageField(upload_to='images/topics/%Y%m%d', null=True, blank=True)

    def __str__(self):
        return self.sugg_act


class Entry(models.Model):
    topic = models.ForeignKey(AuditTopic, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    from_part = models.CharField(max_length=10)
    act = models.TextField()
    file = models.FileField(upload_to='files/entries/%Y%m%d', null=True, blank=True)
    image = models.ImageField(upload_to='images/entries/%Y%m%d', null=True, blank=True)

    def __str__(self):
        return self.act



