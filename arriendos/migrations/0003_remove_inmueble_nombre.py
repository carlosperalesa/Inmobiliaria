# Generated by Django 5.0.6 on 2024-05-18 05:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arriendos', '0002_alter_inmueble_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inmueble',
            name='nombre',
        ),
    ]