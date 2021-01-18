
import datetime

def revertirfecha(fecha):
    fecha_formato = '%d/%m/%Y'
    fecha_obj = datetime.datetime.strptime(fecha, fecha_formato)
    return fecha_obj