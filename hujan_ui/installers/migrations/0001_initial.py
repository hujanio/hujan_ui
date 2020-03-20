# Generated by Django 2.2.10 on 2020-03-19 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('ip_address', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=220)),
                ('system_id', models.TextField(help_text='unique id MAAS')),
            ],
        ),
    ]
