from django.views.generic import TemplateView
from django.conf.urls import include, url
from django.contrib import admin

##########################################################################
## URL Patterns
##########################################################################

urlpatterns = [
    # Admin URLs
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Application URLs
    url(r'^$', TemplateView.as_view(template_name='site/home.html'), name='home'),

    # Authentication URLs
    # url('', include('social.apps.django_app.urls', namespace='social')),
    url('^accounts/', include('django.contrib.auth.urls')),
]
