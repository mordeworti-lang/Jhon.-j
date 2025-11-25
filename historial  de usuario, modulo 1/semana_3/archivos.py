def validacion(pregunta, tipo):
    """Valida la entrada del usuario según el tipo especificado."""
    while True:
        try:
            valor = input(pregunta).strip()
            if tipo != str:
                return tipo(valor)
            if valor:
                return valor
            else:
                print(" Inválido. No puede estar vacío.")
        except ValueError:
            print(f" Inválido. Se esperaba {tipo.__name__}.")

   
def pedir_texto(pregunta):
    """Solicita un texto no vacío."""
    return validacion(pregunta, str)

 
def pedir_int(pregunta):
    """Solicita un número entero mayor a 0."""
    while True:
        valor = validacion(pregunta, int)
        if valor > 0:
            return valor
        else:  
            print(" Número inválido. Debe ser mayor a 0.")


def pedir_float(pregunta):
    """Solicita un número decimal mayor a 0."""
    while True:
        valor = validacion(pregunta, float)
        if valor > 0:
            return valor    
        else:  
            print(" Número inválido. Debe ser mayor a 0.")


def agregar_a_diccionario(inventario, nombre=None, precio=None, cantidad=None):
    """
    Agrega un nuevo producto al inventario.
    
    Parámetros:
        inventario (list): Lista de productos
        nombre (str, opcional): Nombre del producto
        precio (float, opcional): Precio del producto
        cantidad (int, opcional): Cantidad en stock
    
    Retorna:
        str: Mensaje de éxito o error
    """
    # Si no se pasan parámetros, pedir al usuario
    if nombre is None:
        nombre = pedir_texto(" ¿Cuál producto vas a agregar?: ")
    if precio is None:
        precio = pedir_float(" ¿Cuál es el precio?: $")
    if cantidad is None:  
        cantidad = pedir_int(" ¿Cuál es la cantidad?: ")
    
    # Verificar si ya existe
    producto_existe = buscar_producto(inventario, nombre)
    if producto_existe:
        print(f" El producto '{nombre}' ya existe. Usa 'Actualizar' para modificarlo.")
        return f"Producto '{nombre}' ya existe."
    
    # Crear producto (usar "nombre" en lugar de "producto")
    producto = { 
        "nombre": nombre,  # ← Cambiar "producto" por "nombre"
        "precio": float(precio),
        "cantidad": int(cantidad)
    }
    inventario.append(producto)
    print(f" Producto '{nombre}' agregado exitosamente.")
    return f"Producto '{nombre}' agregado."


def mostrar_inventario(inventario):
    """Muestra todos los productos del inventario."""
    if not inventario:
        print(" El inventario está vacío.")
        return
    
    print("\n" + "=" * 60)
    print(f"{'NOMBRE':25} {'PRECIO':>10} {'CANTIDAD':>10} {'SUBTOTAL':>12}")
    print("=" * 60)
    
    for p in inventario:
        subtotal = p["precio"] * p["cantidad"]
        print(f"{p['nombre'][:25]:25} ${p['precio']:>9.2f} {p['cantidad']:>10} ${subtotal:>11.2f}")
    
    print("=" * 60)

    
def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre (case-insensitive).
    
    Parámetros:
        inventario (list): Lista de productos
        nombre (str): Nombre del producto a buscar
    
    Retorna:
        dict o None: El producto encontrado o None si no existe
    """
    nombre_lower = nombre.lower().strip()
    for p in inventario:
        if p["nombre"].lower() == nombre_lower:  # ← Usar "nombre"
            return p 
    return None 


def eliminar(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.
    
    Parámetros:
        inventario (list): Lista de productos
        nombre (str): Nombre del producto a eliminar
    
    Retorna:
        tuple: (bool, str) - (éxito, mensaje)
    """
    p = buscar_producto(inventario, nombre)
    if not p:
        print(f" Producto '{nombre}' no encontrado.")
        return False, f"Producto '{nombre}' no encontrado."
    
    confirmacion = input(f" ¿Seguro que deseas eliminar '{nombre}'? (S/N): ").strip().upper()
    if confirmacion != 'S':
        print(" Eliminación cancelada.")
        return False, "Eliminación cancelada."
   
    inventario.remove(p)
    print(f" Producto '{nombre}' eliminado exitosamente.")
    return True, f"Producto '{nombre}' eliminado."
   

