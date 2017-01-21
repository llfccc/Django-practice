# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    chinese_name = models.CharField(max_length=100, unique=True,verbose_name='姓名')
    group_name = models.CharField(max_length=100, verbose_name='组别')
    title_name = models.CharField(max_length=100, verbose_name='级别')

    def __unicode__(self):
        return self.chinese_name
