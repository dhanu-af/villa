from django.contrib import admin
from django.utils.html import format_html

from .models import (
    FAQ,
    Amenity,
    Booking,
    ContactEnquiry,
    GalleryCategory,
    GalleryImage,
    NearbyAttraction,
    Room,
    RoomImage,
    SiteSettings,
    SpecialOffer,
    Testimonial,
)

admin.site.site_header = "Cannelle Hill Cabanas — Admin"
admin.site.site_title = "Cannelle Hill Cabanas Admin"
admin.site.index_title = "Manage rooms, bookings, gallery and enquiries"


def thumb(obj, field="image", size=60):
    """Small helper to render an admin-list thumbnail for any ImageField."""
    image = getattr(obj, field, None)
    if not image:
        return "—"
    return format_html('<img src="{}" style="height:{}px;border-radius:4px;" />', image.url, size)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """Admins edit the single site-wide settings row here (contact, socials, map)."""

    fieldsets = (
        ("Branding", {"fields": ("site_name", "tagline", "logo", "hero_image", "hero_description", "about_summary")}),
        ("Google Rating", {"fields": ("google_rating", "google_review_count")}),
        ("Contact", {"fields": ("address", "phone", "whatsapp_number", "email")}),
        ("Social Media", {"fields": ("facebook_url", "instagram_url", "twitter_url", "youtube_url", "tripadvisor_url")}),
        ("Location / Map", {"fields": ("google_maps_embed_url", "latitude", "longitude")}),
        ("SEO", {"fields": ("meta_description",)}),
    )

    def has_add_permission(self, request):
        # Only one SiteSettings row should ever exist.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", "price_per_night", "max_guests", "is_active", "order")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("amenities",)
    inlines = [RoomImageInline]

    @admin.display(description="Preview")
    def image_preview(self, obj):
        return thumb(obj, "main_image")


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "show_on_amenities_page", "order")
    list_editable = ("order", "show_on_amenities_page")
    list_filter = ("show_on_amenities_page",)
    search_fields = ("name",)


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "caption", "category", "order", "uploaded_at")
    list_editable = ("order",)
    list_filter = ("category",)
    search_fields = ("caption",)

    @admin.display(description="Preview")
    def image_preview(self, obj):
        return thumb(obj)


@admin.register(NearbyAttraction)
class NearbyAttractionAdmin(admin.ModelAdmin):
    list_display = ("name", "distance", "order")
    list_editable = ("order",)
    search_fields = ("name",)


@admin.register(SpecialOffer)
class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "discount_percent", "valid_from", "valid_to", "is_active", "order")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("guest_name", "country", "rating", "is_approved", "created_at")
    list_editable = ("is_approved",)
    list_filter = ("is_approved", "rating")
    search_fields = ("guest_name", "comment")
    actions = ["approve_testimonials"]

    @admin.action(description="Approve selected testimonials")
    def approve_testimonials(self, request, queryset):
        queryset.update(is_approved=True)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)
    search_fields = ("question",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    """Booking management dashboard: filter by status/date, bulk-confirm requests."""

    list_display = ("full_name", "room", "check_in", "check_out", "adults", "children", "status", "created_at")
    list_filter = ("status", "room", "check_in")
    search_fields = ("full_name", "email", "phone")
    date_hierarchy = "check_in"
    list_editable = ("status",)
    actions = ["mark_confirmed", "mark_cancelled"]
    readonly_fields = ("created_at",)

    @admin.action(description="Mark selected bookings as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status=Booking.STATUS_CONFIRMED)

    @admin.action(description="Mark selected bookings as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status=Booking.STATUS_CANCELLED)


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    """Contact enquiry management dashboard: unread filter + mark-as-read action."""

    list_display = ("name", "email", "subject", "is_read", "created_at")
    list_filter = ("is_read",)
    search_fields = ("name", "email", "subject", "message")
    actions = ["mark_read"]
    readonly_fields = ("created_at",)

    @admin.action(description="Mark selected enquiries as read")
    def mark_read(self, request, queryset):
        queryset.update(is_read=True)
