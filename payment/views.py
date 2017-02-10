# coding=utf-8
from django.shortcuts import render

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render
import os,sys,json,time
# sys.path.append("..")
# from supplierList.models import SupplierList
from .models import RegistrationTable,SupplierPayment
from django.db.models import Count, Avg
from django.contrib.auth.decorators import login_required, permission_required

from django.forms.models import model_to_dict
from django.http import HttpResponse
from docx_tpl import handle_uploaded_excel,generated_doc
from convertData import charToNumber,ClosingDate
from .forms import UploadFileForm
import zipfile
from django.http import HttpResponseRedirect ,StreamingHttpResponse

@login_required
def upload_file(request):
    if request.user.has_perm('stockCode.add_codetable'):
        if request.method == 'POST':
            form_content =UploadFileForm(request.POST, request.FILES)
            if form_content.is_valid():
                myFile = form_content.cleaned_data['file']
                company_name = form_content.cleaned_data['company_name']
                # 保存上传的文件为指定的文件名

                def writeExcel():
                    with open(os.path.join("F:\\django_wzb\\wzb\\upload", 'target2.xlsx'), 'wb+') as f:
                        for chunk in myFile.chunks():      # 分块写入文件
                            f.write(chunk)
                try:
                    writeExcel()
                except:
                    time.sleep(4)
                    writeExcel()

                SupplierPaymentCode=SupplierPayment.objects.all()
                SupplierPaymentDict=[]
                for k in SupplierPaymentCode:
                    SupplierPaymentDict.append(model_to_dict(k))

                insert_result = handle_uploaded_excel(SupplierPaymentDict,company_name)                
                response = HttpResponseRedirect('/payment/showAllPayment/')
                return response

        else:
            form = UploadFileForm()

            response=render(request, 'upload.html', locals())
            return response

    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')



@login_required
def showAllPayment(request):

    b=RegistrationTable.objects.order_by('-id')[:10]
    return render(request, 'showAllPayment.html', locals())

@login_required
def download(request):
    
    chinese_name= request.user.profile.chinese_name
    generated_doc(chinese_name)
    def make_zip(source_dir, output_filename):
        zipf = zipfile.ZipFile(output_filename, 'w',zipfile.ZIP_DEFLATED)
        pre_len = len(os.path.dirname(source_dir))
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname)
        zipf.close()

    source_dir=sys.path[0]+r"\\doc\\%s\\" %chinese_name
    output_filename = sys.path[0]+"%s.zip" %chinese_name
    make_zip(source_dir, output_filename)

    response = StreamingHttpResponse(open(output_filename, "rb").read())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="doc.zip"'
    return response


@login_required
def edit(request,id):
    data=RegistrationTable.objects.filter(id=id)[0]
    return render(request, 'editPayment.html', locals())


@login_required
def editHandle(request):
        if request.user.has_perm('supplierList.update_all_supplier'):
            if request.method == 'POST':             
                received_data = dict(request.POST)
                print(received_data)
                del received_data['submit']
            
                # #删除值为空的字典
                def changeListToString(data):
                    result={}
                    for i,j in data.items():                        
                        if j[0]:      
                            result[i]=j[0];
                    return result

                received_data=changeListToString (received_data)               
                if not  received_data.has_key('amount_in_words'):
                    pt=charToNumber()  
                    received_data['amount_in_words']=pt.cwchange(float(received_data['amount_in_figures']))
                cd=ClosingDate()
                x={}
                x['payment_date']=received_data['payment_date']
                x['closing_date']=received_data['closing_date']
                x['transfer_finance']=received_data['transfer_finance']
                print(cd.getClosingDate(x))
                k = RegistrationTable(**received_data)     
                k.save()

                return HttpResponseRedirect('/payment/showAllPayment/')
            else:
                raise Http404
        else:
            messages.success(request, '你没有权限访问这个页面')
            return render(request, 'noPremission.html')
#@login_required
# # 显示未经编码的内容

# @login_required
# def showAllKeyEvents(request):
#     chinese_name = request.user.profile.chinese_name
#     b = KeyEvent.objects.order_by('-id')[:10]

#     return render(request, 'showAllKeyEnvet.html', locals())


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


