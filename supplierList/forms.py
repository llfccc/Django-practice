# coding=utf8
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from django.forms import ModelForm
from .models import SupplierList


class SupplierListForm(ModelForm):
    class Meta:
        model = SupplierList
        # fields = ['applicant','accounts_set','material_category','material_name','brand','model','unit','remark','demand_department','equipment_name','equipment_model','manufacturers']
        fields = "__all__"
