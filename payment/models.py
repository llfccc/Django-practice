#coding=utf-8
from __future__ import unicode_literals
from django.db import models


class RegistrationTable(models.Model):
    max_num = models.IntegerField(blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    company_name = models.CharField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    supplier_name = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    bank_of_deposit = models.CharField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    bank_account = models.CharField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    amount_in_figures = models.FloatField( blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    amount_in_words = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    record_date = models.DateField(blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    posting_date = models.DateField( blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    document_num = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    closing_date = models.CharField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    payment_date = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    expiring_date = models.DateField( blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    acceptance_bill = models.CharField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    cash = models.CharField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    cheque = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    transfer_finance = models.DateField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    payment_in_advance = models.CharField( max_length=255,blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    applicant=models.CharField( max_length=255,blank=True, null=True)
    deleted=models.CharField( max_length=255,blank=True, null=True)
    def __unicode__(self):
        return "{0}".format(self.max_num)


    class Meta:
        permissions = (
            ("query_payment", "查询付款单"),
            ("edit_payment", "修改付款单"),
        )


class SupplierPayment(models.Model):

    supplier_name = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'.
    company_name = models.CharField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    bank_of_deposit = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    closing_date = models.CharField(max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    bank_account = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    payment_date = models.CharField( max_length=255, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it started with '_'. Field renamed because it ended with '_'. Field renamed because of name conflict.
    # def __unicode__(self):
    #     return self.supplier_name

    class Meta:
        permissions = (
            ("query_supplier_payment", "查询付款单供应商"),
            ("edit_supplier_payment", "修改付款单供应商"),
        )
