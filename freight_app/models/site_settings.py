from django.db import models

class SiteSettings(models.Model):
    phone = models.CharField(max_length=50, default="210-201-6321")
    email = models.EmailField(default="dispatch@freightflowsolutions.co")
    address = models.TextField(default="100 Lorenz Rd, San Antonio, TX 78209")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"
