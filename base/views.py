""" Views for the base application """
from django.forms.models import ModelForm

from django.shortcuts import render, redirect, get_object_or_404
from base.models import Code, Plant


def home(request):
    """ Default view for the root """
    return render(request, 'base/home.html')


def code_generator(request):
    return render(request, 'code_generator.html')


def add_plant_code(request):
    if request.POST.has_key("code"):
        return redirect('add_plant', code=request.POST["code"])
    else:
        return render(request, 'add_plant_code.html')


class PlantForm(ModelForm):
    class Meta:
        model = Plant


def add_plant(request, code=None):
    if request.POST:
        plant = Plant()
        form = PlantForm(request.POST, instance=plant)
        if form.is_valid():
            form.save()
        return redirect('home')

    else:
        code = get_object_or_404(Code, code=code)
        form = PlantForm(initial={'code': code.pk})
        return render(request, 'add_plant.html', {"form": form})
