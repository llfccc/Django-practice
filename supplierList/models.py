from __future__ import unicode_literals

from django.db import models

# Create your models here.
class SupplierList(models.Model):
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    archive_class = models.CharField(max_length=255, blank=True, null=True)
    archive_id = models.CharField(max_length=255, blank=True, null=True)
    review_document_id = models.CharField(max_length=255, blank=True, null=True)
    material_name = models.CharField(max_length=255, blank=True, null=True)
    supplier_class = models.CharField(max_length=255, blank=True, null=True)
    review_class = models.CharField(max_length=255, blank=True, null=True)
    starting_date = models.DateField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    review_result = models.CharField(max_length=255, blank=True, null=True)
    application_date = models.DateField(blank=True, null=True)
    review_table_situation = models.TextField(blank=True, null=True)
    delay_reason = models.CharField(max_length=255, blank=True, null=True)
    review_remark = models.CharField(max_length=255, blank=True, null=True)
    province = models.CharField(max_length=255, blank=True, null=True)
    whether_cooperation = models.CharField(max_length=255, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    artificial_person = models.CharField(max_length=255, blank=True, null=True)
    business_license_id = models.CharField(max_length=255, blank=True, null=True)
    business_license_period = models.DateField(blank=True, null=True)
    business_license_confirmation = models.CharField(max_length=255, blank=True, null=True)
    registered_capital = models.CharField(max_length=255, blank=True, null=True)
    other_remark = models.CharField(max_length=255, blank=True, null=True)
    certificate_remark = models.CharField(max_length=255, blank=True, null=True)
    company_contact = models.CharField(max_length=255, blank=True, null=True)
    contact_information = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    contact_1 = models.CharField(max_length=255, blank=True, null=True)
    contact_position_1 = models.CharField(max_length=255, blank=True, null=True)
    contact_telephone_1 = models.CharField(max_length=255, blank=True, null=True)
    contact_2 = models.CharField(max_length=255, blank=True, null=True)
    contact_position_2 = models.CharField(max_length=255, blank=True, null=True)
    contact_telephone_2 = models.CharField(max_length=255, blank=True, null=True)
    contact_3 = models.CharField(max_length=255, blank=True, null=True)
    contact_position_3 = models.CharField(max_length=255, blank=True, null=True)
    contact_telephone_3 = models.CharField(max_length=255, blank=True, null=True)
    qq = models.CharField(max_length=255, blank=True, null=True)  # Field name made lowercase.
    contact_remark = models.CharField(max_length=255, blank=True, null=True)
    annual = models.CharField(max_length=255, blank=True, null=True)
    position_abbr = models.CharField(max_length=255, blank=True, null=True)
    qichacha = models.IntegerField(blank=True, null=True)
    qichacha_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.supplier_name

    class Meta:
        managed = True
        db_table = 'supplierlist_supplier_list'
        permissions = (
            ("query_supplier", "Can query supplier"),
            ("add_new_supplier", "Can add new supplier"),
            ("show_document", "Can show document"),
            ("update_all_supplier", "can update all supplier"),
            ("update_contract", "Can update contract"),
        )

class OptionalSupplierList(models.Model):
    file_location = models.CharField(max_length=255, blank=True, null=True)
    record_date = models.DateField(blank=True, null=True)
    supplier_class = models.CharField(max_length=255, blank=True, null=True)
    material_name = models.CharField(max_length=255, blank=True, null=True)
    supplier_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    landline = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.supplier_name

    class Meta:
        managed = True
        db_table = 'supplierlist_optional_supplier'
        permissions = (
            ("query_optional_supplier", "Can query optional supplier"),
            ("add_new_optional_supplier", "Can add new optional supplier"),
            ("update_all_optional_supplier", "can update all optional supplier"),
        )
