from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings

urlpatterns = patterns('',
    #~ (r'^/accounts/login/','tasks.views.login_view',{}),
    #~ (r'^/accounts/logout/$','tasks.views.logout_view',{}),
    
    (r'^$','tasks.views.index',{},'tasks_home'),
    (r'^tasks/', include("tasks.urls")),
    
    (r'^accounts/login/$', 'django.contrib.auth.views.login',{},'accounts_login'),
    (r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page':settings.HOME_URL},'accounts_logout'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',{
    'document_root': settings.RUTA_BASE+'/static'
    },'static')
)
