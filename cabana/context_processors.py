from .models import SiteSettings


def site_settings(request):
    """Expose the singleton SiteSettings row to every template as `site`."""
    settings_obj, _ = SiteSettings.objects.get_or_create(pk=1)
    return {"site": settings_obj}
