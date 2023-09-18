from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Contact)
admin.site.register(Frontend)
admin.site.register(Category)
admin.site.register(ParentHelp)
admin.site.register(News)

