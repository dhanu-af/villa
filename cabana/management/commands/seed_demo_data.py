from django.core.management.base import BaseCommand

from cabana.models import (
    FAQ,
    Amenity,
    GalleryCategory,
    NearbyAttraction,
    Room,
    SiteSettings,
    SpecialOffer,
    Testimonial,
)

# Attractions seeded in an earlier version of this command were for Ella,
# which is a different region of Sri Lanka from Deniyaya. Removed on cleanup
# so they don't linger for anyone who ran the command before this fix.
STALE_NEARBY_ATTRACTIONS = [
    "Nine Arch Bridge", "Little Adam's Peak", "Ella Rock",
    "Local Tea Factory Tour", "Ravana Falls",
]
# Fabricated named guest quotes from an earlier version — removed since they
# were never real reviews. The real 5.0/45 Google rating is stored on
# SiteSettings instead (google_rating / google_review_count).
STALE_TESTIMONIAL_NAMES = ["Amara Perera", "James Whitfield", "Sofia Rossi", "Daniel Kim"]
# Amenity names and special offers from an earlier, fabricated version of
# this command, superseded by the real amenities list / offer wording below.
STALE_AMENITY_NAMES = ["Swimming Pool", "Free Parking", "Airport Transfers", "Farm-to-Table Restaurant", "Spa & Wellness", "Eco-Friendly Design"]
STALE_SPECIAL_OFFER_TITLES = ["Early Bird Escape", "Stay 4, Pay 3"]

# Amenities/features shared by every room, per the property's real details.
ROOM_FEATURES = [
    "Private Bathroom", "Balcony or Terrace", "Mountain or Garden View", "Dining Area",
    "Electric Kettle", "Hair Dryer", "Complimentary Toiletries", "Fresh Towels",
    "Comfortable Bedding", "Seating Area",
]


