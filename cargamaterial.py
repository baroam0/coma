

from apps.materiales.models import Material

archivo = open("materiales.txt", "r")

materiales = archivo.readlines()

materiales = list(dict.fromkeys(materiales))


for material in materiales:
    if material != "":
        print(material)
        grabar = Material(descripcion=str(material))
        grabar.save()

