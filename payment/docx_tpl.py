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
from django.db import connection

#读取上传后的excel文件
def handle_uploaded_excel(SupplierPaymentDict,company_name):
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
    result=insert_db(data,SupplierPaymentDict,company_name)


def insert_db(data,SupplierPaymentDict,company_name):
    
    supplierDF=pd.DataFrame.from_dict(SupplierPaymentDict)
    now_date=datetime.datetime.now()
    priceDF=pd.DataFrame(list(data[1:]),columns=data[0])
    priceDF=pd.DataFrame(priceDF.groupby([u'供应商',u'发票号']).sum()[u'结算金额'])  
    priceDF.reset_index(level=0, inplace=True)
    priceDF.reset_index(level=0, inplace=True)
    
    priceDF.columns = ['document_num','supplier_name','amount_in_figures']

    priceDF['company_name']=company_name
    priceDF['record_date']=now_date
    priceDF['cheque']='√'
    priceDF['cash']='×'
    priceDF['acceptance_bill']='×'
   
    resultDF = pd.merge(priceDF,supplierDF , how='left', left_on=['supplier_name','company_name'],
                    right_on=['supplier_name','company_name'], suffixes=['_l', '_r']) 

    cursor = connection.cursor()
    cursor.execute("""SELECT max(max_num)   FROM  payment_registrationtable""")
    currentMax=[]
    currentMax.append(cursor.fetchall()[0][0])
    cursor.close()


    list_to_insert = list()
    def df2list(x,currentMax):
        currentMax[0]+=1        
        pt=charToNumber()  
        list_to_insert.append(RegistrationTable(supplier_name=x.supplier_name,amount_in_figures=x.amount_in_figures,bank_account=x.bank_account,\
            bank_of_deposit=x.bank_of_deposit,closing_date=x.closing_date,max_num=currentMax[0],\
            company_name=x.company_name,record_date=x.record_date,cheque=x.cheque,cash=x.cash,acceptance_bill=x.acceptance_bill,document_num=x.document_num,\
            payment_date=x.payment_date))    

    #将df保存为一个列表，以便批量插入数据库
    resultDF.apply(lambda x:df2list(x,currentMax),axis=1)

    RegistrationTable.objects.bulk_create(list_to_insert)

    return 1

def generated_doc(chinese_name,modelName="f:\\f.docx"):
  
    path=sys.path[0]+r"\\doc\\%s\\" %chinese_name
    doc = DocxTemplate(modelName)
    data=RegistrationTable.objects.order_by('id')[10:16]

    for d in data:
        d=model_to_dict(d) 
        doc = DocxTemplate(modelName)
        context = { u"company_name" : d['company_name'],u"supplier_name" : d['supplier_name'],u"amount_in_figures" : d['amount_in_figures'],\
            u"bank_of_deposit" : d['bank_of_deposit'],u"bank_account" : d['bank_account'],u"amount_in_words" : d['amount_in_words']  }
        doc.render(context)
        doc.save(path+"%s.docx" %context['supplier_name'])