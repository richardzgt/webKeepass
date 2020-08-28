#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/8/4 下午3:57
# @File : mytags.py
# @Author : richard zhu
# @purpose : 自定义模板过滤器


from django import template
from dashboard.models import Item
register = template.Library()

@register.filter(name='passwd2str')
def passwd2str(value):
    """
    密码解码
    """
    if value:
        return Item.decode_passwd(value)
    return


@register.filter(name='pwd2fake')
def pwd2fake(pwd):
    if pwd:
        if len(pwd)>0:
            return 6*"*"
    return


@register.filter(name='items_cnt')
def items_cnt(item_group_id):
    return Item.objects.filter(group=item_group_id).count()

