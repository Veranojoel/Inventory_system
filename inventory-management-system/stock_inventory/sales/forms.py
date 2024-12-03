from django import forms
from .models import Product

class SalesTerminalForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())  # Hidden field to hold product ID
    quantity = forms.IntegerField(min_value=1, initial=1, label="Quantity")
