#coding=utf-8
from docxtpl import DocxTemplate




#读取上传后的excel文件
def handle_uploaded_excel(file):
    pythoncom.CoInitializeEx(pythoncom.COINIT_MULTITHREADED)
    file_name = r"F:\django_wzb\wzb\upload\target.xlsx"
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

    
def generated_doc(modelName="f.docx"):
    doc = DocxTemplate(modelName)
    context = { u"companyName" : u"有限公司",u"supplierName" : u"测试供应商名称",u"price" : "13434324",u"bankOfDeposit" : u"开户行" }
    doc.render(context)
    doc.save("generated_doc.docx")