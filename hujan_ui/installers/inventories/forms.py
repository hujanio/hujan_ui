from django import forms
from hujan_ui.installers.models import Inventory


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('__all__')
