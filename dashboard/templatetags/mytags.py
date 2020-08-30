#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/8/4 下午3:57
# @File : mytags.py
# @Author : richard zhu
# @purpose : 自定义模板过滤器


from django import template
from dashboard.models import Item
from utils.enhance import auto_log
import logging

register = template.Library()
logger = logging.getLogger('webKeepass')

@register.filter(name='passwd2str')
@auto_log
def passwd2str(value):
    """
    密码解码
    """
    try:
        if value:
            return Item.decode_passwd(value)
    except Exception as e:
        logger.error(e)
    return


@register.filter(name='pwd2fake')
@auto_log
def pwd2fake(pwd):
    if pwd == None:
        return "None"
    else:
        return 6*"*"


@register.filter(name='items_cnt')
def items_cnt(item_group_id):
    return Item.objects.filter(group=item_group_id).count()

