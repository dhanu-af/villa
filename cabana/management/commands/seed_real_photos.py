from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from cabana.models import GalleryCategory, GalleryImage, Room, RoomImage, SiteSettings

SOURCE_DIR = Path(settings.BASE_DIR) / "photo_assets"

HERO_IMAGE = "site/493028559_1257325396399724_1276988226606087605_n.jpg"

ROOM_MAIN_IMAGE = {
    "Garden View Cabana": "rooms/493534257_1257324679733129_7326307807188426400_n.jpg",
    "Hillside Deluxe Villa": "rooms/493531922_1257325326399731_4028510733461427977_n.jpg",
    "Family Eco Cabana": "rooms/493306490_1257325349733062_4921544270822885795_n.jpg",
}

ROOM_GALLERY_IMAGES = {
    "Garden View Cabana": [
        "rooms/gallery/493049537_1257325313066399_6496868266512484071_n.jpg",
        "rooms/gallery/492528353_1257325416399722_3803119207420148429_n.jpg",
    ],
    "Hillside Deluxe Villa": [
        "rooms/gallery/493219504_1257325369733060_5432467504304959566_n.jpg",
        "rooms/gallery/493662191_1257324673066463_7735865449443120055_n.jpg",
    ],
}

GALLERY_IMAGES = [
    ("gallery/492437599_1257325309733066_229633360357268477_n.jpg", "Grounds & Gardens", "Natural stream on the property"),
    ("gallery/492367171_1257324916399772_121313160714950317_n.jpg", "Cabanas", "Signature A-frame architecture"),
    ("gallery/492466169_1257325386399725_1594170384652343035_n.jpg", "Cabanas", "Private deck overlooking the valley"),
    ("gallery/492807996_1257325333066397_3673630018996784305_n.jpg", "Cabanas", "Solar-powered cabana"),
]


class Command(BaseCommand):
    help = (
        "Copies the real property photos bundled in photo_assets/ into MEDIA_ROOT "
        "and attaches them to the matching Room/SiteSettings/GalleryImage rows. "
        "Safe to rerun — skips anything already attached."
    )

    def handle(self, *args, **options):
        site = SiteSettings.objects.get_or_create(pk=1)[0]
        if not site.hero_image:
            self._attach(site, "hero_image", HERO_IMAGE)
            site.save()
            self.stdout.write("Set homepage hero image.")

        for name, rel_path in ROOM_MAIN_IMAGE.items():
            room = Room.objects.filter(name=name).first()
            if room and not room.main_image:
                self._attach(room, "main_image", rel_path)
                room.save()
                self.stdout.write(f"Set main image for '{name}'.")

        for name, rel_paths in ROOM_GALLERY_IMAGES.items():
            room = Room.objects.filter(name=name).first()
            if not room:
                continue
            for rel_path in rel_paths:
                filename = Path(rel_path).name
                if RoomImage.objects.filter(room=room, image__endswith=filename).exists():
                    continue
                ri = RoomImage(room=room)
                self._attach(ri, "image", rel_path)
                ri.save()
                self.stdout.write(f"Added room gallery image for '{name}'.")

        for rel_path, category_name, caption in GALLERY_IMAGES:
            filename = Path(rel_path).name
            if GalleryImage.objects.filter(image__endswith=filename).exists():
                continue
            category, _ = GalleryCategory.objects.get_or_create(name=category_name)
            gi = GalleryImage(category=category, caption=caption)
            self._attach(gi, "image", rel_path)
            gi.save()
            self.stdout.write(f"Added gallery image: {caption}.")

        self.stdout.write(self.style.SUCCESS("Real photos seeded successfully."))

    def _attach(self, instance, field_name, rel_path):
        source_path = SOURCE_DIR / rel_path
        with open(source_path, "rb") as f:
            getattr(instance, field_name).save(Path(rel_path).name, File(f), save=False)
