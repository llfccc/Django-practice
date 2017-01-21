#coding=utf-8
from django.db import connection
from .models import  CodeTable
from operator import itemgetter, attrgetter
from django.forms.models import model_to_dict

def findMaxNumber():
    cursor = connection.cursor()
    cursor.execute("""SELECT distinct  U8code   FROM stockcode_codetable""")
    row = cursor.fetchall()
    cursor.close()

    result = {}
    for temp in row:
        if temp[0]:
            categroy = temp[0][:3].upper()
            try:
                num = int(temp[0][3:])
            except:
                num= 0

            if categroy not in result:
                result[categroy] = [num]
            else:
                result[categroy].append(num)
    for t in result:
        result[t] = max(result[t])+1
    return result

def processDataset():
    maxNumber=findMaxNumber()

    dataset=CodeTable.objects.filter(add_completed="0").filter(varified=1).order_by('material_category')
    result=dataset.values()

    for code in result:
        #code['recommend']是自动生成的一个存货编号
        code['recommend']=code['material_category']+str(maxNumber.get(code['material_category'])).zfill(5)
        #code['category']物资大类
        code['category']=code['material_category'][0]
        if maxNumber.get(code['material_category']):
            maxNumber[code['material_category']]+=1
        pass
    return result
