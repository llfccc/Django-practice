from django.contrib import admin

# Register your models here.

from stockCode.models import CodeTable,MaterialProperty,MeasurementUnit,Warehouse
#from wzb.models import NewUser as User
from django.contrib.auth.models import User

class CodeTableAdmin(admin.ModelAdmin):
    search_fields = ('id','applicant', 'material_name','model','U8code')
    list_display = ('id','application_time', 'applicant', 'material_name','U8code')
    list_filter = ('application_time','applicant')
    ordering = ('-id','application_time',)

class MaterialPropertyAdmin(admin.ModelAdmin):
    search_fields = ('material_category', 'scope','remark','attribute')
    list_display = ('material_category', 'scope', 'remark','attribute')
    list_filter = ('material_category',)
    ordering = ('material_category',)

class MeasurementUnitAdmin(admin.ModelAdmin):

    search_fields = ('accounts_set', 'measurement_unit','measurement_unit_code')
    list_display = ('accounts_set', 'measurement_unit', 'measurement_unit_code')
    list_filter = ('accounts_set',)
    ordering = ('accounts_set',)

class WarehouseAdmin(admin.ModelAdmin):
    search_fields = ('material_category', 'accounts_set','warehouse_code','category_chinese_name')
    list_display = ('material_category', 'accounts_set', 'warehouse_code','category_chinese_name')
    list_filter = ('material_category',)
    ordering = ('id','material_category','accounts_set',)

admin.site.register(CodeTable, CodeTableAdmin)
admin.site.register(MaterialProperty,MaterialPropertyAdmin)
admin.site.register(MeasurementUnit,MeasurementUnitAdmin)
admin.site.register(Warehouse,WarehouseAdmin)
# admin.site.register(User)
