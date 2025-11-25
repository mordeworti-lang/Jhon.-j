inventario = {
    "leyes del poder": 12000,
    "la divina comedia": 23000,
    "habitos atomicos": 11250,
    "el arte de la guerra": 10250,
    "padre rico padre pobre": 15000,
    "la santa biblia": 8000,
    "viaje al medio oeste": 30000
}

carrito = {}

# ------------------- PREGUNTAR CANTIDAD -------------------
def pregunta_numero(texto):
    while True:
        try:
            cantidad = int(input(texto))
            if cantidad > 0:
                print(" Dale mi rey. ")
                return cantidad
            else:
                print(" my bro, cantidad inválida. Debe ser mayor que cero.")
        except ValueError:
            print(" my bro, eso no me sirve, escribe un número.")


# ------------------- PREGUNTAR PRODUCTO -------------------
def pregunta(texto):
    while True:
        producto = input(texto)

        if producto in inventario:
            print(" Lo tendras enseguida.")
            return producto
        else:
            print(" my bro, ese libro no lo tenemos.")
            print("Productos disponibles:")
            for p in inventario:
                print(" -", p)
            print()


# ------------------- AGREGAR AL CARRITO -------------------
def agregar_a_carrito():
    producto = pregunta(" ¿Qué libro deseas llevar? ")
    cantidad = pregunta_numero(" ¿Cuántos vas a llevar? ")

    if producto in carrito:
        carrito[producto] += cantidad
    else:
        carrito[producto] = cantidad

    print(f"Agregado: {producto} x{cantidad}")


# ------------------- FACTURA -------------------
def factura():
    print("--" * 30)
    print("              TIENDA EL COMPAA")
    print("--" * 30)
    print(f"{'PRODUCTO':22} {'CANT':4} {'PRECIO':7}   TOTAL")

    productos_totales = 0
    total_precios = 0

    for producto, cantidad in carrito.items():
        precio = inventario[producto]
        total_producto = precio * cantidad

        productos_totales += cantidad
        total_precios += total_producto

        print(f"{producto[:22]:22} {cantidad:4} {precio:7}   {total_producto}")

    print("--" * 30)
    print(f"TOTAL PRODUCTOS: {productos_totales}")
    print(f"TOTAL A PAGAR:   {total_precios}")
    print("--" * 30)
