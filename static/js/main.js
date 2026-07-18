// Cannelle Hill Cabanas — small progressive-enhancement behaviors.
// No frameworks: plain JS kept minimal for fast page loads.

document.addEventListener("DOMContentLoaded", function () {
  // Shrink the navbar background once the page is scrolled, for a cleaner
  // full-screen hero effect on the homepage.
  var navbar = document.querySelector(".chc-navbar");
  if (navbar) {
    var onScroll = function () {
      navbar.classList.toggle("scrolled", window.scrollY > 40);
    };
    window.addEventListener("scroll", onScroll);
    onScroll();
  }

  // Auto-dismiss Django messages (success/error alerts) after a few seconds.
  document.querySelectorAll(".alert-dismissible").forEach(function (alertEl) {
    setTimeout(function () {
      var alert = bootstrap.Alert.getOrCreateInstance(alertEl);
      alert.close();
    }, 6000);
  });

  // Simple lightbox for the photo gallery: clicking a thumbnail opens it
  // full-size in a Bootstrap modal (#chcLightboxModal).
  var lightboxModalEl = document.getElementById("chcLightboxModal");
  if (lightboxModalEl) {
    var lightboxImg = lightboxModalEl.querySelector("img");
    var lightboxCaption = lightboxModalEl.querySelector(".chc-lightbox-caption");
    var lightboxModal = new bootstrap.Modal(lightboxModalEl);
    document.querySelectorAll("[data-lightbox-src]").forEach(function (thumb) {
      thumb.addEventListener("click", function () {
        lightboxImg.src = thumb.getAttribute("data-lightbox-src");
        lightboxCaption.textContent = thumb.getAttribute("data-lightbox-caption") || "";
        lightboxModal.show();
      });
    });
  }

  // Enforce that the booking form's check-out date can't be before check-in.
  var checkIn = document.querySelector("#id_check_in");
  var checkOut = document.querySelector("#id_check_out");
  if (checkIn && checkOut) {
    var syncMinCheckout = function () {
      if (checkIn.value) {
        checkOut.min = checkIn.value;
      }
    };
    checkIn.addEventListener("change", syncMinCheckout);
    syncMinCheckout();
  }
});
