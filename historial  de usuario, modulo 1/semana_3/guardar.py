import csv
import os

def guardar_csv(inventario, ruta, incluir_header=True):
    """Guarda el inventario en un archivo CSV."""
    if not inventario:
        print(" El inventario está vacío. No hay nada que guardar.")
        return False
    
    try:
        with open(ruta, "w", newline="", encoding="utf-8") as archivo:  # ← Corregido: utf-8
            campos = ['nombre', 'precio', 'cantidad']  # ← Usar "nombre"
            writer = csv.DictWriter(archivo, fieldnames=campos)
            
            if incluir_header:
                writer.writeheader()  # ← Sin parámetros
            
            writer.writerows(inventario)  # ← Agregar esta línea
            
        print(f" Inventario guardado exitosamente en: {ruta}")
        print(f"   ({len(inventario)} productos guardados)")
        return True
        
    except PermissionError:
        print(f" Error: No tienes permisos para escribir en '{ruta}'.")
        return False
    except IOError as e:
        print(f" Error al escribir el archivo: {e}")
        return False
    except Exception as e:
        print(f" Error inesperado al guardar: {e}")
        return False

    
def cargar_csv(ruta):  # ← Eliminar parámetro "inventario"
    """Carga productos desde un archivo CSV."""
    if not os.path.exists(ruta):
        print(f" Archivo no encontrado: {ruta}")
        return None, 0
    
    productos_cargados = []
    filas_invalidas = 0
    numero_linea = 0
    
    try:
        with open(ruta, 'r', encoding='utf-8') as archivo:
            lector = csv.reader(archivo)
            
            try:
                encabezado = next(lector)
                numero_linea += 1
            except StopIteration:
                print(" El archivo está vacío.")
                return None, 0
            
            encabezado_esperado = ['nombre', 'precio', 'cantidad']
            encabezado_limpio = [col.strip().lower() for col in encabezado]
            
            # Validar encabezado (solo una vez)
            if encabezado_limpio != encabezado_esperado:
                print(f" Encabezado inválido. Se esperaba: {','.join(encabezado_esperado)}")
                print(f"   Se encontró: {','.join(encabezado)}")
                return None, 0
            
            # Leer filas
            for fila in lector:
                numero_linea += 1
                
                if len(fila) != 3:
                    print(f" Línea {numero_linea}: Se esperaban 3 columnas, se encontraron {len(fila)}")
                    filas_invalidas += 1
                    continue
                
                # Desempaquetar
                nombre, precio_str, cantidad_str = fila  # ← Corregido: "nombre"
                nombre = nombre.strip()
                
                # Validar nombre no vacío
                if not nombre:
                    print(f" Línea {numero_linea}: Nombre vacío")
                    filas_invalidas += 1
                    continue
                
                try:
                    # Convertir y validar precio
                    precio = float(precio_str.strip())
                    if precio < 0:
                        print(f" Línea {numero_linea}: Precio negativo ({precio})")
                        filas_invalidas += 1
                        continue
                    
                    # Convertir y validar cantidad
                    cantidad = int(cantidad_str.strip())
                    if cantidad < 0:
                        print(f" Línea {numero_linea}: Cantidad negativa ({cantidad})")
                        filas_invalidas += 1
                        continue
                    
                    # Crear producto válido
                    producto = {
                        "nombre": nombre,  # ← Usar "nombre" consistentemente
                        "precio": precio,
                        "cantidad": cantidad
                    }
                    productos_cargados.append(producto)
                    
                except ValueError as e:
                    print(f" Línea {numero_linea}: Error de conversión - {e}")
                    filas_invalidas += 1
                    continue
        
        # Resumen de carga
        print(f"\n Resumen de carga:")
        print(f"    Productos válidos: {len(productos_cargados)}")
        if filas_invalidas > 0:
            print(f"   ⚠️ Filas inválidas omitidas: {filas_invalidas}")
        
        return productos_cargados, filas_invalidas
        
    except UnicodeDecodeError:
        print(f" Error: El archivo '{ruta}' no tiene codificación UTF-8 válida.")
        return None, 0
    except IOError as e:
        print(f" Error al leer el archivo: {e}")
        return None, 0
    except Exception as e:
        print(f" Error inesperado: {e}")
        return None, 0


def fusionar_inventarios(inventario_actual, productos_nuevos):
    """Fusiona productos nuevos con el inventario actual."""
    agregados = 0
    actualizados = 0
    
    for nuevo in productos_nuevos:
        producto_existente = None
        for p in inventario_actual:
            if p["nombre"].lower() == nuevo["nombre"].lower():  # ← Usar "nombre"
                producto_existente = p
                break
        
        if producto_existente:
            # Actualizar: sumar cantidad y actualizar precio
            producto_existente["cantidad"] += nuevo["cantidad"]
            producto_existente["precio"] = nuevo["precio"]
            actualizados += 1
            print(f"    Actualizado: {nuevo['nombre']} (nueva cantidad: {producto_existente['cantidad']})")
        else:
            # Agregar nuevo producto
            inventario_actual.append(nuevo)
            agregados += 1
            print(f"    Agregado: {nuevo['nombre']}")
    
    return agregados, actualizados


def cargar_con_opciones(inventario_actual, ruta):
    """Carga un CSV y pregunta si sobrescribir o fusionar."""
    productos_nuevos, filas_invalidas = cargar_csv(ruta)
    
    if productos_nuevos is None:
        return False
    
    if not productos_nuevos:
        print(" No se encontraron productos válidos en el archivo.")
        return False
    
    # Si el inventario está vacío, simplemente cargar
    if not inventario_actual:
        inventario_actual.extend(productos_nuevos)
        print(f"\n Se cargaron {len(productos_nuevos)} productos.")
        return True
    
    # Preguntar al usuario
    print(f"\n El inventario actual tiene {len(inventario_actual)} productos.")
    print(f"   Se encontraron {len(productos_nuevos)} productos en el archivo.")
    print("\n¿Qué deseas hacer?")
    print("  S - Sobrescribir (reemplazar todo el inventario)")
    print("  F - Fusionar (actualizar existentes y agregar nuevos)")
    print("  C - Cancelar")
    
    while True:
        opcion = input("\nOpción (S/F/C): ").strip().upper()
        
        if opcion == 'S':
            # Sobrescribir
            inventario_actual.clear()
            inventario_actual.extend(productos_nuevos)
            print(f"\n Inventario sobrescrito. Total: {len(inventario_actual)} productos.")
            return True  # ← Agregar return
        
        elif opcion == 'F':
            # Fusionar
            print("\n Fusionando inventarios...")
            print("   Política: Suma cantidades y actualiza precios de productos existentes\n")
            agregados, actualizados = fusionar_inventarios(inventario_actual, productos_nuevos)
            print(f"\n Fusión completada:")
            print(f"    Productos nuevos agregados: {agregados}")
            print(f"    Productos actualizados: {actualizados}")
            print(f"    Total en inventario: {len(inventario_actual)}")
            return True  # ← Agregar return
        
        elif opcion == 'C':
            print(" Carga cancelada.")
            return False
        
        else:
            print(" Opción inválida. Usa S, F o C.")