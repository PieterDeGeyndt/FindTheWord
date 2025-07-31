
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from ftwapp.sitemaps import CategorySitemap, SubcategorySitemap, WordSitemap

sitemaps = {
    'categories': CategorySitemap,
    'subcategories': SubcategorySitemap,
    'words': WordSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ftwapp.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('nested_admin/', include('nested_admin.urls')),  # required for JS/CSS
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

