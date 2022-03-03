# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.contrib.auth.models import User

#tp = FileSystemStorage(location='/media/topup')
#os = FileSystemStorage(location='/media/ocs')

# Create your models here.
class Logs(models.Model):

    id = models.BigAutoField(primary_key=True)
    date_time = models.DateTimeField()
    process = models.IntegerField()
    message_description = models.CharField(max_length=255)
    etat = models.CharField(max_length=255)

class Queue(models.Model):

    id = models.BigAutoField(primary_key=True)
    id_queue = models.IntegerField()
    action_type = models.IntegerField(null=True)
    command_content = models.CharField(max_length=255,null=True)
    created_date = models.DateTimeField()
    status = models.IntegerField(null=True)
    updated_date = models.DateTimeField()
    msisdn = models.CharField(max_length=255)
    pincode = models.CharField(max_length=255,null=True)
    error_code = models.IntegerField(null=True)
    error_description = models.CharField(max_length=255,null=True)
    etat = models.CharField(max_length=255,null=True)
    thread_name = models.CharField(max_length=255,null=True)
    thread_number = models.IntegerField(null=True)
    fee = models.DecimalField(max_digits=25,decimal_places=10,null=True)
    ip_adresse_client = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255,null=True)

class QueueHist(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    id_queue_hist = models.IntegerField()
    action_type = models.IntegerField(null=True)
    command_content = models.CharField(max_length=255,null=True)
    created_date = models.DateTimeField()
    status = models.IntegerField(null=True)
    updated_date = models.DateTimeField()
    error_description = models.CharField(max_length=255,null=True)
    msisdn = models.CharField(max_length=255,null=True)
    pincode = models.CharField(max_length=255,null=True)
    error_code = models.IntegerField(null=True)
    etat = models.CharField(max_length=255,null=True)
    thread_name = models.CharField(max_length=255,null=True)
    thread_number = models.IntegerField(null=True)
    fee = models.DecimalField(max_digits=25,decimal_places=10,null=True)
    ip_adresse_client = models.CharField(max_length=255,null=True)
    username = models.CharField(max_length=255,null=True)

class PackageData(models.Model):

    id = models.BigAutoField(primary_key=True)
    id_package_date = models.IntegerField()
    balance_data = models.CharField(max_length=255,null=True)
    code = models.CharField(max_length=255)
    created_date = models.DateTimeField()
    frais = models.IntegerField()
    promotion1 = models.CharField(max_length=255,null=True)
    promotion1_data = models.CharField(max_length=255,null=True)
    promotion2 = models.CharField(max_length=255,null=True)
    promotion2_data = models.CharField(max_length=255,null=True)
    promotion3 = models.CharField(max_length=255,null=True)
    promotion3_data = models.CharField(max_length=255,null=True)
    promotion4 = models.CharField(max_length=255,null=True)
    promotion4_data = models.CharField(max_length=255,null=True)
    promotion5 = models.CharField(max_length=255,null=True)
    promotion5_data = models.CharField(max_length=255,null=True)
    quantite_data = models.CharField(max_length=255)
    updated_date = models.DateTimeField()
    validite = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    balance_voix = models.CharField(max_length=255,null=True)
    quantite_voix = models.CharField(max_length=255,null=True)
    types = models.IntegerField()
    fraisrg = models.IntegerField()

class AlertQueue(models.Model):

    id = models.BigAutoField(primary_key=True)
    check_1 = models.BooleanField(default=False)
    check_2 = models.BooleanField(default=False)
    check_3 = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    corrected = models.BooleanField(default=False)
    id_queue = models.ForeignKey(Queue, on_delete=models.CASCADE)

class AlertQueueHist(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    check_1 = models.BooleanField(default=False)
    check_2 = models.BooleanField(default=False)
    check_3 = models.BooleanField(default=False)
    reported = models.BooleanField(default=False)
    corrected = models.BooleanField(default=False)
    id_queue_hist = models.ForeignKey(QueueHist, on_delete=models.CASCADE)

class AlertConfig(models.Model):

    id = models.BigAutoField(primary_key=True)
    params = models.CharField(max_length=255)
    values = models.CharField(max_length=255)

#class HEALTHCHECK(models.Model):

    #id = models.BigAutoField(primary_key=True)
    #date = models.DateTimeField(auto_now=True)
    #topup = models.FileField(storage=tp)
    #ocs_aaa_dpi = models.FileField(storage=os,blank=True)