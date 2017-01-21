from django.contrib import admin
from supplierList.models import SupplierList
# Register your models here.
class SupplierListAdmin(admin.ModelAdmin):
    search_fields = ('supplier_name', 'material_name','supplier_class')
    list_display = ('id','supplier_name', 'material_name','supplier_class')
    list_filter = ('supplier_class',)
    ordering = ('id',)

admin.site.register(SupplierList, SupplierListAdmin)
