from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('', RedirectView.as_view(url='/products/', permanent=True)),

    #APIs REST
    path('api/users/', include('users.api.urls')),
    path('api/products/', include('products.api.urls')),
    path('api/scraping/', include('scraping.api.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
