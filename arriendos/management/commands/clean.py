from django.core.management.base import BaseCommand
import os
import shutil
import re  # Importamos el módulo re para trabajar con expresiones regulares


class Command(BaseCommand):
    help = 'Elimina las carpetas __pycache__ y los archivos log.000.txt en el directorio del proyecto.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS(
            'Iniciando la limpieza de __pycache__ y archivos log...'))
        # Directorio actual del proyecto
        self.eliminar_pycache_y_logs(os.getcwd())

    def eliminar_pycache_y_logs(self, directorio):
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

            # Eliminar archivos log.000.txt
            for file in files:
                # Expresión regular para log.000.txt
                if re.match(r"log\.\d{3}\.txt", file):
                    ruta_completa = os.path.join(root, file)
                    self.stdout.write(self.style.SUCCESS(
                        'Eliminando: {}'.format(ruta_completa)))
                    try:
                        os.remove(ruta_completa)
                        self.stdout.write(
                            self.style.SUCCESS('¡Archivo eliminado!'))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(
                            'Error al eliminar el archivo: {}'.format(e)))
