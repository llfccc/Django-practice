# coding=utf-8
from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render
import sys,json
# sys.path.append("..")
# from supplierList.models import SupplierList
# from .models import KeyEvent
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required, permission_required
#生成pdf

from django.http import HttpResponse

#@login_required
# # 显示未经编码的内容

# @login_required
# def showAllKeyEvents(request):
#     chinese_name = request.user.profile.chinese_name
#     b = KeyEvent.objects.order_by('-id')[:10]

#     return render(request, 'showAllKeyEnvet.html', locals())
# @login_required
# def edit(request,id):
#     data=KeyEvent.objects.filter(id=id)[0]
#     return render(request, 'edit.html', locals())

# @login_required

# def insert(request):
#     #if request.user.has_perm('supplierList.query_supplier'):
#     data=SupplierList.objects.values("supplier_name").filter(supplier_name__isnull=False).annotate(sid=Count("supplier_name")).order_by("-id")
#     data=json.dumps(list(data))
#     #data=list(data)

#     return render(request, 'insert.html', locals())

# @login_required
# def insertHandle(request):
#         if request.user.has_perm('supplierList.update_all_supplier'):
#             if request.method == 'POST':
             
#                 received_data = dict(request.POST)
#                 del received_data['submit']
#                 # #删除值为空的字典
#                 def changeListToString(data):
#                     result={}
#                     for i,j in data.items():
#                         if j[0]:
#                             print(i,j)
#                             result[i]=j[0];
#                     return result
                    
#                 received_data=changeListToString (received_data)
#                 print (received_data)
                

#                 # keys = list(received_data.keys())
#                 # received_data2={}
#                 # for key in keys:
#                 #     if  received_data[key][0]:
#                 #         received_data2[key]=received_data[key][0]
    
#                 print(received_data)
#                 k = KeyEvent(**received_data)     
#                 k.save()

#                 return HttpResponseRedirect('/keyEvent/showAllKeyEvents/')
#             else:
#                 raise Http404
#         else:
#             messages.success(request, '你没有权限访问这个页面')
#             return render(request, 'noPremission.html')


from django.http import HttpResponseRedirect ,StreamingHttpResponse
@login_required
def printPayment(request,id):
    
    # data=KeyEvent.objects.filter(id=id)[0]
    # print(data.supplier_class)
    return render(request, 'printPayment.html', locals())


def download(request):
    generatePDF()
    return render(request, 'viewer.html', locals())


import reportlab.lib.fonts              
#canvas画图的类库
from reportlab.pdfgen.canvas import Canvas  
from reportlab.pdfbase import pdfmetrics
#用于定位的inch库，inch将作为我们的高度宽度的单位
from reportlab.lib.units import inch                    
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

def generatePDF():
    pdfmetrics.registerFont(TTFont('hei', 'SIMHEI.TTF'))
    canvas = Canvas('report.pdf',pagesize=(207*mm,121*mm)) 
    #setFont是字体设置的函数，第一个参数是类型，第二个是大小
    pdfmetrics.registerFont(TTFont("haha", "simsun.ttc"))
    canvas.setFont("haha", 4*mm)  
    #向一张pdf页面上写string
    canvas.drawCentredString(100*mm, 110*mm, u"广东美味鲜调味食品有限公司")  
    canvas.setFont("haha", 8*mm)  
    canvas.drawCentredString(100*mm, 100*mm, u"付款审批单") 

    # canvas.circle(60, 30, 5, stroke=1, fill=0)
    canvas.setLineWidth(0.3*mm)
    tableStart=15*mm
    tableStop=192*mm
    line1Hight=90*mm
    line2Hight=80*mm
    line3Hight=67*mm
    line4Hight=57*mm
    line5Hight=47*mm
    line6Hight=37*mm
    canvas.line(tableStart,line1Hight,tableStop,line1Hight)
    canvas.line(tableStart,line2Hight,tableStop,line2Hight)
    canvas.line(tableStart,line3Hight,tableStop,line3Hight)
    canvas.line(tableStart,line4Hight,tableStop,line4Hight)
    canvas.line(tableStart,line5Hight,tableStop,line5Hight)
    canvas.line(tableStart,line6Hight,tableStop,line6Hight)
    #showpage将保留之前的操作内容之后新建一张空白页
    canvas.showPage()                      
    #将所有的页内容存到打开的pdf文件里面。
    canvas.save()                   