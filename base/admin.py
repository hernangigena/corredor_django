from django.contrib import admin
from base.models import Code, Plant, UrlQRCode
from django import forms
from datetime import datetime

from django.db.models import AutoField
from django.core.exceptions import ValidationError

#QR Code Generation
from django.core.files import File
from django.core.files.base import ContentFile
 
from base.PyQRNative import QRCode, QRErrorCorrectLevel
 
import cStringIO as StringIO

#PDF Generation
from xhtml2pdf import pisa
from django.http import HttpResponse

from django.template.loader import get_template
from django.template.context import Context
from django.utils.html import escape

import os
from django.conf import settings


def copy_model_instance(obj):
    initial = dict([(f.name, getattr(obj, f.name)) for f in obj._meta.fields if not isinstance(f, AutoField) and not f in obj._meta.parents.values()])
    return obj.__class__(**initial)


class CodeAdminForm(forms.ModelForm):
    class Meta:
        model = Code
        exclude = ('code', 'printed', 'printed_date', 'qr_code')

    quantity = forms.IntegerField(1000, 100, required=True)

    def save(self, commit=True, force_insert=False, force_update=False, *args, **kwargs):
        m = super(CodeAdminForm, self).save(commit=False, *args, **kwargs)
        m.code = self.generate_code()
        m.qr_code = UrlQRCode(url="http://localhost:8000?code=" + m.code)
        self.generate_qr_code(m)
        m.qr_code.save()
        m.qr_code_id = m.qr_code.pk

        for i in range(int(self.visible_fields()[0].value()) - 1):
            m_new = copy_model_instance(m)
            m_new.code = self.generate_code()
            m_new.qr_code = UrlQRCode(url="http://localhost:8000?code=" + m_new.code)
            self.generate_qr_code(m_new)
            m_new.qr_code.save()
            m_new.qr_code_id = m_new.qr_code.pk
            m_new.save()
        return m

    def generate_code(self):
        from random import sample
        import string

        code = ''.join(sample(string.ascii_letters + string.digits, 8))

        return code

    def generate_qr_code(self, instance):
        qr = QRCode(4, QRErrorCorrectLevel.L)
        qr.addData(instance.qr_code.url)
        qr.make()
        image = qr.makeImage()
 
       #Save image to string buffer
        image_buffer = StringIO.StringIO()
        image.save(image_buffer, format='JPEG')
        image_buffer.seek(0)
 
       #Here we use django file storage system to save the image.
        file_name = 'UrlQR_%s.jpg' % instance.code
        file_object = File(image_buffer, file_name)
        content_file = ContentFile(file_object.read())
        instance.qr_code.qr_image.save(file_name, content_file, save=True)


#Print Codes

def fetch_resources(uri, rel):
    """
    Callback to allow xhtml2pdf/reportlab to retrieve Images,Stylesheets, etc.
    `uri` is the href attribute from the html link element.
    `rel` gives a relative path, but it's not used here.

    """
    if uri.startswith(settings.MEDIA_URL):
        path = os.path.join(settings.MEDIA_ROOT,
                            uri.replace(settings.MEDIA_URL, ""))
    elif uri.startswith(settings.STATIC_URL):
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))
    else:
        path = os.path.join(settings.STATIC_ROOT,
                            uri.replace(settings.STATIC_URL, ""))

        if not os.path.isfile(path):
            path = os.path.join(settings.MEDIA_ROOT,
                                uri.replace(settings.MEDIA_URL, ""))

            if not os.path.isfile(path):
                raise Exception('media urls must start with %s or %s' % (settings.MEDIA_ROOT, settings.STATIC_ROOT))

    return path


def render_to_pdf(template_src, context_dict):
    """Function to render html template into a pdf file"""
    template = get_template(template_src)
    context = Context(context_dict)
    html = template.render(context)
    print html
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")),
                            dest=result,
                            encoding='UTF-8',
                            link_callback=fetch_resources)
    if not pdf.err:
        response = HttpResponse(result.getvalue(), mimetype='application/pdf')

        return response

    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def print_codes(modeladmin, request, queryset):

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    codes = []
    for code in queryset:
        if not code.printed:
            codes.append(code)
        else:
            raise ValidationError("El codigo %s ya fue imprimido y no puede volver a ser utilizado" % code.code)

    response = render_to_pdf('codigos_pdf.html', {'pagesize': 'a4', 'codes': codes})

    queryset.update(printed=True, printed_date=datetime.now())

    return response


print_codes.short_description = "Imprimir codigos"


class CodeAdmin(admin.ModelAdmin):
    form = CodeAdminForm
    list_display = ("code", "created_date", "available", "printed", "printed_date")
    list_filter = ("printed",)
    actions = [print_codes]

    def changelist_view(self, request, extra_context=None):
        self.list_display_links = (None, )
        return super(CodeAdmin, self).changelist_view(request, extra_context=None)

    def available(self, obj):
        return "Si"


admin.site.register(Code, CodeAdmin)
admin.site.register(Plant)
