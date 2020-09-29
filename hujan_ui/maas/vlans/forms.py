from django import forms
from hujan_ui import maas

class BaseVlanForm(forms.Form):
    fabric_id = forms.ChoiceField(required=True,label='Fabric',)
    space = forms.ChoiceField(required=False) 
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fabric_id'].choices = self.get_choice_fabric()
        self.fields['space'].choices = self.get_choice_space()

    def get_choice_fabric(self):
        fabrics = maas.get_fabrics()
        f = [(x['id'], x['name']) for x in fabrics]
        f.insert(0,(None, '-----'))
        return f

    def get_choice_space(self):
        space = maas.get_spaces()
        f = [(x['id'], x['name']) for x in space]
        f.insert(0,(None, '-----'))
        return f

class VlanForm(forms.Form):
    name = forms.CharField(required=True)
    vid = forms.CharField(required=True)
    fabric_id = forms.ChoiceField(required=True,label='Fabric',)
    space = forms.ChoiceField(required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fabric_id'].choices = self.get_choice_fabric()
        self.fields['space'].choices = self.get_choice_space()

    def get_choice_fabric(self):
        fabrics = maas.get_fabrics()
        f = [(x['id'], x['name']) for x in fabrics]
        f.insert(0,(None, '-----'))
        return f

    def get_choice_space(self):
        space = maas.get_spaces()
        f = [(x['id'], x['name']) for x in space]
        f.insert(0,(None, '-----'))
        return f


class VlanEditForm(BaseVlanForm):
    name = forms.CharField(required=False)
    vid = forms.CharField(required=True)
    mtu = forms.IntegerField(required=False)
    description = forms.TextInput()