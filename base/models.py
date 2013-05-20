""" Basic models, such as user profile """
from django.db import models


class Code(models.Model):

    def __unicode__(self):
        return self.code

    code = models.CharField(max_length=8, unique=True)
    printed = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True)
    printed_date = models.DateTimeField(null=True)
