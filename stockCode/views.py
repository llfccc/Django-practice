# coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, render
from .forms import UploadFileForm,ApplicantForm
from .function import handle_data,add_note,send_notificiton
from .models import FileModel, CodeTable,MaterialProperty,MeasurementUnit,Warehouse
from accounts.models import Profile
import os,sys,datetime,json,time,random, zipfile
from .function2 import processDataset
from .function3 import processExcel,removeFile
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
#from wzb.models import NewUser as User
from django.contrib import messages
# from django.template import RequestContext
# Imaginary function to handle an uploaded file.
from django.forms.models import model_to_dict
# reload(sys)
# sys.setdefaultencoding('utf8')
from echarts import Echart, Legend, Bar, Axis
from django.http import HttpResponseRedirect ,StreamingHttpResponse

# 接收上传文件并读取保存到数据库中

@login_required
def upload_file(request):
    if request.user.has_perm('stockCode.add_codetable'):
        if request.method == 'POST':

            form_content =UploadFileForm(request.POST, request.FILES)
            if form_content.is_valid():
                myFile = form_content.cleaned_data['file']
                # 保存上传的文件为指定的文件名
                htmlInt=int(request.POST.get('randomInt','0'))
                sessionInt=int(request.session.get("postToken",default=1))
                request.session["postToken"]=0
                # print (htmlInt)
                # print('********')
                # print (sessionInt)
                if sessionInt!=htmlInt:
                    # 不存在合法Token,该表单为重复提交
                    # return HttpResponse("请不要点击多次提交按钮")

                    return HttpResponseRedirect("/stockCode/showUnCode/")
                else:
                    def writeExcel():
                        with open(os.path.join("F:\\django_wzb\\wzb\\upload", 'target.xlsx'), 'wb+') as f:
                            for chunk in myFile.chunks():      # 分块写入文件
                                f.write(chunk)
                    try:
                        writeExcel()
                    except:
                        time.sleep(4)
                        writeExcel()

                    insert_result = handle_data(request.FILES['file'], request)
                    message=u'提交了一批文档'
                    add_note(request,request.user,message)
                    response = HttpResponseRedirect('/stockCode/showUnCode/')
                    # print(insert_result)

                    if insert_result:
                        messages.success(request, insert_result)
                        return response
                    try:
                        messages.success(request, '上传成功，请确认是否已包含所有条目')
                        return response
                    except:
                        messages.success(request, '发生了错误，请确认格式无误，否则请联系管理员')
                        return response

        else:
            form = UploadFileForm()
            randomInt=int(random.uniform(10000, 90000))
            response=render(request, 'upload.html', locals())
            request.session["postToken"]=randomInt

            return response

    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')

#申请表表单
@login_required
def insertApplicant(request):
    if request.user.has_perm('stockCode.add_codetable'):
        if request.method == 'POST':
            form_content = ApplicantForm(request.POST)
            if form_content.is_valid():
                cleaned_data=form_content.cleaned_data
                cleaned_data['user_id']=request.user.id
                cleaned_data['application_time']=datetime.datetime.now()
                try:
                    cleaned_data['material_category']=cleaned_data['material_category'].upper()
                except:
                    pass
                k = CodeTable(**cleaned_data)
                k.applicant=request.user.profile.chinese_name
                try:
                    k.group_name = Profile.objects.get(
                        chinese_name=k.applicant).group_name
                except:
                    k.group_name=u'未找到'
                    pass
                k.save()
                messages.success(request, '添加成功，请确认是否已包含所有条目')
                message=u'提交了一批文档'
                add_note(request,request.user,message)
                return HttpResponseRedirect('/stockCode/showUnCode/')
        else:
            form = ApplicantForm(initial={'user_id':1})
            return render(request, 'insertApplicant.html', locals())
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')



def test(request):
    b = {'material_name': 3, 'accounts_set': 2, 'applicant': 3}
    k = CodeTable(**b)
    k.save()

# 显示未经编码的内容
@login_required
def showUnCode(request):
    chinese_name = request.user.profile.chinese_name
    b = CodeTable.objects.filter(
        applicant=chinese_name, add_completed=0).order_by('-id')
    return render(request, 'showUnCode.html', locals())


#删除未审核的编码
@login_required
def delCode(request,id):
    try:
        id=int(id)

    except:
        id=0
    chinese_name = request.user.profile.chinese_name
    b = CodeTable.objects.get(id=id)

    if chinese_name==b.applicant and b.varified==0:
        CodeTable.objects.get(id=id).delete()
        messages.success(request, '删除成功')
        return HttpResponseRedirect('/stockCode/showUnCode/')
    else:
        messages.success(request, '你没有权限删除已审核的编码或者你不是该编码的申请者')
        return render(request, 'noPremission.html')

