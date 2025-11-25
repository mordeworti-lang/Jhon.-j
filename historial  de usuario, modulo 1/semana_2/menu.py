from Agregar import * # importo el archivo de agregar. 

# Hago un while para que el menú se repita hasta que yo decida salir.
while True:
    
    # Esto es solo para separar bonito el menú.
    print("_" * 40)
    print(" 1, Agregar producto. ")
    print(" 2, Mostrar inventario. ")
    print(" 3, mostrar carrito. ")
    print(" 4, finalizar compra, y ver valor total del carrito. ")
    print(" 5, Salir. ")
    
    # Otro while para controlar que el usuario no meta basura.
    while True:
        try:
            # Aquí le pido al usuario una opción del menú.
            opcion = int(input(" ¿Que deseas hacer?. "))
            
            # Verifico que el número esté entre 1 y 5.
            if 5 >= opcion >= 1:
                break  # Si sirve, me salgo de este while.
            else:
                # Si mete otro número, le digo que no sirve.
                print(" No sirve mi compaa, tienes que poner un numero del 1 - 5. ")
        except ValueError:
            # Si mete letras o algo raro, cae acá.
            print(" No sirve mi compaa, tienes que poner un numero del 1 - 5. ")
            continue
    
    # Si elige 1, llamo la función para agregar al carrito. 
    if opcion == 1:
        agregar_a_carrito()
    
    # Si elige 2, muestro el inventario que ya tengo cargado.
    elif opcion == 2:
       print(" Nuestros productos:")
       for p in inventario:
                print(" -", p)
                print()

    # Si elige 3, muestro el carrito con lo que se ha ido agregando.
    elif opcion == 3:
        print(" En tu carrito tienes:")
        for p in carrito:
                print(" -", p)
                print()

    # Si elige 4, saco la factura total.
    elif opcion == 4:
        factura()

    # Si elige 5, cierro todo y me salgo del programa.
    elif opcion == 5:
        break
