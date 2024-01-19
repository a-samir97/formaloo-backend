from django.contrib import admin
from .models import Application, PurchasedApplication

admin.site.register(Application)
admin.site.register(PurchasedApplication)