# 显示已经编码的内容
@login_required
def showAlreadyCode(request):
    if request.method == 'POST':
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']
        if not start_date:
            start_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if not end_date:

            end_date=datetime.date.today() + datetime.timedelta(days=1)
        else:
            end_date =  datetime.datetime.strptime(end_date, "%Y-%m-%d").date()+ datetime.timedelta(days=1)

        chinese_name = request.user.profile.chinese_name
        b = CodeTable.objects.filter(
            applicant=chinese_name, U8code__isnull=False).filter(application_time__range=(start_date, end_date)).order_by('-id')
        b_len=len(b)
    return render_to_response('showAleradyCode.html', locals())

# 主管审核新增编码申请
@login_required

def varifyCode(request):
    if request.user.has_perm('stockCode.varify_application'):
        group_name = request.user.profile.group_name
        # print(group_name)
        # test=CodeTable.objects.get(id=21).profile.group_name

        # .filter(user.profile.group_name=group_name)
        b = CodeTable.objects.filter(varified="0").filter(group_name=group_name)
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')
    return render(request, 'varifyCode.html', locals())

# 审核编码申请操作


@login_required
@permission_required('stockCode.varify_application')
def varifyApplication(request):

    if request.method == 'POST':

        received_json_data = json.loads(request.body)

    else:
        raise Http404

    for k, v in received_json_data.items():

        if v['checked']:
            p = CodeTable.objects.get(id=k)
            p.varified = 1
            p.varified_time = datetime.datetime.now()
            p.varified_user_id = request.user.profile.chinese_name

            p.save()

    return HttpResponse('ok', content_type="text/html", status=200)


@login_required
def editCode(request):

    if request.user.has_perm('stockCode.edit_u8code'):
        codeDataset=processDataset().__dict__['_result_cache']

        materialProperty=MaterialProperty.objects.all()
        materialDict=[]
        for k in materialProperty:
            materialDict.append(model_to_dict(k))

        measurementUnitCode=MeasurementUnit.objects.all()
        measurementDict=[]
        for k in measurementUnitCode:
            measurementDict.append(model_to_dict(k))

        WarehouseCode = Warehouse.objects.all()
        WarehouseCodeDict=[]
        for k in WarehouseCode:
            WarehouseCodeDict.append(model_to_dict(k))
        removeFile()
        account_count=[]
        account_count=processExcel(codeDataset,materialDict,measurementDict,WarehouseCodeDict)

        code_number=len(codeDataset)
        account_number=len(account_count)
    else:
        messages.success(request, '你没有权限访问这个页面')
        return render(request, 'noPremission.html')
    return render(request, 'editCode.html', locals())

@login_required
@permission_required('stockCode.edit_u8code')
def receiveCode(request):

    if request.method == 'POST':
        received_json_data = json.loads(request.body)
    else:
        raise Http404

    receivers=[]
    for k, v in received_json_data.items():
        if v['code']:
            p = CodeTable.objects.get(id=k)
            p.U8code = v['code']
            p.add_completed=1
            p.add_code_time = datetime.datetime.now()
            p.add_code_time_username = request.user.profile.chinese_name

            p.save()
            message='你的一部分编码已经添加了'
            receivers.append(CodeTable.objects.get(id=k).applicant)
    receivers_set=set(receivers)
    for receiver in receivers_set:
        send_notificiton(request,receiver,message)

    return HttpResponse('ok', content_type="text/html", status=200)


# 下载文件
@login_required
def downloadZip(request):
    def make_zip(source_dir, output_filename):
        zipf = zipfile.ZipFile(output_filename, 'w',zipfile.ZIP_DEFLATED)
        pre_len = len(os.path.dirname(source_dir))
        for parent, dirnames, filenames in os.walk(source_dir):
            for filename in filenames:
                pathfile = os.path.join(parent, filename)
                arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
                zipf.write(pathfile, arcname)
        zipf.close()
    source_dir = 'e:\\code'
    output_filename = "e:\\code.zip"
    make_zip(source_dir, output_filename)

    response = StreamingHttpResponse(open(output_filename, "rb").read())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="code.zip"'
    return response


@login_required
def downloadModel(request):

    output_filename = "f:\\django_wzb\\wzb\\downloadModel\\codeV3.xlsx"

    response = StreamingHttpResponse(open(output_filename, "rb").read())
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="codeV3.xlsx"'
    return response

# 显示已经编码的内容
@login_required
def showAllAddCode(request):
    if request.method == 'POST':
        start_date=request.POST['start_date']
        end_date=request.POST['end_date']

        if not start_date:
            start_date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        if not end_date:
            end_date=datetime.date.today() + datetime.timedelta(days=1)

        chinese_name = request.user.profile.chinese_name
        b = CodeTable.objects.filter(U8code__isnull=False).filter(add_code_time__range=(start_date, end_date)).order_by('-id')

    return render_to_response('showAllAddCode.html', locals())


@login_required
def dataStatistics(request):
    chart = Echart('GDP', 'This is a fake chart')
    chart.use(Bar('China', [2, 3, 4, 5]))
    chart.use(Legend(['GDP']))
    chart.use(Axis('category', 'bottom', data=['Nov', 'Dec', 'Jan', 'Feb']))
    return render(request, 'dataStatistics.html', locals())
