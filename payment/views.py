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
from docx_tpl import handle_uploaded_excel,insert_db,generated_doc
from convertData import charToNumber,ClosingDate
from .forms import UploadFileForm,ApplicantForm
import zipfile,datetime
from django.http import HttpResponseRedirect ,StreamingHttpResponse
from django.contrib import messages
from django.core import serializers


@login_required
def upload_file(request):
    chinese_name = request.user.profile.chinese_name
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

                data = handle_uploaded_excel()      
                result=insert_db(data,SupplierPaymentDict,company_name,chinese_name)          
                response = HttpResponseRedirect('/payment/showPayment/')
                return response

        else:
            form = UploadFileForm()

            response=render(request, 'upload.html', locals())
            return response

    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')


#申请表表单
@login_required
def insertPayment(request):
    chinese_name = request.user.profile.chinese_name

    if request.user.has_perm('payment.edit_payment'):
        if request.method == 'POST':
            form_content = ApplicantForm(request.POST)
            if form_content.is_valid():
                cleaned_data=form_content.cleaned_data
                cleaned_data['user_id']=request.user.id
                cleaned_data['application_time']=datetime.datetime.now()
                company_name = form_content.cleaned_data['company_name']
                supplier_name = form_content.cleaned_data['supplier_name']
                amount_in_figures = form_content.cleaned_data['amount_in_figures']

                SupplierPaymentCode=SupplierPayment.objects.all()
                SupplierPaymentDict=[]
                for k in SupplierPaymentCode:
                    SupplierPaymentDict.append(model_to_dict(k))
                data=[(1,1,u'结算单号',u'计算日期',u'供应商',2,u'发票号',4,5,6,2,1,u'结算金额',5,2,3, None),
                    (u'1', None, u'000000000008305', 1, supplier_name,u'RG20161202585',  u'0000002500', u'Z1400040', u'15kg/\u888b',  u'kg', 1500.0, 5.2,amount_in_figures, 5.2, 7800.0, u'\u674e\u8bd7\u871c', None)]
                result=insert_db(data,SupplierPaymentDict,company_name,chinese_name)       

                messages.success(request, '添加成功，请确认是否已包含所有条目')
                # message=u'提交了一批文档'
                # add_note(request,request.user,message)
                return HttpResponseRedirect('/payment/showPayment/')
        else:
            db=SupplierPayment.objects
            supplier_name=db.values("supplier_name").filter(supplier_name__isnull=False).distinct()
            supplier_name=json.dumps(list(supplier_name))
            company_name=SupplierPayment.objects.values("company_name").filter(company_name__isnull=False).distinct()
            company_name=json.dumps(list(company_name))


            form = ApplicantForm(initial={'user_id':1})
            return render(request, 'insertPayment.html', locals())
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')

@login_required
def showAllPayment(request):
    if request.user.has_perm('payment.query_payment'):     
        if request.method == 'POST':
            start_date=request.POST['start_date']
            end_date=request.POST['end_date']
            if not start_date:
                start_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            if not end_date:
                end_date=datetime.date.today() + datetime.timedelta(days=1)
            else:
                end_date =  datetime.datetime.strptime(end_date, "%Y-%m-%d").date()+ datetime.timedelta(days=1)
            b=RegistrationTable.objects.filter(deleted='0').filter(record_date__range=(start_date, end_date)).order_by('-id')
        else:
            start_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            end_date=datetime.date.today() + datetime.timedelta(days=1)
            b=RegistrationTable.objects.filter(deleted='0').filter(record_date__range=(start_date, end_date)).order_by('-id') 
        return render(request, 'showAllPayment.html', locals())
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')
        

@login_required
def showPayment(request):
    if request.user.has_perm('payment.edit_payment'):
        chinese_name = request.user.profile.chinese_name
        if request.method == 'POST':
            start_date=request.POST['start_date']
            end_date=request.POST['end_date']
            if not start_date:
                start_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            if not end_date:
                end_date=datetime.date.today() + datetime.timedelta(days=1)
            else:
                end_date =  datetime.datetime.strptime(end_date, "%Y-%m-%d").date()+ datetime.timedelta(days=1)
            b=RegistrationTable.objects.filter(deleted='0').filter(applicant=chinese_name).filter(record_date__range=(start_date, end_date)).order_by('-id')
        else:
            start_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
            end_date=datetime.date.today() + datetime.timedelta(days=1)
            b=RegistrationTable.objects.filter(deleted='0').filter(applicant=chinese_name).filter(record_date__range=(start_date, end_date)).order_by('-id')   
        return render(request, 'showPayment.html', locals())
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')


