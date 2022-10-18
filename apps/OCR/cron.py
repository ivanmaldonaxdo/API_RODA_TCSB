import time
from APIOpenkm import OpenKM

def opkm():
openkm = Openkm()

#openkm = OpenKm('usrocr', 'j2X7^1IwI^cn','http://65.21.188.116:8080/OpenKM/services/rest/')
#response = openkm.get_docs(_serv='AGU',_path = '/okm:root/Cobros/76242774-5/1/2020/AGU')

print(type(response.content))
 now = time.localtime(time.time())
fecha = time.strftime("%Y_%m_%d", now)
print(fecha)
with open("boleta_{}.pdf" .format(fecha), "wb") as pdf:
    pdf.write(response.content)
query = {
    'anio_doc':'2020'
}