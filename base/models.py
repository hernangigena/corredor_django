""" Basic models, such as user profile """
from django.db import models


class Code(models.Model):

    def __unicode__(self):
        return self.code

    code = models.CharField(max_length=8)
    created_date = models.DateTimeField(auto_now_add=True)
