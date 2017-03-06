# coding=utf-8
import pandas as pd
import numpy as np
import shutil
import os,sys

import wzb.settings
PROJECT_ROOT=wzb.settings.PROJECT_ROOT


# 用来生成批量导入表
def processExcel(codeDataset, materialDict, measurementDict, WarehouseCodeDict):
    # codeDF是编码表，materialDF是物资属性表，measurementDF是计量单位表
    codeDF = pd.DataFrame.from_dict(codeDataset)
    materialDF = pd.DataFrame.from_dict(materialDict)
    measurementDF = pd.DataFrame.from_dict(measurementDict)
    WarehouseDF = pd.DataFrame.from_dict(WarehouseCodeDict)

    lenDF = len(codeDF)

    account_count=[]       #保存具体有多少个账套生成了

    if not codeDF.empty:
        codeDF = pd.merge(codeDF, materialDF, how='left', left_on='material_category',
                          right_on='material_category', suffixes=['_l', '_r'])
        codeDF['material_category'] = codeDF['material_category'].apply(lambda x: x + '0')
        
            
        # 遍历新增编码中的所有账套
        
        all_accounts = ["009","012", "100","901","905"]
        for account in all_accounts:
            
            newDF = codeDF[codeDF.accounts_set.str.contains(account)]

            if not newDF.empty:
                account_count.append(account)
                newDF["account_set"] = account
                encodeDF = pd.merge(newDF, measurementDF, how='left', left_on=['unit', 'account_set'], right_on=[
                                  'measurement_unit', 'accounts_set'], suffixes=['_l', '_r'])
                #存货对照表                  
                inventoryDF = pd.merge(encodeDF, WarehouseDF, how='left', left_on=['category', 'account_set'],
                                       right_on=['material_category', 'accounts_set'], suffixes=['_l', '_r'])
                generate_excel(encodeDF,inventoryDF, account)
    return account_count

