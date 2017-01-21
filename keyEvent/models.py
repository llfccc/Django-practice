from __future__ import unicode_literals

from django.db import models

# Create your models here.

class KeyEvent(models.Model):
    supplier_name = models.CharField(max_length=255)
    material_name = models.CharField(max_length=255, blank=True, null=True)
    supplier_class = models.CharField(max_length=255, blank=True, null=True)
    belong_to = models.CharField(max_length=255, blank=True, null=True)
    recorder = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    record_date = models.DateField( blank=True, null=True)
    planed_date = models.DateField( blank=True, null=True)
    planed_quantity = models.CharField(max_length=255, blank=True, null=True)
    event_description = models.TextField(blank=True, null=True)
    quality_deduction = models.FloatField(blank=True, null=True)
    delay_batch = models.SmallIntegerField(blank=True, null=True)
    supply_deduction = models.FloatField(blank=True, null=True)
    warehouse_deduction = models.FloatField(blank=True, null=True)
    service_deduction = models.FloatField(blank=True, null=True)
    special_bonus_point = models.FloatField(blank=True, null=True)
    special_penalty_point = models.FloatField(blank=True, null=True)
    effective = models.CharField(max_length=255, blank=True, null=True)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        # db_table = 'keyevent'
        permissions = (
            ("query_keyEvent", "Can query KeyEvent"),
            ("add_new_keyEvent", "Can add new keyEvent"),

        )

