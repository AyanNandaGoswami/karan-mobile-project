# django
from django import forms

# local import
from .models import InvoiceItems, InvoiceShipToDetail, Invoices


class InvoiceItemAdminForm(forms.ModelForm):
    class Meta:
        model = InvoiceItems
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('id'):
            if cleaned_data.get('product').stock_quantity <= 0:
                raise forms.ValidationError("The stock for %s is currently empty. Please restock this item." % cleaned_data.get('product'))
            if cleaned_data.get('quantity') <= 0:
                raise forms.ValidationError("Quantity is not valid for product %s" % cleaned_data.get('product'))

