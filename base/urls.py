"""urlconf for the base application"""

from django.conf.urls import url, patterns


urlpatterns = patterns('base.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^generator$', 'code_generator', name='generator'),
                       url(r'^add_plant_code$', 'add_plant_code', name="add_plant_code"),
                       url(r'^add_plant/(?P<code>\w{0,10})$', 'add_plant', name="add_plant"),
                       url(r'^login_corredor$', 'login_corredor', name="login_corredor"),
                       )
