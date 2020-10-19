#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/8/7 上午9:53
# @File : form.py
# @Author : richard zhu
# @purpose :

from django import forms
from dashboard.models import ItemGroup, Item, CustomKV


class GroupForm(forms.ModelForm):
    # name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = ItemGroup
        fields = ['name']
        exclude = ['user']

class ItemForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super(ItemForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['group'].queryset = ItemGroup.objects.filter(user=user)

    class Meta:
        model = Item

        fields = ['title', 'username', 'password', 'group', 'url', 'comment' ]

        widgets = {
            'url': forms.TextInput(attrs=({'placeholder':"http://xxxx"})),
            'comment': forms.Textarea(attrs=({'cols': 50, 'rows': 1}))
        }

class FieldsForm(forms.ModelForm):
    class Meta:
        model = CustomKV
        fields = '__all__'

