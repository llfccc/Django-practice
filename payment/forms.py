# coding=utf8
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from django.forms import ModelForm



class UploadFileForm(forms.Form):
    company_name = forms.CharField(max_length=50, required=False)
    file = forms.FileField(required=True, label='文件')
    #randomInt=forms.CharField(required=True, label='验证码')


class ApplicantForm(forms.Form):
    supplier_name = forms.CharField(label='供应商名称')
    company_name = forms.CharField(label='公司名称')
    document_num = forms.CharField(label='发票号')
    amount_in_figures = forms.FloatField(required=False,label='金额')
    # serial_number = forms.CharField(max_length=100 ,required=False,label='货号')

    # model = forms.CharField(max_length=100 ,required=False,label='规格型号')
    # unit = forms.CharField(max_length=100 ,label='计量单位')
    # number = forms.CharField(max_length=100 ,required=False,label='数量')
    # remark = forms.CharField(max_length=100 ,required=False,label='备注')
    # demand_department = forms.CharField(max_length=100 ,required=False,label='需求部门')
    # equipment_name = forms.CharField(max_length=100 ,required=False,label='设备名称')
    # equipment_model = forms.CharField(max_length=100 ,required=False,label='设备型号')
    # manufacturers = forms.CharField(max_length=100 ,required=False,label='设备供应商')
    # grade = forms.CharField(max_length=100 ,required=False,label='等级')
    # vender = forms.CharField(max_length=100 ,required=False,label='厂家')
