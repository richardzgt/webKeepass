#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/8/19 下午2:25
# @File : enhance.py
# @Author : richard zhu
# @purpose :
from dashboard.models import Item
import functools
import logging
import traceback
logger = logging.getLogger('webKeepass')

def auto_log(func):
    """
    auto write log decorator
    """
    @functools.wraps(func)
    def _deco(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(traceback.format_exc())
            logger.error(e)
            return False, e.__str__()
    return _deco

def get_object(model, **kwargs):
    if not kwargs:
        return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        return the_object[0]
    else:
        # 返回多个也不要了
        return None

def items_filter(user, **kwargs):
    """
    过滤user下的item，防止被其他人修改
    """
    items = Item.objects.select_related('group__user').filter(group__user=user)
    the_object = items.filter(**kwargs)
    return the_object
