from django.core.management.base import BaseCommand
import os
import shutil


class Command(BaseCommand):
    help = 'Elimina las carpetas __pycache__ en el directorio del proyecto.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS(
            'Iniciando la limpieza de __pycache__...'))
        self.eliminar_pycache(os.getcwd())  # Directorio actual del proyecto

    def eliminar_pycache(self, directorio):
        for root, dirs, files in os.walk(directorio):
            for dir in dirs:
                if dir == "__pycache__":
                    ruta_completa = os.path.join(root, dir)
                    self.stdout.write(self.style.SUCCESS(
                        'Eliminando: {}'.format(ruta_completa)))
                    try:
                        shutil.rmtree(ruta_completa)
                        self.stdout.write(
                            self.style.SUCCESS('¡Carpeta eliminada!'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            'Error al eliminar la carpeta: {}'.format(e)))
