
from django import forms


class CheckoutForm(forms.Form):
    full_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your full name",
            "class": "checkout-input",
        })
    )

    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your phone number",
            "class": "checkout-input",
        })
    )

    address = forms.CharField(
        widget=forms.Textarea(attrs={
            "placeholder": "Enter your full delivery address",
            "class": "checkout-input",
            "rows": 3,
        })
    )

    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your city",
            "class": "checkout-input",
        })
    )

    state = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your state",
            "class": "checkout-input",
        })
    )

    pincode = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your PIN code",
            "class": "checkout-input",
        })
    )

    payment_method = forms.ChoiceField(
        choices=[
            ("cod", "Cash on Delivery"),
        ],
        initial="cod",
        widget=forms.RadioSelect,
    )
