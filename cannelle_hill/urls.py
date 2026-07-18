"""
URL configuration for the Cannelle Hill Cabanas project.

Routes admin, the sitemap/robots.txt (SEO), the `cabana` app's public pages,
and media file serving during local development.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from cabana.sitemaps import RoomSitemap, StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "rooms": RoomSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cabana.urls')),

    # SEO: sitemap.xml and robots.txt so search engines can crawl the site.
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
