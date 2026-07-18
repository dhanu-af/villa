from django import forms

from .models import Booking, ContactEnquiry


class BookingForm(forms.ModelForm):
    """Online booking request form shown on the Booking / Rooms pages."""

    class Meta:
        model = Booking
        fields = [
            "room", "full_name", "email", "phone",
            "check_in", "check_out", "adults", "children", "special_requests",
        ]
        widgets = {
            "room": forms.Select(attrs={"class": "form-select"}),
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your full name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+94 77 123 4567"}),
            "check_in": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "check_out": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "adults": forms.NumberInput(attrs={"class": "form-control", "min": 1}),
            "children": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "special_requests": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Anything we should know?"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        if check_in and check_out and check_out <= check_in:
            raise forms.ValidationError("Check-out date must be after the check-in date.")
        return cleaned_data


class ContactForm(forms.ModelForm):
    """General enquiry form shown on the Contact page."""

    class Meta:
        model = ContactEnquiry
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "+94 77 123 4567"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Subject"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "How can we help?"}),
        }
