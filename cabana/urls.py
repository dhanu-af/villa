from django.urls import path

from . import views

app_name = "cabana"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("rooms/", views.room_list, name="rooms"),
    path("rooms/<slug:slug>/", views.room_detail, name="room_detail"),
    path("gallery/", views.gallery, name="gallery"),
    path("amenities/", views.amenities, name="amenities"),
    path("things-to-do/", views.nearby, name="nearby"),
    path("rates/", views.rates, name="rates"),
    path("faq/", views.faq, name="faq"),
    path("contact/", views.contact, name="contact"),
    path("booking/", views.booking_create, name="booking"),
]
