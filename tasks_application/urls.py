from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tasks.forms import InboxForm, TaskForm

urlpatterns = patterns('',
    (r'^inbox/insert/$','django.views.generic.create_update.create_object',{'form_class':InboxForm,'post_save_redirect':'/'}),
    (r'^process/update/(?P<object_id>\d+)/$','django.views.generic.create_update.update_object',{'form_class':TaskForm,'post_save_redirect':'/process/'}),
    (r'^$','tasks.views.index'),
    (r'^process/$','tasks.views.process'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