def generate_excel(encodeDF, inventoryDF, fileName):
    lenDF = len(encodeDF)
    sheet1 = pd.DataFrame()
    sheet2 = pd.DataFrame()
    # sheet3=pd.DataFrame()
    sheet4 = pd.DataFrame()
    sheet7 = pd.DataFrame()
    sheet8 = pd.DataFrame()
    sheetNone = pd.DataFrame()
    sheet1[u'存货编码'] = encodeDF.ix[:, 'recommend']
    sheet1[u'存货名称'] = encodeDF.ix[:, 'material_name']
    sheet1[u'规格型号'] = encodeDF.ix[:, 'model']
    sheet1[u'存货大类编码'] = encodeDF.ix[:, 'material_category']
    sheet1[u'计量单位组编码'] = encodeDF.ix[:, 'measurement_unit_group_code']
    sheet1[u'主计量单位编码'] = encodeDF.ix[:, 'measurement_unit_code']
    sheet1[u'海关单位换算率'] = np.array([1.0] * lenDF)
    sheet1[u'是否内销'] = encodeDF.ix[:, 'domestic']
    sheet1[u'是否采购'] = encodeDF.ix[:, 'purchase']
    sheet1[u'是否生产耗用'] = encodeDF.ix[:, 'productionconsumption']
    sheet1[u'是否进口'] = encodeDF.ix[:, 'import_field']
    sheet1[u'是否在制'] = encodeDF.ix[:, 'manufacturing']

    #因为各账套存货大类不一致，导致问题，特殊处理
    #替换100账套中的U180等为U18
    if fileName=="100":
        replace_list=["U180","L030","L040","L050","B110","B120"]
        def f(df):
            if df in replace_list:        
                return df[:3]
            else :
                return df
        sheet1[u'存货大类编码']=sheet1[u'存货大类编码'].apply(f)

    #替换901账套中的p010等为U18
    if fileName=="901" or fileName=="905":
        replace_list=["P010","P020","P030","P040","P050","P060","P070","P080","P090","P100","X010","X020","X030","X040","X050","X060","X070"]
        def f(df):
            if df in replace_list:        
                return df[:3]
            else :
                return df
        sheet1[u'存货大类编码']=sheet1[u'存货大类编码'].apply(f)

    #排除901和905账套的品牌和货号，因为缺少字段导入不进去
    if(fileName!="901" and fileName!="905"):
        sheet1[u'存货扩展自定义项1'] = encodeDF.ix[:, 'brand']
        sheet1[u'存货扩展自定义项2'] = encodeDF.ix[:, 'serial_number']

    sheet2[u'存货编码'] = encodeDF.ix[:, 'recommend']
    sheet2[u'入库超额上限'] = encodeDF.ix[:, 'storagearea']
    sheet2[u'供应类型'] = np.array([u'领用'] * lenDF)
    sheet2[u'领料方式'] = np.array([0] * lenDF)

    sheet4[u'存货编码'] = encodeDF.ix[:, 'recommend']
    sheet4[u'允许BOM子件'] = np.array([1] * lenDF)

    sheet7[u'存货编码'] = encodeDF.ix[:, 'recommend']
    sheet7[u'建档人'] = np.array([u'王贝贝'] * lenDF)
    sheet7[u'变更人'] = np.array([u'王贝贝'] * lenDF)
    sheet7[u'是否考虑自由库存'] = np.array([1] * lenDF)

    sheet8[u'存货编码'] = encodeDF.ix[:, 'recommend']
    sheet8[u'存货自定义项4'] = encodeDF.ix[:, 'equipment_name']
    sheet8[u'存货自定义项5'] = encodeDF.ix[:, 'manufacturers']
    sheet8[u'存货自定义项6'] = encodeDF.ix[:, 'equipment_model']
    sheet8[u'存货自定义项8'] = encodeDF.ix[:, 'grade']  # 等级
    sheet8[u'存货自定义项9'] = encodeDF.ix[:, 'vender']  # 厂家

    if not encodeDF.empty:
        codeFilePath = PROJECT_ROOT+u'\\download\\code\\' + fileName + u"--A 编码表" + ".xls"
        writer = pd.ExcelWriter(codeFilePath)
        sheet1.to_excel(writer, index=None)
        sheet2.to_excel(writer, u'控制', index=None)
        sheetNone.to_excel(writer, u'成本', index=None)
        sheet4.to_excel(writer, u'计划', index=None)
        sheetNone.to_excel(writer, u'批次属性', index=None)
        sheetNone.to_excel(writer, u'质量', index=None)
        sheet7.to_excel(writer, u'其它', index=None)
        sheet8.to_excel(writer, u'自定义', index=None)
        sheetNone.to_excel(writer, u'自由项', index=None)
        sheetNone.to_excel(writer, u'物料自由项档案', index=None)
        sheetNone.to_excel(writer, u'核算自由项档案', index=None)
        writer.save()

    #判断是否仓库编码这一列全为空，全为空则不生成excel
    num_null=inventoryDF[inventoryDF.loc[:,'warehouse_code'].isnull()].shape[0]
    num_all=inventoryDF.shape[0]
    if not inventoryDF.empty and num_null != num_all:

  
        inventoryControlPath = PROJECT_ROOT+u'\\download\\code\\' + fileName + u"--B 存货对照表" + u".xls"
        sheet20 = pd.DataFrame()
        sheet20[u'仓库编码'] = inventoryDF.ix[:, 'warehouse_code']
        sheet20[u'存货编码'] = inventoryDF.ix[:, 'recommend']
        writer2 = pd.ExcelWriter(inventoryControlPath)
        sheet20.to_excel(writer2, u'sheet1', index=None)
        sheetNone.to_excel(writer2, u'供应商', index=None)
        writer2.save()
    

#移除上一次产生的文件
def removeFile():
    dirPath=PROJECT_ROOT+'\\download\\code'
    if not os.path.isdir(dirPath):
        return
    files = os.listdir(dirPath)
    try:
        for file in files:
            filePath = os.path.join(dirPath, file)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif os.path.isdir(filePath):
                removeDir(filePath)
        # os.rmdir(dirPath)
    except :
        pass