#接收供应商更新的订单信息
@login_required
def updatePayment(request): 
    chinese_name = request.user.profile.chinese_name
    if request.method == 'POST':        
        received_data = json.loads(request.body)     
    
    def changeListToString(data):
        result={}
        for i,j in data.items():                        
            if j[0]:      
                result[i]=j[0];
        return result

    for k, v in received_data.items():
        pass
        if v['transfer_finance']:
            transfer_finance=v["transfer_finance"]
            t=RegistrationTable.objects.filter(id=k)[0]
            pt=charToNumber()
            amount_in_words=pt.cwchange(float(t.amount_in_figures))       
            x={}
            x['payment_date']=t.payment_date
            x['closing_date']=t.closing_date
            x['transfer_finance']=transfer_finance    
            cd=ClosingDate(x)                    
            expiring_date= cd.getClosingDate()  
            RegistrationTable.objects.filter(id=k).update(transfer_finance=transfer_finance,applicant=chinese_name,deleted=0,expiring_date=expiring_date,amount_in_words=amount_in_words)

    return str("success")



@login_required
def edit(request,id):
    if request.user.has_perm('payment.edit_payment'):
        data=RegistrationTable.objects.filter(id=id)[0]
        supplier_name=SupplierPayment.objects.values("supplier_name").filter(supplier_name__isnull=False).distinct()
        supplier_name=json.dumps(list(supplier_name))
        company_name=SupplierPayment.objects.values("company_name").filter(company_name__isnull=False).distinct()
        company_name=json.dumps(list(company_name))


        Supplier = SupplierPayment.objects.all()
        from collections import defaultdict
        result = {} 
        for t in Supplier:  
            k=model_to_dict(t) 
            if k['supplier_name']:   
                if   result.has_key(k['supplier_name']): 
                    result[k['supplier_name']][k['company_name']]=k                    
                else:
                    result[k['supplier_name']]={}
                    result[k['supplier_name']][k['company_name']]=k           

        result=json.dumps(result)
        return render(request, 'editPayment.html', locals())
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')


@login_required
def delete(request,id):
    obj=RegistrationTable.objects.filter(id=id).update(deleted='1')
    return HttpResponseRedirect('/payment/showPayment/')

@login_required
def editHandle(request):
        chinese_name= request.user.profile.chinese_name
        if request.user.has_perm('payment.edit_payment'):
            if request.method == 'POST':             
                received_data = dict(request.POST)                
                del received_data['submit']            
                # #删除值为空的字典
                def changeListToString(data):
                    result={}
                    for i,j in data.items():                        
                        if j[0]:      
                            result[i]=j[0];
                    return result
                received_data=changeListToString (received_data)                               
                if  not received_data.get('amount_in_words'): 
                    pt=charToNumber()  
                    received_data['amount_in_words']=pt.cwchange(float(received_data['amount_in_figures']))
                #计算付款期限
                if not received_data.get('expiring_date'):
                    if received_data.get('transfer_finance'):
                        try:                      
                            x={}
                            x['payment_date']=received_data['payment_date']
                            x['closing_date']=received_data['closing_date']
                            x['transfer_finance']=received_data['transfer_finance']                                  
                            cd=ClosingDate(x)                    
                            received_data['expiring_date']= cd.getClosingDate()
                        except:
                            messages.success(request, '缺少必须的项')
                            return HttpResponseRedirect('/payment/edit/%s' %received_data['id'])
                received_data['applicant']=chinese_name
                received_data['deleted']=0
                k = RegistrationTable(**received_data)     
                k.save()
                return HttpResponseRedirect('/payment/showPayment/')
            else:
                raise Http404
        else:
            messages.success(request, '你没有权限访问这个页面')
            return render(request, 'noPremission.html')

@login_required
def download(request):
    if request.method == 'POST':             
        received_data = dict(request.POST)
        downloadList=[]
        for t in received_data.keys():
            id=t[8:]
            if id.isdigit():
                downloadList.append(id)


    chinese_name= request.user.profile.chinese_name
    data=RegistrationTable.objects.filter(id__in=downloadList).order_by('id')
    generated_doc(chinese_name,data)
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
