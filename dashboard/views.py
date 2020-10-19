from django.shortcuts import get_object_or_404, reverse, render, redirect, HttpResponse, HttpResponseRedirect
from django.views.generic import View, ListView, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from dashboard.models import Item, ItemGroup, CustomKV
from dashboard.form import GroupForm, ItemForm, FieldsForm
from utils.enhance import get_object, items_filter, RecordSysLog, auto_log
from portal.views import DefaultMixin
import logging
import json

logger = logging.getLogger("webKeepass")

class GroupListView(DefaultMixin, ListView):
    """
    对整个资源列表的 查get 增post
    """
    template_name = 'groupList.html'
    # model = ItemGroup
    def get_queryset(self):
        return ItemGroup.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = 1
        context['form'] = GroupForm()
        return context

    def post(self, request):
        name = request.POST.get("name")
        try:
            ItemGroup.objects.create(name=name.strip(),
                                     user=request.user,
                                     )
            RecordSysLog(request, "create", "ItemGroup").record_syslog("%s" % name)
            return HttpResponseRedirect(reverse('dashboard:group'))
        except Exception as e:
            logger.error(e)
            return HttpResponse(e, status=400)



class GroupUpdate(DefaultMixin, UpdateView):
    model = ItemGroup
    form_class = GroupForm
    def get(self, request, pk):
        group = get_object_or_404(ItemGroup, id=pk)
        return HttpResponse(group)

    def post(self, request, pk):
        group = get_object_or_404(ItemGroup, id=pk)
        try:
            for key, value in request.POST.items():
                old_value = getattr(group, key)
                if old_value != value:
                    setattr(group, key, value)
                    RecordSysLog(request, "update", "ItemGroup").record_syslog("<%s> [%s]: %s -> %s" % (group.name, key, old_value, value))
            group.save()
            return HttpResponse(status=202)
        except Exception as e:
            return HttpResponse(e ,status=500)

class GroupDelete(DefaultMixin, DeleteView):
    """
    对资源对象的查get 改POST 删delete
    """
    def delete(self, request, pk):
        try:
            group = ItemGroup.objects.filter(user=request.user).filter(pk=pk)
            group.delete()
            RecordSysLog(request, "delete", "ItemGroup").record_syslog("<%s>" % (group.name))
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(json.dumps({'msg':e}), status=400)

class ItemList(DefaultMixin, ListView):
    template_name = "itemList.html"

    def get_queryset(self):
        gid = self.request.GET.get("gid")
        items = items_filter(self.request.user)
        if gid:
            items = items.filter(group=gid)
        return items

class ItemView(DefaultMixin, View):
    def get(self, request):
        id = request.GET.get("id")
        if id:
            item = items_filter(request.user, id=id)[0]
            itemf = ItemForm(user=request.user, instance=item)
            return render(request, 'itemUpdate.html', locals())
        else:
            itemf = ItemForm(user=request.user)
            return render(request, 'itemCreate.html', locals())

    def post(self, request):
        error_msg = ""
        try:
            itf = ItemForm(request.POST, user=request.user)
            if itf.is_valid():
                # 根据请求参数id查询模型数据是否存在
                id = request.GET.get('id')
                result = items_filter(request.user, id=id)
                # 不存在则新增数据
                if not result:
                    itf.save()
                    # logger.error(itf.fields.title)
                    RecordSysLog(request, "create", "Item").record_syslog("<{title}> 用户名[{username}] 密码[{password}] ".format(**itf.cleaned_data))
                    return HttpResponseRedirect(reverse("dashboard:item-list"))
                # 存在则修改数据
                else:
                    item_obj = result[0]
                    d = itf.cleaned_data
                    for key, value in d.items():
                        old_value = getattr(item_obj, key)
                        if key == 'password' and Item.decode_passwd(old_value) == value:
                            continue
                        if old_value != value :
                            setattr(item_obj, key, value)
                            RecordSysLog(request, "update", "Item").record_syslog("<%s> [%s]: %s -> %s" % (d['title'], key, Item.decode_passwd(old_value), value))
                    item_obj.save()
                    return HttpResponseRedirect(reverse("dashboard:item-list")+ "?gid=%s" % item_obj.group_id)
            else:
                error_msg = itf.errors.as_json()
        except Exception as e:
            logger.error(e)
            error_msg += str(e)

        return HttpResponse("操作失败:{}".format(error_msg), status=500)

    def delete(self, request):
        try:
            id = request.GET.get("id")
            item = items_filter(request.user, id=id)
            item.delete()
            RecordSysLog(request, "delete", "Item").record_syslog("<%s>" % (item.title))
            return HttpResponse(status=200)
        except Exception as e:
            return HttpResponse(str(e), status=400)

class FieldsView(DefaultMixin, View):
    def get(self, request):
        item_id = request.GET.get("item_id")
        if item_id:
            item = items_filter(request.user, id=item_id)[0]
            fields = CustomKV.objects.filter(item=item)
            return render(request, 'fields.html', locals())

    def post(self, request):
        error_msg = ""
        try:
            item_id = request.GET.get("item_id")
            key = request.POST.getlist('key')
            value = request.POST.getlist('value')
            fields_list = [ {key:value} for key, value in zip(key, value) ]
            item = items_filter(request.user, id=item_id)[0]
            CustomKV.objects.filter(item=item).delete() # 全部删除

            for each_field in fields_list:
                for key, value in each_field.items():
                    if all((key, value)):
                        CustomKV.objects.create(item=item, key=key, value=value)

            return HttpResponseRedirect(reverse('dashboard:fields')+'?item_id={}'.format(item.id))

        except Exception as e:
            logger.error(e)
            error_msg += str(e)
            return JsonResponse({'msg':error_msg}, status=500)
