#coding=utf-8
from docxtpl import DocxTemplate
import functools
import time,datetime
import os,sys
import functools
import pandas as pd
# reload(sys)
# sys.setdefaultencoding('utf8')
import win32com.client
import pythoncom
from .models import RegistrationTable
from django.forms.models import model_to_dict  


#读取上传后的excel文件
def handle_uploaded_excel():
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    file_name = r"F:\django_wzb\wzb\upload\target2.xlsx"
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
    result=insert_db(data)


def insert_db(data):
    df=pd.DataFrame(list(data[1:]),columns=data[0])
    price=df.groupby([u'供应商']).sum()[u'结算金额']
    price=dict(price)

    id=5
    for k,v in price.items():
        id=id+1
        p=RegistrationTable(id=id,supplier_name=k,amount_in_figures=v)
        p.save()
    return price

def generated_doc(modelName="f:\\f.docx"):
    doc = DocxTemplate(modelName)
    data=RegistrationTable.objects.order_by('id')[10:16]

    pt=cnumber()  
    print pt.cwchange('600190101000.80')  
    for d in data:
        d=model_to_dict(d) 
        doc = DocxTemplate(modelName)
        context = { u"companyName" : d['company_name'],u"supplierName" : d['supplier_name'],u"price" : d['amount_in_figures'],u"bankOfDeposit" : d['bank_of_deposit'] }
        doc.render(context)
        doc.save("%s.docx" %context['supplierName'])


class cnumber:
    cdict={}
    gdict={}
    xdict={}
    def __init__(self):
        self.cdict={1:u'',2:u'拾',3:u'佰',4:u'仟'}
        self.xdict={1:u'元',2:u'万',3:u'亿',4:u'兆'} #数字标识符
        self.gdict={0:u'零',1:u'壹',2:u'贰',3:u'叁',4:u'肆',5:u'伍',6:u'陆',7:u'柒',8:u'捌',9:u'玖'}       

    def csplit(self,cdata): #拆分函数，将整数字符串拆分成[亿，万，仟]的list
        g=len(cdata)%4
        csdata=[]
        lx=len(cdata)-1
        if g>0:
            csdata.append(cdata[0:g])
        k=g
        while k<=lx:
            csdata.append(cdata[k:k+4])
            k+=4
        return csdata
    
    def cschange(self,cki): #对[亿，万，仟]的list中每个字符串分组进行大写化再合并
        lenki=len(cki)
        i=0
        lk=lenki
        chk=u''
        for i in range(lenki):
            if int(cki[i])==0:
                if i<lenki-1:
                    if int(cki[i+1])!=0:
                        chk=chk+self.gdict[int(cki[i])]                    
            else:
                chk=chk+self.gdict[int(cki[i])]+self.cdict[lk]
            lk-=1
        return chk
        
    def cwchange(self,data):
        cdata=str(data).split('.')
        
        cki=cdata[0]
        ckj=cdata[1]
        i=0
        chk=u''
        cski=self.csplit(cki) #分解字符数组[亿，万，仟]三组List:['0000','0000','0000']
        ikl=len(cski) #获取拆分后的List长度
        #大写合并
        for i in range(ikl):
            if self.cschange(cski[i])=='': #有可能一个字符串全是0的情况
                chk=chk+self.cschange(cski[i]) #此时不需要将数字标识符引入
            else:
                chk=chk+self.cschange(cski[i])+self.xdict[ikl-i] #合并：前字符串大写+当前字符串大写+标识符
        #处理小数部分
        lenkj=len(ckj)
        if lenkj==1: #若小数只有1位
            if int(ckj[0])==0: 
                chk=chk+u'整'
            else:
                chk=chk+self.gdict[int(ckj[0])]+u'角整'
        else: #若小数有两位的四种情况
            if int(ckj[0])==0 and int(ckj[1])!=0:
                chk=chk+u'零'+self.gdict[int(ckj[1])]+u'分'
            elif int(ckj[0])==0 and int(ckj[1])==0:
                chk=chk+u'整'
            elif int(ckj[0])!=0 and int(ckj[1])!=0:
                chk=chk+self.gdict[int(ckj[0])]+u'角'+self.gdict[int(ckj[1])]+u'分'
            else:
                chk=chk+self.gdict[int(ckj[0])]+u'角整'
        return chk