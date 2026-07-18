from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from .forms import BookingForm, ContactForm
from .models import (
    FAQ,
    Amenity,
    GalleryCategory,
    GalleryImage,
    NearbyAttraction,
    Room,
    SpecialOffer,
    Testimonial,
)


def _notify_new_booking(booking):
    """Email the property (and the guest) when a new booking request comes in."""
    admin_body = render_to_string("cabana/emails/booking_admin_notification.txt", {"booking": booking})
    send_mail(
        subject=f"New booking request from {booking.full_name}",
        message=admin_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.BOOKING_NOTIFICATION_EMAIL],
        fail_silently=True,
    )
    guest_body = render_to_string("cabana/emails/booking_guest_confirmation.txt", {"booking": booking})
    send_mail(
        subject="We received your booking request — Cannelle Hill Cabanas",
        message=guest_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[booking.email],
        fail_silently=True,
    )


def _notify_new_enquiry(enquiry):
    """Email the property when a new contact enquiry is submitted."""
    body = render_to_string("cabana/emails/enquiry_admin_notification.txt", {"enquiry": enquiry})
    send_mail(
        subject=f"New website enquiry: {enquiry.subject or 'General enquiry'}",
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.BOOKING_NOTIFICATION_EMAIL],
        fail_silently=True,
    )


def home(request):
    """Homepage: full-screen hero, teasers for about/rooms/amenities, testimonials, booking CTA."""
    rooms = Room.objects.filter(is_active=True)[:3]
    amenities = Amenity.objects.filter(show_on_amenities_page=True)[:6]
    testimonials = Testimonial.objects.filter(is_approved=True)[:6]
    offers = SpecialOffer.objects.filter(is_active=True)[:2]
    booking_form = BookingForm()
    return render(request, "cabana/home.html", {
        "rooms": rooms,
        "amenities": amenities,
        "testimonials": testimonials,
        "offers": offers,
        "booking_form": booking_form,
        "meta_title": "Cannelle Hill Cabanas | Peaceful Hillside Retreat in Deniyaya",
    })


def about(request):
    return render(request, "cabana/about.html", {
        "meta_title": "About Us | Cannelle Hill Cabanas",
    })


def room_list(request):
    rooms = Room.objects.filter(is_active=True)
    return render(request, "cabana/rooms.html", {
        "rooms": rooms,
        "meta_title": "Accommodation & Rooms | Cannelle Hill Cabanas",
    })


def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug, is_active=True)
    booking_form = BookingForm(initial={"room": room})
    return render(request, "cabana/room_detail.html", {
        "room": room,
        "booking_form": booking_form,
        "meta_title": f"{room.name} | Cannelle Hill Cabanas",
    })


def gallery(request):
    categories = GalleryCategory.objects.prefetch_related("images")
    uncategorised = GalleryImage.objects.filter(category__isnull=True)
    return render(request, "cabana/gallery.html", {
        "categories": categories,
        "uncategorised": uncategorised,
        "meta_title": "Photo Gallery | Cannelle Hill Cabanas",
    })


def amenities(request):
    amenity_list = Amenity.objects.filter(show_on_amenities_page=True)
    return render(request, "cabana/amenities.html", {
        "amenities": amenity_list,
        "meta_title": "Facilities & Amenities | Cannelle Hill Cabanas",
    })


def nearby(request):
    attractions = NearbyAttraction.objects.all()
    return render(request, "cabana/nearby.html", {
        "attractions": attractions,
        "meta_title": "Things to Do Nearby | Cannelle Hill Cabanas",
    })


def rates(request):
    rooms = Room.objects.filter(is_active=True)
    offers = SpecialOffer.objects.filter(is_active=True)
    return render(request, "cabana/rates.html", {
        "rooms": rooms,
        "offers": offers,
        "meta_title": "Rates & Special Offers | Cannelle Hill Cabanas",
    })


def faq(request):
    faqs = FAQ.objects.all()
    return render(request, "cabana/faq.html", {
        "faqs": faqs,
        "meta_title": "Frequently Asked Questions | Cannelle Hill Cabanas",
    })


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            _notify_new_enquiry(enquiry)
            messages.success(request, "Thank you! Your message has been sent — we'll reply shortly.")
            return redirect("cabana:contact")
    else:
        form = ContactForm()
    return render(request, "cabana/contact.html", {
        "form": form,
        "meta_title": "Contact Us | Cannelle Hill Cabanas",
    })


def booking_create(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            _notify_new_booking(booking)
            messages.success(
                request,
                "Thank you! Your booking request has been received. "
                "Our team will confirm availability by email shortly.",
            )
            return redirect("cabana:booking")
    else:
        # Pre-fill from the homepage quick-search bar (check_in/check_out/adults/children query params).
        initial = {k: v for k, v in request.GET.items() if k in {"check_in", "check_out", "adults", "children"}}
        form = BookingForm(initial=initial)
    rooms = Room.objects.filter(is_active=True)
    return render(request, "cabana/booking.html", {
        "form": form,
        "rooms": rooms,
        "meta_title": "Book Now | Cannelle Hill Cabanas",
    })
