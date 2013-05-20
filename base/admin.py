from django.contrib import admin
from base.models import Code
from django import forms
from datetime import datetime

from django.db.models import AutoField

#PDF Generation
from xhtml2pdf import pisa
import cStringIO as StringIO
import cgi
from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponse


def copy_model_instance(obj):
    initial = dict([(f.name, getattr(obj, f.name)) for f in obj._meta.fields if not isinstance(f, AutoField) and not f in obj._meta.parents.values()])
    return obj.__class__(**initial)


class CodeAdminForm(forms.ModelForm):
    class Meta:
        model = Code
        exclude = ('code',)

    quantity = forms.IntegerField(1000, 100, required=True)

    def save(self, commit=True, force_insert=False, force_update=False, *args, **kwargs):
        m = super(CodeAdminForm, self).save(commit=False, *args, **kwargs)
        m.code = self.generate_code()
        for i in range(int(self.visible_fields()[0].value()) - 1):
            m_new = copy_model_instance(m)
            m_new.code = self.generate_code()
            m_new.save()
        return m

    def generate_code(self):
        from random import sample
        import string

        code = ''.join(sample(string.ascii_letters + string.digits, 8))

        return code


def generar_pdf(html):
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('Error al generar el PDF: %s' % cgi.escape(html))


def print_codes(modeladmin, request, queryset):

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    codes = []
    for code in queryset:
        codes.append(code)

    html = render_to_string('codigos_pdf.html', {'pagesize': 'a4', 'codes': codes}, context_instance=RequestContext(request))
    print html
    response = generar_pdf(html)

    queryset.update(printed=True, printed_date=datetime.now())

    return response


print_codes.short_description = "Imprimir codigos"


class CodeAdmin(admin.ModelAdmin):
    form = CodeAdminForm
    list_display = ("code", "created_date", "available", "printed", "printed_date")
    actions = [print_codes]

    def changelist_view(self, request, extra_context=None):
        self.list_display_links = (None, )
        return super(CodeAdmin, self).changelist_view(request, extra_context=None)

    def available(self, obj):
        return "Si"


admin.site.register(Code, CodeAdmin)
