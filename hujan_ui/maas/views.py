from django.shortcuts import redirect, render
from django.utils.translation import ugettext_lazy as _
from hujan_ui.maas.forms import ConfigMAASForm
from hujan_ui.installers.models import ConfigMAAS
import sweetify


def config_maas(request):
    config = ConfigMAAS.objects.first()
    form = ConfigMAASForm(request.POST or None, instance=config)
    if request.method == 'POST' and form.is_valid():
        form.save()
        sweetify.success(request, _('Config Successfully'), icon='success', button='OK', timer=3000)
        return redirect('maas:config_maas')

    context = {
        'title': _('Config MAAS'),
        'form': form
    }
    return render(request, 'maas/form.html', context)
