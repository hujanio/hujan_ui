# Generated by Django 2.2.10 on 2020-07-24 04:49

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('installers', '0007_deployment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Installer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('steps', multiselectfield.db.fields.MultiSelectField(choices=[('server', 'Server'), ('inventory', 'Inventory'), ('global_configuration', 'Global Configuration'), ('advanced_configuration', 'Advanced Configuration'), ('deployment', 'Deployment')], default='server', max_length=71)),
            ],
        ),
    ]