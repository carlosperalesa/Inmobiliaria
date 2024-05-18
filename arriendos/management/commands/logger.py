import os
from datetime import datetime
from django.core.management.base import BaseCommand

# Define los archivos a copiar
archivos_py = {
    "se": "inmobiliaria/settings.py",
    "ur": "inmobiliaria/urls.py",
    "vi": "arriendos/views.py",
    "mo": "arriendos/models.py",
    "fo": "arriendos/forms.py",
    "ap": "arriendos/apps.py",
    "ad": "arriendos/admin.py"
}

archivos_html = {
    "tin": "arriendos/templates/index.html",
    "twe": "arriendos/templates/welcome.html",
    "tco": "arriendos/templates/contacto.html",
    "the": "arriendos/templates/header.html",
    "tfo": "arriendos/templates/footer.html",
    "tlu": "arriendos/templates/registration/login.html",
    "teu": "arriendos/templates/registration/edit.html",
    "tru": "arriendos/templates/registration/register.html",
    "tci": "arriendos/templates/inmuebles/crear_inmuebles.html",
    "tei": "arriendos/templates/inmuebles/editar_inmuebles.html",
    "tvi": "arriendos/templates/inmuebles/ver_inmuebles.html",
    "tvp": "arriendos/templates/inmuebles/ver_propiedad.html",
}


class Command(BaseCommand):
    help = "Copiar contenido de archivos especificados a un archivo de salida."

    def add_arguments(self, parser):
        parser.add_argument(
            "--py", nargs="*", help="Archivos Python a incluir", choices=archivos_py.keys())
        parser.add_argument(
            "--html", nargs="*", help="Archivos HTML a incluir", choices=archivos_html.keys())

    def handle(self, *args, **options):
        # Define el prefijo del archivo de salida
        archivo_salida_prefijo = "log."

        # Obtiene la ruta del directorio actual (donde está este script)
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Inicializa el contador de archivos de salida
        contador = 0

        # Itera mientras exista un archivo con el nombre generado
        while os.path.isfile(os.path.join(script_dir, f"{archivo_salida_prefijo}{str(contador).zfill(3)}.txt")):
            contador += 1

        # Define el nombre del archivo de salida
        archivo_salida = os.path.join(script_dir, f"{archivo_salida_prefijo}{
                                      str(contador).zfill(3)}.txt")

        # Abre el archivo de salida en modo de escritura
        try:
            with open(archivo_salida, "w") as archivo_out:
                # Escribe un encabezado en el archivo de salida
                archivo_out.write(f"Log generado el {
                                  datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                archivos_no_encontrados = True

                # Función para procesar archivos
                def procesar_archivos(archivo_dict, archivo_keys):
                    nonlocal archivos_no_encontrados
                    for archivo in archivo_keys:
                        archivo_completo = archivo_dict[archivo]

                        # Verifica si el archivo existe
                        if os.path.isfile(archivo_completo):
                            archivos_no_encontrados = False
                            try:
                                # Abre el archivo en modo de lectura
                                with open(archivo_completo, "r") as archivo_in:
                                    archivo_out.write(
                                        f"\n******************************{archivo_completo}******************************\n\n")
                                    archivo_out.write(archivo_in.read())
                            except Exception as e:
                                archivo_out.write(f"\nError al leer {
                                                  archivo_completo}: {str(e)}\n\n")
                        else:
                            archivo_out.write(
                                f"\n******************************{archivo_completo} no existe******************************\n\n")

                # Procesar archivos Python
                if options["py"] is not None:
                    if len(options["py"]) == 0:
                        options["py"] = archivos_py.keys()
                    procesar_archivos(archivos_py, options["py"])

                # Procesar archivos HTML
                if options["html"] is not None:
                    if len(options["html"]) == 0:
                        options["html"] = archivos_html.keys()
                    procesar_archivos(archivos_html, options["html"])

                if archivos_no_encontrados:
                    archivo_out.write(
                        "No se encontraron archivos válidos para copiar.\n")

            self.stdout.write(self.style.SUCCESS(
                f"Todo OK. Archivo de salida: {archivo_salida}"))
        except Exception as e:
            self.stderr.write(
                f"Error al escribir en el archivo de salida: {str(e)}")
