from django.contrib import admin
from base.models import Code
from django import forms


class CodeAdminForm(forms.ModelForm):
    class Meta:
        model = Code

    quantity = forms.IntegerField(1000, 100, required=True)
    

class CodeAdmin(admin.ModelAdmin):
    form = CodeAdminForm

admin.site.register(Code, CodeAdmin)
