""" Views for the base application """
from django.forms.models import ModelForm

from django.shortcuts import render, redirect, get_object_or_404
from base.models import Code, Plant
from base.forms import UserForm
from django.contrib.auth.models import User
import json
from django.contrib.auth import authenticate, login
from datetime import datetime
from django.utils.timezone import utc
#import pdb


def home(request):
    context = {}
    if request.user.is_authenticated():

        try:
            access = request.user.accountaccess_set.all()[0]
        except IndexError:
            access = None
            context['info'] = {"first_name": request.user.first_name, "last_name": request.user.last_name}
        else:
            client = access.api_client
            context['info'] = client.get_profile_info(raw_token=access.access_token)

    plants = Plant.objects.all()
    plant_dict = [{"lat": str(plant.lat), "lng": str(plant.lng),
                  "user_name": plant.user.first_name + " " + plant.user.last_name,
                  "date_joined": plant.user.date_joined.strftime("%d/%m/%y %H:%M"),
                  "days": (datetime.utcnow().replace(tzinfo=utc) - plant.user.date_joined).days} for plant in plants]

    context['plants'] = json.dumps(plant_dict)

    return render(request, 'base/home.html', context)


def code_generator(request):
    return render(request, 'code_generator.html')


def add_plant_code(request):
    if "code" in request.POST:
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
        if not request.user.is_authenticated():
            user = User(username=request.POST["email"])
            form_user = UserForm(request.POST, instance=user)

            if not form_user.is_valid():
                return render(request, 'add_plant.html', {"form": form, "form_user": form_user})

            user = form_user.save()
        else:
            user = request.user

        plant_dict = {"lat": request.POST["lat"], "lng": request.POST["lng"], "code": request.POST["code"], "user": user.pk}

        form = PlantForm(plant_dict)

        if not form.is_valid():
            return render(request, 'add_plant.html', {"form": form})

        form.save()

        return redirect('/')

    else:
        code = get_object_or_404(Code, code=code)
        form = PlantForm(initial={'code': code.pk})
        return render(request, 'add_plant.html', {"form": form})


def login_corredor(request):
    email = request.POST['inputEmail']
    password = request.POST['inputPassword']
    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect('home')
        else:
            return redirect('home')
    else:
        return redirect('home')
