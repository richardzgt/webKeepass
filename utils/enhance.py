#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/8/19 下午2:25
# @File : enhance.py
# @Author : richard zhu
# @purpose :
from dashboard.models import Item
from portal.models import SysLog
from django.conf import settings
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

def try_login(func):
    def _deco_(request, *args, **kwargs):
        logger.info("---------------")
        return func(request, *args, **kwargs)
    return _deco_



class RecordSysLog(object):
    def __init__(self, request, action, attr):
        """

        """
        self.request = request
        self.action = action
        self.attr = attr

    @property
    def ip(self):
        return self.request.META.get("HTTP_X_FORWARD_FOR", self.request.META['REMOTE_ADDR'])

    @property
    def username(self):
        return self.request.user.username

    @auto_log
    def record_syslog(self, message):
        try:
            SysLog.objects.create(user=self.username,
                                  ip=self.ip,
                                  action=self.action,
                                  attr=self.attr,
                                  message=message
                                  )
        except Exception as e:
            return False
        return True

class ValidTryLogin(RecordSysLog):
    def __init__(self, request):
        super(ValidTryLogin, self).__init__(request, "create", "Login")

    def record_login_failed(self):
        return self.record_syslog("failed")

    def record_login_success(self):
        return self.record_syslog("success")

    @property
    def login_valid(self):
        failed_cnt = SysLog.objects.filter(ip=self.ip,
                              action="create",
                              attr="Login",
                              message="failed",
                              created_at__minute__lte=settings.TRY_LOGIN_FAILED_INTERVAL).count()
        if failed_cnt > settings.TRY_TIME:
            return False
        return True
