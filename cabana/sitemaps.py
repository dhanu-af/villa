from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Room


class StaticViewSitemap(Sitemap):
    """SEO: lists every static page so search engines can discover them."""

    priority = 0.7
    changefreq = "weekly"

    def items(self):
        return [
            "cabana:home", "cabana:about", "cabana:rooms", "cabana:gallery",
            "cabana:amenities", "cabana:nearby", "cabana:rates", "cabana:faq",
            "cabana:contact", "cabana:booking",
        ]

    def location(self, item):
        return reverse(item)


class RoomSitemap(Sitemap):
    """SEO: lists every individual room detail page."""

    priority = 0.8
    changefreq = "weekly"

    def items(self):
        return Room.objects.filter(is_active=True)

    def location(self, obj):
        return reverse("cabana:room_detail", args=[obj.slug])
