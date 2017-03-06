# encoding:utf-8
from .models import CodeTable
from django.contrib.auth.models import User
from accounts.models import Profile
from notifications.signals import notify
from django.utils import timezone
from .models import CodeTable
from django.contrib.auth.models import User

from notifications.signals import notify

import functools
import time,datetime
import os
import functools
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
import win32com.client
import pythoncom
# if "g:\\anaconda3" not in sys.path:
#     sys.path.append("g:\\anaconda3")

#转换浮点数为数字
def convertFloatChar(model):
    try:
        float(model)
        model = int(model)
    except:
        pass
    return model


# 建立一个装饰器计算函数耗时
def time_me(info="used"):
    def _time_me(fn):
        @functools.wraps(fn)
        def _wrapper(*args, **kwargs):
            start = time.clock()
            fn(*args, **kwargs)
            # print "%s %s %s" % (fn.__name__, info, time.clock() - start), "second"
        return _wrapper
    return _time_me  # encoding:utf-8


#获取读取后的excel内容，并排除前3行，只读取有效内容
def handle_data(file, request):
    data = handle_uploaded_excel(file)
    for k, v in enumerate(data[3:]):
        if v[0]:
            pass
        else:
            result = data[3:k + 3]
            break
    insert_result = insert_db(result, request)
    return insert_result


#读取上传后的excel文件
def handle_uploaded_excel(file):
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    file_name = r"F:\upload\target.xlsx"
    table = 'Sheet1'
    xlApp = win32com.client.Dispatch('Excel.Application')  # 打开EXCEL，这里不需改动
    xlApp.Visible = False
    xlBook = xlApp.Workbooks.Open(file_name)  # 将D:\\1.xls改为要处理的excel文件路径
    xlSht = xlBook.Worksheets(table)  # 要处理的excel页，默认第一页是‘sheet1’
    rowcount = xlSht.UsedRange.Rows.Count
    colcount = 17  # 读取几列xlSht.UsedRange.Columns.count
    data = xlSht.Range(xlSht.Cells(1, 1), xlSht.Cells(
        rowcount + 1, colcount + 1)).Value
    xlBook.Close(SaveChanges=1)  # 完成 关闭保存文件
    del xlApp

    return data

def insert_db(result, request):
    for i in range(len(result)):
        b = CodeClass(result[i])
        k = CodeTable(**b.__dict__)
        k.applicant = request.user.profile.chinese_name
        k.application_time = datetime.datetime.now()
        k.user_id = request.user.id
        k.group_name = Profile.objects.get(
            chinese_name=k.applicant).group_name
        # k.save()
        try:
            k.save()
        except:
            return u"有部分数据项插入不成功，可能是因为缺少必填项"


def add_note(request, receiver, message):
    user_name = receiver.profile.chinese_name
    group_name = receiver.profile.group_name
    t = Profile.objects.filter(group_name=group_name).filter(
        title_name='主管').first()
    final_message = user_name + message
    notify.send(request.user, recipient=t.user, verb=final_message)


def send_notificiton(request, receiver, message):
    receiver_id = Profile.objects.filter(chinese_name=receiver).first().id
    user = User.objects.get(id=receiver_id)
    final_message = message
    notify.send(request.user, recipient=user, verb=final_message)


class CodeClass:
    def __init__(self, result):
        self.accounts_set = result[2]
        try:
            self.material_category = result[3].upper()
        except:
            pass
        self.material_name = result[4]
        self.brand = result[5]
        self.serial_number = result[6]
        self.model = convertFloatChar(result[7])
        self.unit = result[8]
        self.number = result[9]
        self.remark = result[10]
        self.demand_department = result[11]
        self.equipment_name = result[12]
        self.equipment_model = result[13]
        self.manufacturers = result[14]
        self.grade = result[15]
        self.vender = result[16]


def add_note(request, receiver, message):
    try:
        user_name = receiver.profile.chinese_name
        group_name = receiver.profile.group_name
        t = Profile.objects.filter(group_name=group_name).filter(
            title_name='主管').first()
        final_message = user_name + message
        notify.send(request.user, recipient=t.user, verb=final_message)
    except:
        pass


def send_notificiton(request, receiver, message):
    try:
        receiver_id = Profile.objects.filter(chinese_name=receiver).first().id
        user = User.objects.get(id=receiver_id)
        final_message = message
        notify.send(request.user, recipient=user, verb=final_message)
    except:
        pass


