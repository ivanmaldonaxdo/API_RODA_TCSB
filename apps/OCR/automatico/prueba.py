






from apps.management.models import Cliente


class claseprueba():

    def prueba():
        cli = Cliente.objects.get(nom_cli="BANCO DEL ESTADO")
        print(cli)
    

print()