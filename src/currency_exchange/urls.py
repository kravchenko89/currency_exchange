from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('auth/', include('django.contrib.auth.urls')),

    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls))
                  ] + urlpatterns
