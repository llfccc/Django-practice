#coding=utf-8
from django.shortcuts import render
from .models import SupplierList,OptionalSupplierList
import json, datetime
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.db.models import Q,Count
from .forms import SupplierListForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from echarts import Echart, Legend, Bar, Axis
from django.http import Http404,JsonResponse
# Create your views here.


@login_required
def querySupplier(request):
    if request.user.has_perm('supplierList.query_supplier'):
        if 'searchText' in request.POST:
            searchText = request.POST['searchText']
            data=SupplierList.objects.filter(Q(supplier_name__icontains=searchText)|Q(material_name__icontains=searchText)).order_by('-id')
        else:
            data=SupplierList.objects.order_by('-id')
        return render(request,'querySupplier.html',locals())
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')


#dumps方法转换数据为json的时候，如果格式化的数据中有datetime类型的数据时会报错
class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


@login_required
def info(request,id):
    if request.user.has_perm('supplierList.query_supplier'):
        supplierInfo=model_to_dict(SupplierList.objects.get(id=id));
        supplierInfo=json.dumps(supplierInfo, ensure_ascii=False, cls=CJsonEncoder)
        return HttpResponse(supplierInfo)
    else:
        raise Http404

@login_required
def  addNewSupplier(request):
    if request.user.has_perm('supplierList.query_supplier'):
        k=SupplierList(supplier_name='新增')
        k.save()
        return HttpResponse('ok', content_type="text/html", status=200)
    else:
        raise Http404

@login_required
def updateAll(request):
    if request.user.has_perm('supplierList.update_all_supplier'):
        if request.method == 'POST':
            received_data = json.loads(request.body)

            received_data['id']=received_data['supplier_id']
            del received_data['supplier_id']
            #删除值为空的字典
            received_data=dict(filter(lambda x: x[1] != '', received_data.items()))
            k = SupplierList(**received_data)
            k.save()
            return JsonResponse({"result":"ok"})
        else:
            raise Http404
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')

#显示供应商证件情况
@login_required
def showDocument(request):
    if request.user.has_perm('supplierList.show_document'):
        if request.method == 'POST':
            archive_class=request.POST['archive_class']
            data=SupplierList.objects.filter(archive_class=archive_class).all()

        else:
            pass
        return render(request,'showDocument.html',locals())
        #raise Http404
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')




@login_required
def  queryOptionalSupplier(request):
    if request.user.has_perm('supplierList.query_optional_supplier'):
        if 'searchText' in request.POST:
            searchText = request.POST['searchText']
            data=OptionalSupplierList.objects.filter(Q(supplier_name__icontains=searchText)|Q(material_name__icontains=searchText)).order_by('-id')
        else:
            data=OptionalSupplierList.objects.order_by('-id')
        return render(request,'queryOptionalSupplier.html',locals())
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')

@login_required
def  addNewOptionalSupplier(request):
    if request.user.has_perm('supplierList.add_new_optional_supplier'):
        k=OptionalSupplierList(supplier_name='新增')
        k.save()
        return JsonResponse({"result":"ok"})
    else:
        raise Http404
@login_required
def  infoOptional(request,id):
    if request.user.has_perm('supplierList.query_optional_supplier'):
        supplierInfo=model_to_dict(OptionalSupplierList.objects.get(id=id));
        supplierInfo=json.dumps(supplierInfo, ensure_ascii=False, cls=CJsonEncoder)
        return HttpResponse(supplierInfo)
    else:
        raise Http404

@login_required
def  updateAllOptional(request):
    if request.user.has_perm('supplierList.update_all_optional_supplier'):
        if request.method == 'POST':

            received_data = json.loads(request.body)
            received_data['id']=received_data['supplier_id']
            del received_data['supplier_id']
            #删除值为空的字典
            received_data=dict(filter(lambda x: x[1] != '', received_data.items()))
            k = OptionalSupplierList(**received_data)
            k.save()
            return JsonResponse({"result":"ok"})
        else:
            raise Http404
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')

@login_required
def dataStatistics(request):
    supplierNumber=SupplierList.objects.values('supplier_class').annotate(dcount=Count('supplier_class')).order_by('-dcount')
    supplier_count=list(supplierNumber.values_list('dcount'))
    supplier_count=[x[0] for x in supplier_count]
    supplier_class=list(supplierNumber.values_list('supplier_class'))
    supplier_class=[x[0] for x in supplier_class]
    chart = Echart('评审供应商数量', 'TaTaTa')
    chart.use(Bar('China',supplier_count))
    chart.use(Legend(['GDP']))
    chart.use(Axis('category', 'bottom', data=supplier_class))


    supplierNumber=SupplierList.objects.values('position_abbr').annotate(dcount=Count('position_abbr')).order_by('-dcount')
    abbr_count=list(supplierNumber.values_list('dcount'))
    abbr_count=[x[0] for x in abbr_count][:10]
    position_abbr=list(supplierNumber.values_list('position_abbr'))
    position_abbr=[x[0] for x in position_abbr][:10]


    chart2 = Echart('供应商分布', 'TaTaTa')
    chart2.use(Bar('China',abbr_count))
    chart2.use(Legend(['GDP']))
    chart2.use(Axis('category', 'bottom', data=position_abbr))

    return render(request, 'dataStatistics.html', locals())
