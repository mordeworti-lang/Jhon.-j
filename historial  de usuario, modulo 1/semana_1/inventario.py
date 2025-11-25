# Bucle para pedir el nombre del producto hasta que sea válido (solo letras)
while True:
    producto = str(input("¿Qué producto deseas agregar al inventario? "))
    if producto.isalpha():  # Verifica que el producto contenga solo letras
        break  # Sale del bucle si es válido
    else:
        print("Oe, volvete serio, eso es un número.")  # Mensaje si el input es inválido

# Bucle para pedir el precio del producto hasta que sea un número válido
while True:
    try:
        precio = float(input("¿Cuál es el precio de este? "))
        break  # Sale del bucle si la conversión a float es exitosa
    except ValueError:  # Captura el error si no se ingresa un número
        print("Eo, eo, eo, eso no es un número válido.")

# Bucle para pedir la cantidad del producto hasta que sea un entero válido
while True:
    try:
        cantidad = int(input("¿Cuál es la cantidad de este? "))
        break  # Sale del bucle si la conversión a int es exitosa
    except ValueError:  # Captura el error si no se ingresa un número entero
        print("Ombree, pone un número. Hermano, no jodas.")
        continue  # Continua el bucle hasta que se ingrese correctamente

# Calcula el costo total multiplicando precio por cantidad
costo_total = float(precio * cantidad)

# Muestra un resumen del producto agregado
print(f"{producto} / su precio es {precio} / la cantidad de este es {cantidad} / su costo total es {costo_total}.")