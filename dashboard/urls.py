#!/usr/bin/env python
# set coding: utf-8
# @Time : 2020/7/24 15:09
# @File : urls.py
# @Author : richard zhu
# @purpose :

from django.urls import path, include, re_path
from dashboard.views import (GroupListView,
                             GroupDelete,
                             GroupUpdate,
                             ItemList,
                             ItemView,
                             FieldsView)
app_name="dashboard"
urlpatterns = [
    path("", GroupListView.as_view(), name='group'),
    path("group/", GroupListView.as_view(), name='group'),
    path("group/<int:pk>/update", GroupUpdate.as_view(), name='group-update'),
    path("group/<int:pk>/delete", GroupDelete.as_view(), name='group-delete'),
    path("item/list/", ItemList.as_view(), name='item-list'),  # item列表
    path("item/", ItemView.as_view(), name='item'), # item的crud
    path("fields/", FieldsView.as_view(), name='fields')

]


