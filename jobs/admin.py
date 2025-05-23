from django.contrib import admin
from .models import Job, Application, Message

# Register your models here.
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(Message)
