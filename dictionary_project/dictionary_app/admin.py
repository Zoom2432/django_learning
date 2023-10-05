from django.contrib import admin
from .models import Dict

class DictAdmin(admin.ModelAdmin):
    readonly_fields = ('added',)

admin.site.register(Dict, DictAdmin)
