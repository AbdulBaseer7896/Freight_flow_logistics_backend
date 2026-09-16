from django.db import models

class Contact(models.Model):
    fullName = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=50)
    email = models.EmailField()
    companyName = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullName

class ContactForm(models.Model):
    REGISTER_CHOICES = (
        ('Sole Proprietor', 'Sole Proprietor'),
        ('Partnership', 'Partnership'),
        ('None', 'None'),
    )
    fullName = models.CharField(max_length=255, default="None")
    phoneNumber = models.CharField(max_length=50, default="None")
    email = models.CharField(max_length=255, default="None")
    companyName = models.CharField(max_length=255, default="None")
    register = models.CharField(max_length=50, choices=REGISTER_CHOICES, default="None")
    message = models.TextField(default="None")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.fullName
