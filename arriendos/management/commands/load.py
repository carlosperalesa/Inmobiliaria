import os
import json
from django.core.management.base import BaseCommand
from arriendos.models import Region, Comuna


class Command(BaseCommand):
    help = 'Carga datos de regiones y comunas desde un archivo JSON'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, 'ubicaciones.json')
        with open(json_path) as f:
            data = json.load(f)
            for region, comunas in data['regiones'].items():
                region_obj, created = Region.objects.get_or_create(
                    nombre=region)
                for comuna_nombre in comunas:
                    Comuna.objects.get_or_create(
                        nombre=comuna_nombre, region=region_obj)

        self.stdout.write(self.style.SUCCESS(
            'Los datos se cargaron exitosamente'))
