from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


API_PREFIX = 'api/v1'

urlpatterns = [

    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),
    path('currency/', include('currency.urls')),

    path('auth/', include('django.contrib.auth.urls')),

    path('', TemplateView.as_view(template_name='base.html'), name='index'),

    path(f'{API_PREFIX}/currency/', include('currency.api.urls')),
    path(f'{API_PREFIX}/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f'{API_PREFIX}/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]


schema_view = get_swagger_view(title='DOCS')

urlpatterns.append(path(f'{API_PREFIX}/docs/', schema_view))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
