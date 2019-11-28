from django import forms
from .models import UnPass


class ParseUp(forms.ModelForm):
    class Meta:
        model = UnPass
        fields = ['result_ana', 'correct_act', 'pre_act',
                  'tech_idea', 'process_idea', 'qa_idea',
                  'serv_idea']
        labels = {
            'result_ana': '原因分析',
            'correct_act': '纠正措施',
            'pre_act': '预防措施',
            'tech_idea': '技术部意见',
            'process_idea': '工艺部意见',
            'qa_idea': '质量部意见',
            'serv_idea': '技术支持部意见',
        }
        widgets = {
            'result_ana': forms.Textarea(attrs={'rows': 3}),
            'correct_act': forms.Textarea(attrs={'rows': 3}),
            'pre_act': forms.Textarea(attrs={'rows': 3}),
            'tech_idea': forms.Textarea(attrs={'rows': 3}),
            'process_idea': forms.Textarea(attrs={'rows': 3}),
            'qa_idea': forms.Textarea(attrs={'rows': 3}),
            'serv_idea': forms.Textarea(attrs={'rows': 3}),
        }
