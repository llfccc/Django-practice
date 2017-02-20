from django.contrib import admin
from .models import RegistrationTable,SupplierPayment
# Register your models here.
class RegistrationTableAdmin(admin.ModelAdmin):
    search_fields = ('id','max_num', 'applicant','company_name','supplier_name')
    list_display = ('id','record_date', 'applicant', 'company_name','supplier_name')
    list_filter = ('company_name',)
    ordering = ('record_date',)

# class SupplierPaymentAdmin(admin.ModelAdmin):
#     search_fields = ('id','applicant', 'material_name','model','U8code')
#     list_display = ('id','application_time', 'applicant', 'material_name','U8code')
#     list_filter = ('application_time',)
#     ordering = ('application_time',)


admin.site.register(RegistrationTable,RegistrationTableAdmin)
# admin.site.register(SupplierPayment,SupplierPaymentAdmin)