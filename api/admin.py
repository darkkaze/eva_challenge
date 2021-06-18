from django.contrib import admin

from .models import BodyPart, Patient, Study, Type

# Register your models here.
admin.site.register(Patient)
admin.site.register(BodyPart)
admin.site.register(Type)
admin.site.register(Study)
