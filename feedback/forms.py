from django import forms

from .models import ContactMessage

MIN_MESSAGE_LENGTH = 20


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Олександр", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "+380 …", "autocomplete": "tel"}),
            "subject": forms.TextInput(attrs={"placeholder": "Про що ви хочете написати?"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "Опишіть ваше питання…"}),
        }

    def clean_name(self) -> str:
        return self.cleaned_data["name"].strip()

    def clean_message(self) -> str:
        message = self.cleaned_data["message"].strip()
        if len(message) < MIN_MESSAGE_LENGTH:
            raise forms.ValidationError(
                f"Повідомлення має містити щонайменше {MIN_MESSAGE_LENGTH} символів."
            )
        return message
