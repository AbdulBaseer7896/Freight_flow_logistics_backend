from django.db import models

class CarrierData(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inActive', 'Inactive'),
    )
    MC = models.CharField(max_length=100, default="None")
    Email = models.CharField(max_length=255, default="None")
    Legal_Name = models.CharField(max_length=255, default="None")
    Phone = models.CharField(max_length=100, default="None")
    USDOT_Number = models.CharField(max_length=100, default="None")
    Physical_Address = models.TextField(default="None")
    plan = models.CharField(max_length=100, default="None", blank=True, null=True)
    signature = models.CharField(max_length=255, default="None", blank=True, null=True)
    
    MCAuthFile = models.FileField(upload_to='carriers/', null=True, blank=True)
    COLFile = models.FileField(upload_to='carriers/', null=True, blank=True)
    W9File = models.FileField(upload_to='carriers/', null=True, blank=True)
    NOVFile = models.FileField(upload_to='carriers/', null=True, blank=True)
    
    isActive = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Legal_Name
