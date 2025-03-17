import debug_toolbar
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('shop/', include('shopapp.urls')),
    path('accounts/', include('myauth.urls')),
    # path('api/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema', name='schema-swagger')),
    # path('api/redoc/', SpectacularRedocView.as_view(), name='schema-redoc'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('blog/', include('blogapp.urls')),


    # Страницы ошибок
    path('404/', TemplateView.as_view(template_name="errors/404.html")),
    path('500/', TemplateView.as_view(template_name="errors/500.html")),
]

# Добавление маршрутов для статики и медиа в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
