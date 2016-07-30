from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'NepMart.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/users/', include("account.api.urls", namespace='users-api')),
    url(r'^api/merchants/', include("merchants.api.urls", namespace='merchants-api')),
    url(r'^api/stores/', include("stores.api.urls", namespace='stores-api')),
)
