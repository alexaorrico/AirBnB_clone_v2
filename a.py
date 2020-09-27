def Menu():
    """Funcion que Muestra el Menu"""
    print("""************
Calculadora
************
Menu
1) Suma
2) multiplicar
3) Salir""")
def Calculadora():
    """Funcion Para Calcular Operaciones Aritmeticas"""
    Menu()
    opc = int(input("Selecione Opcion\n"))
    if (opc==3):
        print("sistema saliendo de la Calculadora")
        exit()
    while (opc >0 and opc <=3):
        x = int(input("Ingrese Numero\n"))
        y = int(input("Ingrese Otro Numero\n"))
        if (opc==1):
            print("La Suma es:", x+y)
            exit()
        if (opc==2):
            print("La multiplicación es:", x*y)
            exit()


if __name__ == '__main__':
    Calculadora()
