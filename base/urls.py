"""urlconf for the base application"""

from django.conf.urls import url, patterns, include

urlpatterns = patterns('base.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^add_plant_code$', 'add_plant_code', name="add_plant_code"),
                       url(r'^add_plant/(?P<code>\w{0,10})$', 'add_plant', name="add_plant"),
                       url(r'^login_corredor$', 'login_corredor', name="login_corredor"),
                       url(r'^admin/util/taggit_autocomplete_modified/', include('taggit_autocomplete_modified.urls')),
                       url(r'^blog/', include('fluent_blogs.urls')),
                       url(r'^blog/comments/', include('fluent_comments.urls')),
                       )
