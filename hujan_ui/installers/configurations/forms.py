from django import forms

from hujan_ui.installers.models import GlobalConfig, AdvancedConfig


class GlobalConfigForm(forms.ModelForm):

    class Meta:
        model = GlobalConfig
        fields = ('__all__')


class AdvancedConfigForm(forms.ModelForm):

    class Meta:
        model = AdvancedConfig
        fields = ('__all__')

    def __init__(self, *args, **kwargs):
        """
        to avoid redundan service type
        """
        super().__init__(*args, **kwargs)
        service_type = AdvancedConfig.SERVICE_TYPE
        services_used = AdvancedConfig.objects.all()
        if self.instance.id:
            services_used = services_used.exclude(id=self.instance.id)

        services_available = ((k, v) for k, v in service_type if k not in services_used.values_list('service_type', flat=True))
        self.fields['service_type'].choices = tuple(services_available)
        