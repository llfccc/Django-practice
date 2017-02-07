# coding=utf8
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponse
from django.forms import ModelForm



class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50, required=False)
    file = forms.FileField(required=True, label='文件')
    #randomInt=forms.CharField(required=True, label='验证码')