class Command(BaseCommand):
    """
    Populates the database with the real Cannelle Hill Cabanas business
    details (site settings, amenities, room features, FAQs, offers).

    Room-specific names/descriptions/prices are still placeholders — update
    them from the admin dashboard at /admin/ once you have the real figures.
    """

    help = "Seed the database with Cannelle Hill Cabanas' real business details."

    def handle(self, *args, **options):
        self._cleanup_stale_entries()
        self._seed_site_settings()
        self._seed_amenities()
        self._seed_room_features()
        self._seed_gallery_categories()
        self._seed_special_offers()
        self._seed_faqs()
        self.stdout.write(self.style.SUCCESS("Business details seeded successfully."))

    def _cleanup_stale_entries(self):
        NearbyAttraction.objects.filter(name__in=STALE_NEARBY_ATTRACTIONS).delete()
        Testimonial.objects.filter(guest_name__in=STALE_TESTIMONIAL_NAMES).delete()
        Amenity.objects.filter(name__in=STALE_AMENITY_NAMES).delete()
        SpecialOffer.objects.filter(title__in=STALE_SPECIAL_OFFER_TITLES).delete()

    def _seed_site_settings(self):
        SiteSettings.objects.update_or_create(
            pk=1,
            defaults=dict(
                site_name="Cannelle Hill Cabanas",
                tagline="A Peaceful Hillside Retreat in Deniyaya",
                hero_description=(
                    "Escape to the peaceful hills of Deniyaya and experience a relaxing stay "
                    "surrounded by lush greenery. Cannelle Hill Cabanas offers comfortable "
                    "mountain-view accommodation, warm Sri Lankan hospitality, and easy access "
                    "to nature, making it an ideal destination for couples, families, and "
                    "adventure seekers."
                ),
                address="Hettikanda, Pallegama, Dombagoda Road, Deniyaya, Sri Lanka",
                phone="+94 77 784 6543",
                whatsapp_number="94777846543",
                google_rating=5.0,
                google_review_count=45,
                # Left blank intentionally — paste the real Google Maps embed
                # URL for this address in the admin dashboard.
                meta_description=(
                    "Cannelle Hill Cabanas is a peaceful hillside retreat in Deniyaya, Sri Lanka, "
                    "offering mountain-view cabanas, an outdoor pool, and easy access to the "
                    "Sinharaja rainforest region."
                ),
                about_summary=(
                    "Nestled in the scenic countryside of Deniyaya, Cannelle Hill Cabanas provides "
                    "a tranquil retreat with beautiful mountain and garden views. Whether you're "
                    "exploring the nearby rainforest, enjoying a relaxing swim, or simply unwinding "
                    "on your private balcony, every stay is designed to help you reconnect with "
                    "nature. Guests can also enjoy authentic local cuisine prepared with fresh "
                    "ingredients and friendly, personalized service."
                ),
            ),
        )

    def _seed_amenities(self):
        amenities = [
            ("Free Wi-Fi", "bi-wifi", ""),
            ("Outdoor Swimming Pool", "bi-water", ""),
            ("Free Private Parking", "bi-p-square", ""),
            ("Family Rooms", "bi-people", ""),
            ("Airport Transfer", "bi-airplane", ""),
            ("24-Hour Front Desk", "bi-bell", ""),
            ("Garden & Terrace", "bi-tree", ""),
            ("Room Service", "bi-bell-fill", ""),
            ("Hiking Activities", "bi-signpost-split", ""),
            ("Mountain & Garden Views", "bi-binoculars", ""),
            ("On-site Restaurant", "bi-cup-hot", ""),
            ("Daily Breakfast", "bi-egg-fried", ""),
            ("Balcony/Terrace", "bi-door-open", ""),
            ("Non-Smoking Rooms", "bi-slash-circle", ""),
        ]
        for i, (name, icon, desc) in enumerate(amenities):
            Amenity.objects.update_or_create(name=name, defaults={"icon": icon, "description": desc, "order": i})

    def _seed_room_features(self):
        # Shared per-room features, assigned to every existing room. Room
        # names/descriptions/prices themselves are left as placeholders for
        # you to fill in with the real figures from the admin dashboard.
        for i, name in enumerate(ROOM_FEATURES):
            Amenity.objects.update_or_create(
                name=name,
                defaults={"icon": "bi-check2-circle", "order": 100 + i, "show_on_amenities_page": False},
            )
        feature_qs = Amenity.objects.filter(name__in=ROOM_FEATURES)
        for room in Room.objects.all():
            room.amenities.add(*feature_qs)

    def _seed_gallery_categories(self):
        for i, name in enumerate(["Cabanas", "Grounds & Gardens", "Dining", "Pool & Wellness"]):
            GalleryCategory.objects.update_or_create(name=name, defaults={"order": i})

    def _seed_special_offers(self):
        SpecialOffer.objects.update_or_create(
            title="Book Direct or via Booking.com",
            defaults=dict(
                description="Reserve your stay directly with us or through Booking.com for the best available rates.",
                is_active=True,
                order=1,
            ),
        )

    def _seed_faqs(self):
        faqs = [
            ("Do you have Wi-Fi?", "Yes, complimentary Wi-Fi is available for guests."),
            ("Is breakfast included?", "Yes, a daily breakfast featuring authentic Sri Lankan cuisine is available."),
            ("Do you offer airport transfers?", "Yes, airport transfers can be arranged — contact us with your flight details."),
            ("Is Cannelle Hill Cabanas suitable for families?", "Yes, we offer family rooms and a peaceful, family-friendly setting."),
            ("What activities are nearby?", "Guests can enjoy hiking and easy access to the Sinharaja rainforest region, along with mountain and garden views from the property itself."),
            ("Do you have a swimming pool?", "Yes, we have an outdoor swimming pool on-site."),
        ]
        for i, (question, answer) in enumerate(faqs):
            FAQ.objects.update_or_create(question=question, defaults={"answer": answer, "order": i})
