# Handover — 2026-07-15 (continuing into later date per conversation)

## Goal
Build a complete, professional website for **Cannelle Hill Cabanas** (a real hillside eco-cabana property in Deniyaya, Sri Lanka) — modern luxury design, fully responsive, Django backend with admin dashboard for managing rooms/bookings/enquiries/gallery, SQLite (Postgres-ready), SEO-optimized. The user confirmed they are authorized to build this for the real business (owner/manager/rep).

## State
**Fully built and functional.** All 16 planned tasks are complete:
- Django 6.0.7 project scaffolded at `C:\Users\dnand\cannelle-hill-cabanas` (venv included, Django + Pillow installed)
- All models, admin, forms, views, URLs, templates for every requested page are written
- Migrations applied, database seeded, contact form + booking form tested end-to-end (save to DB + email notification via console backend)
- 12 real property photos (downloaded by the user from the property's Facebook page, with authorization) are wired into: homepage hero, all 3 room main images, 4 room detail images, 4 gallery images
- Real business details (address, phone, Google rating, amenities, hero copy, about copy) have been entered; fabricated placeholder content has been identified and either removed or explicitly flagged as still-placeholder

**Not yet done:** the user wants to fill in real room names/descriptions/prices, real nearby activities/distances, and the Google Maps embed URL "after" (deferred, not urgent).

**Access problem (unresolved, blocking user from viewing the site):** the Django dev server only runs inside this Claude Code session's sandbox. The user tried `http://localhost:8010/` from their own browser and got "another localhost" (i.e., not reaching this server — the sandbox's network is isolated from the user's actual browser, even though the filesystem appears to be the user's real machine, evidenced by real personal files in Downloads and real photos they'd just downloaded being immediately readable). Last thing told to the user: run it themselves —
```
cd C:\Users\dnand\cannelle-hill-cabanas
venv\Scripts\python.exe manage.py runserver
```
then open `http://127.0.0.1:8000/` in their own browser. **This has not yet been confirmed working by the user.**

## Key decisions
- **Refused to scrape Cannelle Hill Cabanas' Booking.com or Facebook listing directly.** User initially asked to copy "all details and pictures" from the real Booking.com listing for Cannelle Hill Cabanas. Declined because: (1) reusing another business's real photos without a verified license is copyright infringement even with claimed authorization, and (2) automated scraping violates Facebook/Booking.com ToS. Resolution: asked the user to download photos themselves (as the authorized rep) into a local folder and paste text details directly — this is how the real photos and business details entered the project.
- **Renamed project from "Daffodils Hill Cabana" to "Cannelle Hill Cabanas"** mid-build, including the Django project package folder (`daffodils_hill` → `cannelle_hill`), after confirming user authorization. Required updating `manage.py`, `wsgi.py`, `asgi.py`, `settings.py` (ROOT_URLCONF, WSGI_APPLICATION, DB name), model defaults, admin site header, and all view meta_titles.
- **Made `Room.main_image` optional** (`blank=True, null=True`) so rooms can be seeded/managed before real photos exist; templates fall back to hand-authored SVG placeholders (`static/images/placeholder-*.svg`) in earthy green/gold theme.
- **Split `Amenity` into property-wide vs. room-only** via a new `show_on_amenities_page` boolean field. Reason: the real "Room Features" list (Private Bathroom, Balcony or Terrace, etc.) the user provided overlapped/duplicated with property-wide amenities (Balcony/Terrace, Mountain & Garden Views) — showing both on the public Amenities page read as redundant. Room features are assigned to all rooms via M2M but hidden from the general Amenities page.
- **Removed fabricated content once real data arrived:** deleted 5 "nearby attractions" seeded from an earlier placeholder pass (Nine Arch Bridge, Little Adam's Peak, Ella Rock, tea factory tour, Ravana Falls) because those are landmarks near **Ella**, a different region from **Deniyaya** (the real property's location, and the actual gateway town to Sinharaja Forest Reserve) — keeping them would have been factually wrong, not just "generic placeholder." Also deleted 4 fabricated named guest testimonials and 2 fabricated discount offers; replaced with the real Google rating (5.0/45 reviews, stored as new `SiteSettings.google_rating` / `google_review_count` fields) shown as a badge on Home/About/Contact instead of inventing quotes.
- **Did not fabricate a Google Maps embed URL** — left blank intentionally rather than guessing coordinates, since presenting a wrong location as if verified would be misleading.
- **launch.json for the dev server lives at `C:\Users\dnand\.claude\launch.json`** (the root working directory), not inside the project folder — the preview tool reads launch.json from the session root, not per-project. Entry name: `"cannelle-hill-cabanas"`, runs `venv/Scripts/python.exe manage.py runserver 8010`.

## Files touched
Everything under `C:\Users\dnand\cannelle-hill-cabanas\` is new this session:
- `cannelle_hill/settings.py` — full config (env-var driven DEBUG/DB/email, GZip middleware, security headers, sitemap/sites framework)
- `cannelle_hill/urls.py` — includes cabana.urls, sitemap.xml, robots.txt, media serving in DEBUG
- `cabana/models.py` — `SiteSettings` (singleton, now includes `hero_description`, `google_rating`, `google_review_count`), `Amenity` (now has `show_on_amenities_page`), `Room`, `RoomImage`, `GalleryCategory`, `GalleryImage`, `NearbyAttraction`, `SpecialOffer`, `Testimonial`, `FAQ`, `Booking`, `ContactEnquiry`
- `cabana/admin.py` — full admin dashboard, custom site header, image thumbnails, booking/enquiry bulk actions
- `cabana/views.py`, `cabana/urls.py`, `cabana/forms.py`, `cabana/sitemaps.py`, `cabana/context_processors.py`, `cabana/templatetags/cabana_extras.py` (`times` filter for star ratings)
- `cabana/management/commands/seed_demo_data.py` — **this is the single source of truth for seed content**; already updated once with real business details and stale-data cleanup logic (deletes old wrong entries by name before reseeding). Room names/prices inside it are still placeholder ("Garden View Cabana" $95, "Hillside Deluxe Villa" $165, "Family Eco Cabana" $135) — update this file when real room data arrives, then rerun `manage.py seed_demo_data`.
- `templates/base.html` + `templates/cabana/*.html` — all 10 pages (home, about, rooms, room_detail, gallery, amenities, nearby, rates, contact, booking, faq) plus 3 email text templates
- `static/css/style.css` — earthy green/white/gold design system (CSS vars: `--chc-green-dark`, `--chc-gold`, etc.)
- `static/js/main.js` — navbar scroll behavior, gallery lightbox, booking date-range JS
- `static/images/placeholder-*.svg` — hand-authored fallback graphics
- `media/site/`, `media/rooms/`, `media/rooms/gallery/`, `media/gallery/` — the 12 real photos the user downloaded from Facebook, wired in via a one-off shell script (not a management command — if photos need reassigning, do it directly via `manage.py shell` using `File(open(path, 'rb'), name=...)` pattern, see conversation for the exact script)
- `requirements.txt`, `.gitignore` — present, no git repo initialized

## Gotchas / constraints learned
- **The `preview_screenshot` tool is broken/unreliable in this sandbox** — repeatedly returns a mis-scaled image (content squeezed into top-left ~35% of frame) even though DOM inspection (`preview_inspect`, `getBoundingClientRect`) confirms the actual page renders at full, correct viewport width with no overflow. Trust `preview_eval`/`preview_snapshot`/`preview_network`/DOM inspection over `preview_screenshot` for layout verification in this environment.
- **The venv broke after renaming the project folder** (`daffodils-hill-cabana` → `cannelle-hill-cabanas`): the `venv/Scripts/activate` script has the old absolute path baked in and fails with `ModuleNotFoundError: No module named 'django'` if sourced. Workaround: always invoke `./venv/Scripts/python.exe` directly instead of activating.
- **`launch.json` scope**: the Browser preview tool's `preview_start({name})` reads `.claude/launch.json` from the session's root working directory (`C:\Users\dnand\.claude\launch.json`), not a project-local `.claude/launch.json`. A project-local one was created by mistake first and had to be removed.
- **Django test client `Client()` fails with `DisallowedHost: testserver`** because `ALLOWED_HOSTS` is explicitly set to `localhost,127.0.0.1` (no default empty-list DEBUG bypass). For scripted form-submission tests, use real `curl` against the running dev server with a scraped CSRF token instead of Django's test `Client`.
- **The Django dev server process does not survive session/context resets** — it was found stopped (`preview_list` returned `[]`) partway through this conversation with no explicit stop command issued. Always check `preview_list` before assuming a previously-started server is still up.
- **Critical unresolved environment mismatch**: this session's Bash/sandbox network is isolated from the user's own browser, even though the filesystem is (apparently) the user's real machine. `localhost:8010` works via `curl` from Bash and via the Browser-pane tool, but the user's own browser cannot reach it. Root cause not fully diagnosed — see Next steps.

## Next steps
1. **Confirm whether the user's own `manage.py runserver` + `http://127.0.0.1:8000/` workaround succeeded.** This is the immediate blocker — the user cannot currently view the site at all through their own browser.
2. If that workaround fails too, that would mean the filesystem is *not* actually the user's literal machine (e.g., it's a synced/mirrored sandbox), and the real fix is deploying to a public host (Railway, Render, PythonAnywhere, Fly.io — NOT Vercel, since this is a stateful Django app with SQLite writes and media uploads that don't fit Vercel's serverless/ephemeral-disk model). User has not yet chosen a hosting provider or confirmed they want to proceed with a public deployment (which requires creating a third-party account — get explicit confirmation before doing this).
3. Once the user provides real room names/descriptions/prices and real nearby activities, update `cabana/management/commands/seed_demo_data.py` (add back `_seed_rooms` and `_seed_nearby_attractions` methods with real data, following the pattern already in the file) and rerun `manage.py seed_demo_data`.
4. Get the real Google Maps embed URL for `Hettikanda, Pallegama, Dombagoda Road, Deniyaya, Sri Lanka` from the user and set `SiteSettings.google_maps_embed_url` via admin.
5. Change the admin password from the placeholder (`admin` / `ChangeMe123!`) before this ever goes anywhere near production.

## Open questions
- Does the user want a public deployment, and if so, which host? (Asked once, user said "no preference" — needs a firmer decision or a recommendation to just proceed with.)
- Real room-specific data (names, descriptions, prices, bed types) — user said "after", not now.
- Real nearby activities/distances around Deniyaya — not yet provided.
- Google Maps embed URL — not yet provided.
