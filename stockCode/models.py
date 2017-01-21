# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class CodeTable(models.Model):
    user = models.ForeignKey(User, related_name='user')
    group_name = models.CharField(
        max_length=30, blank=True, null=True, verbose_name=u'组别')

    # uploader = models.CharField(max_length=100, null=True, verbose_name=u'上传人')
    applicant = models.CharField(max_length=100, verbose_name=u'申请人')
    application_time = models.DateTimeField(null=True, verbose_name=u'申请时间')
    accounts_set = models.CharField(max_length=100, verbose_name=u'账套')
    material_category = models.CharField(max_length=100, verbose_name=u'物资类别')
    material_name = models.CharField(max_length=100, verbose_name=u'物资名称')
    brand = models.CharField(max_length=30, blank=True,null=True, verbose_name=u'品牌')
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'备注')
    serial_number = models.CharField(max_length=100, blank=True,null=True, verbose_name=u'货号')
    model = models.CharField(max_length=100, null=True, verbose_name=u'规格型号')
    unit = models.CharField(max_length=100, null=True,  verbose_name=u'计量单位')
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'备注')
    number = models.CharField(max_length=100, null=True, verbose_name=u'数量')
    remark = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'备注')

    grade = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'等级')
    vender = models.CharField(max_length=500, blank=True, null=True, verbose_name=u'厂家')

    demand_department = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'需求部门')
    equipment_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'设备名称')
    equipment_model = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'设备型号')
    manufacturers = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'设备供应商')

    varified = models.IntegerField(
        blank=True, null=True, verbose_name=u'是否审核',default=0)
    varified_time = models.DateTimeField(
        blank=True, null=True, verbose_name=u'审核时间')
    varified_user_id = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'审核人')
    U8code = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'U8编号')

    add_code_time = models.DateTimeField(
        blank=True, null=True, verbose_name=u'添加编码时间')
    add_code_time_username = models.CharField(
        max_length=100, blank=True, null=True, verbose_name=u'编码员')

    add_completed = models.IntegerField(
         blank=True, null=True, verbose_name=u'是否添加完',default=0)
    def __unicode__(self):
        return self.material_name

    class Meta:
        permissions = (
            ("varify_application", "审核新增编码申请"),
            ("change_application", "变更编码申请"),
            ("edit_u8code", "修改U8编号"),

            # ("add_code", "Can add U8code"),
        )


class MaterialProperty(models.Model):
    material_category = models.CharField(primary_key=True, max_length=255)
    storagearea = models.FloatField(db_column='storageArea', blank=True, null=True)  # Field name made lowercase.
    scope = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)
    attribute = models.CharField(max_length=255, blank=True, null=True)
    domestic = models.IntegerField(blank=True, null=True)
    purchase = models.IntegerField(blank=True, null=True)
    import_field = models.IntegerField(db_column='import', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    productionconsumption = models.IntegerField(db_column='productionConsumption', blank=True, null=True)  # Field name made lowercase.
    manufacturing = models.IntegerField(blank=True, null=True)


class MeasurementUnit(models.Model):
    measurement_unit=models.CharField(max_length=255)
    measurement_unit_group_code= models.CharField(max_length=255)
    measurement_unit_code= models.CharField( max_length=255)
    accounts_set= models.CharField( max_length=255)
    def __unicode__(self):
        return self.measurement_unit

class Warehouse(models.Model):
    material_category=models.CharField(max_length=255)
    accounts_set= models.CharField(max_length=255)
    warehouse_code= models.CharField( max_length=255)
    category_chinese_name = models.CharField(max_length=255)
    def __unicode__(self):
        return self.category_chinese_name

class FileModel(models.Model):
    title = models.CharField(max_length=30)
    file = models.FileField(upload_to='./upload/')

    def __unicode__(self):
        return self.title
