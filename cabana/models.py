from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class SiteSettings(models.Model):
    """
    Singleton-style model holding site-wide details (contact info, socials,
    map location) so they can be edited from the admin panel and are
    available in every template via cabana.context_processors.site_settings.
    """

    site_name = models.CharField(max_length=100, default="Cannelle Hill Cabanas")
    tagline = models.CharField(max_length=200, blank=True, default="A Peaceful Hillside Retreat")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    hero_image = models.ImageField(
        upload_to="site/", blank=True, null=True,
        help_text="Full-screen background photo shown on the homepage hero.",
    )
    about_summary = models.TextField(
        blank=True,
        help_text="Short paragraph shown in the homepage 'About' teaser section.",
    )
    hero_description = models.TextField(
        blank=True,
        help_text="Short description shown under the tagline on the homepage hero.",
    )

    google_rating = models.DecimalField(
        max_digits=2, decimal_places=1, blank=True, null=True,
        help_text="e.g. 5.0 — shown as a star rating badge.",
    )
    google_review_count = models.PositiveIntegerField(
        blank=True, null=True, help_text="Number of Google reviews backing the rating above.",
    )

    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    whatsapp_number = models.CharField(
        max_length=30, blank=True,
        help_text="Digits only with country code, e.g. 94771234567 (used for the WhatsApp chat button).",
    )
    email = models.EmailField(blank=True)

    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    tripadvisor_url = models.URLField(blank=True)

    google_maps_embed_url = models.URLField(
        blank=True,
        help_text="The 'src' URL from a Google Maps embed iframe.",
    )
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    meta_description = models.CharField(
        max_length=300, blank=True,
        help_text="Default SEO meta description used across the site.",
    )

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Enforce a single row so admins can't accidentally create duplicates.
        self.pk = 1
        super().save(*args, **kwargs)


class Amenity(models.Model):
    """A facility/amenity — either property-wide (Facilities & Amenities page) or a per-room feature."""

    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50, default="bi-check-circle",
        help_text="Bootstrap Icons class name, e.g. bi-wifi, bi-cup-hot, bi-water.",
    )
    description = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    show_on_amenities_page = models.BooleanField(
        default=True,
        help_text="Uncheck for room-only features (e.g. 'Electric Kettle') so they don't clutter the property-wide Facilities & Amenities page.",
    )

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Amenities"

    def __str__(self):
        return self.name


class Room(models.Model):
    """A room / cabana type that guests can book."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    main_image = models.ImageField(
        upload_to="rooms/", blank=True, null=True,
        help_text="Upload the main photo for this room. A placeholder is shown until one is added.",
    )
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.PositiveIntegerField(default=2)
    size_sqm = models.PositiveIntegerField(blank=True, null=True, help_text="Room size in square metres.")
    bed_type = models.CharField(max_length=100, blank=True, help_text="e.g. King Bed, Twin Beds.")
    amenities = models.ManyToManyField(Amenity, blank=True, related_name="rooms")
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class RoomImage(models.Model):
    """Extra gallery images for a specific room, uploaded from the admin."""

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="rooms/gallery/")
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.room.name} image #{self.pk}"


class GalleryCategory(models.Model):
    """Grouping for the site-wide photo gallery, e.g. Rooms, Grounds, Dining."""

    name = models.CharField(max_length=80, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Gallery Categories"

    def __str__(self):
        return self.name


class GalleryImage(models.Model):
    """A single photo shown on the Photo Gallery page."""

    category = models.ForeignKey(
        GalleryCategory, on_delete=models.SET_NULL, blank=True, null=True, related_name="images"
    )
    image = models.ImageField(upload_to="gallery/")
    caption = models.CharField(max_length=150, blank=True)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-uploaded_at"]

    def __str__(self):
        return self.caption or f"Gallery image #{self.pk}"


class NearbyAttraction(models.Model):
    """An attraction/activity shown on the Things to Do Nearby page."""

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    distance = models.CharField(max_length=50, blank=True, help_text="e.g. '3 km away' or '15 min drive'.")
    image = models.ImageField(upload_to="nearby/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Nearby Attractions"

    def __str__(self):
        return self.name


class SpecialOffer(models.Model):
    """A promotional rate/offer shown on the Rates & Special Offers page."""

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    discount_percent = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)], blank=True, null=True
    )
    image = models.ImageField(upload_to="offers/", blank=True, null=True)
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-valid_to"]

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    """A guest review shown in the Customer Reviews / Testimonials section."""

    guest_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, blank=True)
    rating = models.PositiveSmallIntegerField(
        default=5, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    photo = models.ImageField(upload_to="testimonials/", blank=True, null=True)
    is_approved = models.BooleanField(
        default=True, help_text="Uncheck to hide this review from the public site."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.guest_name} ({self.rating}★)"


class FAQ(models.Model):
    """A single question/answer pair for the FAQ page."""

    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class Booking(models.Model):
    """An online booking request submitted through the website."""

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED = "cancelled"
    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True, related_name="bookings")
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    check_in = models.DateField()
    check_out = models.DateField()
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.check_in} to {self.check_out}"


class ContactEnquiry(models.Model):
    """A general enquiry submitted through the Contact page form."""

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Contact Enquiries"

    def __str__(self):
        return f"{self.name} — {self.subject or 'Enquiry'}"
