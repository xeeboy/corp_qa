from django import forms
from .models import AuditTopic, Entry


class TopicForm(forms.ModelForm):

    class Meta:
        model = AuditTopic
        fields = ['to_part', 'sugg_act', 'file', 'image']
        labels = {
            'to_part': '@责任部门',
            'sugg_act': '建议措施',
            'file': '相关文件',
            'image': '相关图片',
        }


class EntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        fields = ['act', 'file', 'image']
        labels = {
            'act': '已实施措施',
            'file': '相关文件上传',
            'image': '相关图片上传',
        }
