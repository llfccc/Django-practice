# coding=utf-8
from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render
import sys,json
sys.path.append("..")
from supplierList.models import SupplierList
from .models import KeyEvent
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required, permission_required
#生成pdf
from reportlab.pdfgen import canvas
from django.http import HttpResponse

#@login_required
# 显示未经编码的内容

@login_required
def showAllKeyEvents(request):
    chinese_name = request.user.profile.chinese_name
    b = KeyEvent.objects.order_by('-id')[:10]

    return render(request, 'showAllKeyEnvet.html', locals())
@login_required
def edit(request,id):
    data=KeyEvent.objects.filter(id=id)[0]
    return render(request, 'edit.html', locals())

@login_required

def insert(request):
    #if request.user.has_perm('supplierList.query_supplier'):
    data=SupplierList.objects.values("supplier_name").filter(supplier_name__isnull=False).annotate(sid=Count("supplier_name")).order_by("-id")
    data=json.dumps(list(data))
    #data=list(data)

    return render(request, 'insert.html', locals())

@login_required
def insertHandle(request):
        if request.user.has_perm('supplierList.update_all_supplier'):
            if request.method == 'POST':
             
                received_data = dict(request.POST)
                del received_data['submit']
                # #删除值为空的字典
                def changeListToString(data):
                    result={}
                    for i,j in data.items():
                        if j[0]:
                            print(i,j)
                            result[i]=j[0];
                    return result
                    
                received_data=changeListToString (received_data)
                print (received_data)
                

                # keys = list(received_data.keys())
                # received_data2={}
                # for key in keys:
                #     if  received_data[key][0]:
                #         received_data2[key]=received_data[key][0]
    
                print(received_data)
                k = KeyEvent(**received_data)     
                k.save()

                return HttpResponseRedirect('/keyEvent/showAllKeyEvents/')
            else:
                raise Http404
        else:
            messages.success(request, '你没有权限访问这个页面')
            return render(request, 'noPremission.html')

    




@login_required
def printKey(request,id):
    data=KeyEvent.objects.filter(id=id)[0]
    print(data.supplier_class)
    

    return render(request, 'printKey.html', locals())
