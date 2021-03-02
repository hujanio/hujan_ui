from django import template

register = template.Library()


def sizify(value, suffix=""):
    """
    Simple kb/mb/gb size snippet for templates:
    {{ product.file.size|sizify }}
    """

    if value < 512000:
        value = value / 1024.0
        # ext = 'kb'
    elif value < 4194304000:
        value = value / 1048576.0
        # ext = 'mb'
    else:
        value = value / 1073741824.0
        # ext = 'gb'

    if suffix:
        return '%s %s' % (str(round(value, 2)), suffix)
    return str(round(value, 2))


def bool_icon(value):
    if value:
        return "<i class='fa fa-check-circle text-success'></i>"
    else:
        return "<i class='fa fa-times-circle text-danger'></i>"


register.filter('sizify', sizify)
register.filter('bool_icon', bool_icon)
