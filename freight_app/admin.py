from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from freight_app.models import User, CarrierData, Contact, ContactForm, SiteSettings

admin.site.register(User, UserAdmin)
admin.site.register(CarrierData)
admin.site.register(Contact)
admin.site.register(ContactForm)
admin.site.register(SiteSettings)
