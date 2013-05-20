""" Views for the base application """

from django.shortcuts import render
from base.models import Code


def home(request):
    """ Default view for the root """
    return render(request, 'base/home.html')


def code_generator(request):
    return render(request, 'code_generator.html')
