from django.contrib import admin

# Register your models here.
from ColdStorage.models import *

admin.site.register(UserProfile)
admin.site.register(ColdStorage)
admin.site.register(ApplicationForm)