def actualizar(inventario, nombre, nuevo_precio=None, nueva_cantidad=None, nuevo_nombre=None):
    """
    Actualiza un producto existente.
    
    Parámetros:
        inventario (list): Lista de productos
        nombre (str): Nombre del producto a actualizar
        nuevo_precio (float, opcional): Nuevo precio
        nueva_cantidad (int, opcional): Nueva cantidad
        nuevo_nombre (str, opcional): Nuevo nombre
    
    Retorna:
        str: Mensaje de resultado
    """
    p = buscar_producto(inventario, nombre)
    if not p:
        print(f" Producto '{nombre}' no encontrado.")
        return "Producto no encontrado."
    
    # Modo interactivo
    if nuevo_precio is None and nueva_cantidad is None and nuevo_nombre is None:
        print(f"\n Actualizando: {p['nombre']}")  # ← Corregido: usar p['nombre']
        print(f"   Precio actual: ${p['precio']:.2f}")
        print(f"   Cantidad actual: {p['cantidad']}")
     
        while True:
            print("\n¿Qué deseas actualizar?")
            print("1) Precio")
            print("2) Cantidad")
            print("3) Nombre")
            print("4) Todos")
            print("5) Cancelar")
            
            opcion = pedir_int("Opción: ")
            
            if opcion == 1:
                p["precio"] = pedir_float(" Nuevo precio: $")
                print(" Precio actualizado.")
                break
            elif opcion == 2:
                p["cantidad"] = pedir_int(" Nueva cantidad: ")
                print(" Cantidad actualizada.")
                break
            elif opcion == 3:
                p["nombre"] = pedir_texto(" Nuevo nombre: ")
                print(" Nombre del producto actualizado.")
                break
            elif opcion == 4:
                p["precio"] = pedir_float(" Nuevo precio: $")
                p["cantidad"] = pedir_int(" Nueva cantidad: ")
                p["nombre"] = pedir_texto(" Nuevo nombre: ")
                print(" Producto actualizado completamente.")
                break
            elif opcion == 5:
                print(" Actualización cancelada.")
                return "Actualización cancelada."
            else:
                print("⚠️ Opción inválida.")
    
    # Modo programático (para CSV)
    else:
        if nuevo_precio is not None:
            p["precio"] = float(nuevo_precio)
        if nueva_cantidad is not None:
            p["cantidad"] = int(nueva_cantidad)
        if nuevo_nombre is not None:
            p["nombre"] = str(nuevo_nombre)
        print(" Producto actualizado.")
    
    return "Producto actualizado."


def calcular_estadisticas(inventario):
    """
    Calcula estadísticas del inventario.
    
    Parámetros:
        inventario (list): Lista de productos
    
    Retorna:
        tuple: (unidades_totales, valor_total, producto_mas_caro, producto_mayor_stock, funcion_subtotal)
    """
    if not inventario:
        return (0, 0.0, None, None, None)
    
    # Lambda para calcular subtotal
    subtotal = lambda p: p["precio"] * p["cantidad"]
    
    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)
    producto_mas_caro = max(inventario, key=lambda x: x["precio"])
    producto_mayor_stock = max(inventario, key=lambda x: x["cantidad"])
    
    return (unidades_totales, valor_total, producto_mas_caro, producto_mayor_stock, subtotal)

   
def mostrar_estadisticas(inventario):
    """Muestra las estadísticas del inventario de forma legible."""
    if not inventario:
        print("📭 No hay productos para calcular estadísticas.")
        return
    
    unidades, valor, mas_caro, mayor_stock, subtotal = calcular_estadisticas(inventario)

    print("\n" + "=" * 60)
    print("               ESTADÍSTICAS DEL INVENTARIO")
    print("=" * 60)
    print(f"{'NOMBRE':22} {'CANT':>5} {'PRECIO':>10}   {'SUBTOTAL':>12}")
    print("-" * 60)
    
    for p in inventario:
        subtotal_valor = subtotal(p)  # ← Corregido: llamar a la función
        print(f"{p['nombre'][:22]:22} {p['cantidad']:>5} ${p['precio']:>9.2f}  ${subtotal_valor:>11.2f}")
    
    print("=" * 60)
    print(f"TOTAL PRODUCTOS: {unidades}")
    print(f"VALOR TOTAL INVENTARIO: ${valor:,.2f}")
    print("=" * 60)
    
    print("\n Producto más caro:")
    print(f"   → {mas_caro['nombre']} - ${mas_caro['precio']:.2f}")
    
    print("\n Producto con más stock:")
    print(f"   → {mayor_stock['nombre']} - {mayor_stock['cantidad']} unidades")
    print()