""" Basic models, such as user profile """
from django.db import models


class UrlQRCode(models.Model):
    url = models.URLField()
    qr_image = models.ImageField(
        upload_to="qr_codes/url/",
        height_field="qr_image_height",
        width_field="qr_image_width",
        null=True,
        blank=True,
        editable=False
    )
    qr_image_height = models.PositiveIntegerField(null=True, blank=True, editable=False)
    qr_image_width = models.PositiveIntegerField(null=True, blank=True, editable=False)

    def qr_code(self):
        return '%s' % self.qr_image.url
    qr_code.allow_tags = True


class Code(models.Model):

    def __unicode__(self):
        return self.code

    code = models.CharField(max_length=8, unique=True)
    printed = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    printed_date = models.DateTimeField(null=True)
    qr_code = models.ForeignKey('UrlQRCode', null=True)

class Plant(models.Model):
    code = models.OneToOneField(Code)
    lat = models.DecimalField(max_digits=20, decimal_places=17)
    lng = models.DecimalField(max_digits=20, decimal_places=17)

    def __unicode__(self):
        return unicode(self.code)
