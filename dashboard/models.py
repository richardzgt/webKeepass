#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/7/27 10:21
# @File : models.py
# @Author : richard zhu
# @purpose :

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.pycrypt import PyCrypt
from django.shortcuts import reverse
import logging

logger = logging.getLogger(__name__)


class ItemGroup(models.Model):
    name = models.CharField(max_length=64, verbose_name="组名", unique=True)
    user = models.ForeignKey(User,
                             related_name='+',
                             on_delete=models.CASCADE)
    icon = models.CharField(max_length=64, verbose_name="图标编号", blank=True, null=True)

    def __str__(self):
        return "[%s] <%s>" % (self.name, self.user.username)

    def get_absolute_url(self):
        return reverse('dashboard:group')

    class Meta:
        verbose_name = "密码组"
        verbose_name_plural = "密码组"

class Item(models.Model):
    title = models.CharField(max_length=64, verbose_name=_("密码条目名"))
    username = models.CharField(max_length=64, verbose_name=_("密码用户名"))
    password = models.CharField(max_length=128, verbose_name=_("密码"), blank=True, null=True)
    group = models.ForeignKey(ItemGroup,
                              on_delete=models.CASCADE,
                              verbose_name="关联密码组",
                              related_name='+')
    url = models.URLField(verbose_name="url地址", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,
                                      null=True,
                                      verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True,
                                      null=True,
                                      verbose_name="更新时间")

    comment = models.TextField(max_length=512, verbose_name="备注", blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save(force_insert=force_insert,
                     force_update=force_update,
                     using=using, update_fields=update_fields)
        self.password = PyCrypt().encrypt(self.password)
        super(Item, self).save()

    @property
    def str_passwd(self):
        return PyCrypt().decrypt(self.password)

    @staticmethod
    def decode_passwd(value):
        return PyCrypt().decrypt(value)

    @staticmethod
    def encode_passwd(value):
        return PyCrypt().encrypt(value)

    def __str__(self):
        return "[%s] <%s> %s" % (self.group.name, self.title, self.username)

    class Meta:
        verbose_name = "密码条目"
        verbose_name_plural = "密码条目"
        ordering = ['group']


class CustomKV(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name="关联条目")
    key = models.CharField(max_length=64, verbose_name="key")
    value = models.CharField(max_length=64, verbose_name="value")

    def __str__(self):
        return "[%s] <%s>" % (self.key, self.value)

    class Meta:
        verbose_name = "自定义字段"
        verbose_name_plural = "自定义字段"


class Log(models.Model):
    log_level_choices = (
        (0, 'DEBUG'),
        (1, 'INFO'),
        (2, 'WARNING'),
        (3, 'ERROR'),
        (4, 'CRITICAL'),
    )

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="日志产生用户")
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING, verbose_name="密码项")
    log_level = models.IntegerField(choices=log_level_choices, default=0, verbose_name="操作")
    content = models.TextField(blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="记录时间")

    def __str__(self):
        return "%s [%s] <%s> [%s]" % (self.user.username, self.item.title, self.log_level, self.create_at)

    class Meta:
        verbose_name = "日志"
        verbose_name_plural = "日志"
        ordering = ['-create_at']
