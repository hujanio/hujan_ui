# Generated by Django 2.2.10 on 2020-05-04 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('installers', '0004_auto_20200424_0409'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_type', models.CharField(choices=[('octavia_service', 'Octavia Service'), ('neutron_service', 'Neutron Service'), ('ml2_plugin', 'ML2 Plugin'), ('heat_service', 'Heat Service'), ('magnum_service', 'Magnum Service')], max_length=50)),
                ('configuration', models.TextField()),
            ],
        ),
    ]
