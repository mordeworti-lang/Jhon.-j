

# Importaciones desde tus módulos
from archivos import (
    agregar_a_diccionario, mostrar_inventario, buscar_producto,
    actualizar, eliminar, mostrar_estadisticas,
    pedir_texto, pedir_int
)
from guardar import guardar_csv, cargar_con_opciones

# Inventario global (lista de diccionarios)
inventario = []

# Ruta predeterminada del archivo CSV
RUTA_CSV = "inventario.csv"


def mostrar_menu():
    """Muestra el menú principal."""
    print("\n" + "="*50)
    print("       SISTEMA DE GESTIÓN DE INVENTARIO")
    print("="*50)
    print("  1️  Agregar producto")
    print("  2️  Mostrar inventario")
    print("  3️  Buscar producto")
    print("  4️  Actualizar producto")
    print("  5️  Eliminar producto")
    print("  6️  Ver estadísticas")
    print("  7️  Guardar en CSV")
    print("  8️  Cargar desde CSV")
    print("  9️  Salir")
    print("="*50)


def main():
    """Función principal del programa."""
    print("\n Bienvenido al Sistema de Inventario")
    print("   Puedes cargar un inventario existente o empezar desde cero.\n")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("  Selecciona una opción (1-9): "))
        except ValueError:
            print(" Eso no es un número válido. Intenta de nuevo.")
            continue
        
        # ========== OPCIÓN 1: AGREGAR ==========
        if opcion == 1:
            try:
                print("\n--- AGREGAR PRODUCTO ---")
                agregar_a_diccionario(inventario)
            except KeyboardInterrupt:
                print("\n Operación cancelada.")
            except Exception as e:
                print(f" Error inesperado: {e}")
        
        # ========== OPCIÓN 2: MOSTRAR ==========
        elif opcion == 2:
            try:
                print("\n--- INVENTARIO COMPLETO ---")
                mostrar_inventario(inventario)
            except Exception as e:
                print(f" Error al mostrar inventario: {e}")
        
        # ========== OPCIÓN 3: BUSCAR ==========
        elif opcion == 3:
            try:
                print("\n--- BUSCAR PRODUCTO ---")
                nombre = pedir_texto(" Nombre del producto: ")
                producto = buscar_producto(inventario, nombre)  # ← Cambiar a 'producto'
                
                if producto:
                    print("\n Producto encontrado:")
                    print(f"   Nombre: {producto['nombre']}")  # ← Cambiar a 'nombre'
                    print(f"   Precio: ${producto['precio']:.2f}")
                    print(f"   Cantidad: {producto['cantidad']} unidades")
                    print(f"   Valor total: ${producto['precio'] * producto['cantidad']:.2f}")
                else:
                    print(f" Producto '{nombre}' no encontrado.")
            except KeyboardInterrupt:
                print("\n Búsqueda cancelada.")
            except Exception as e:
                print(f" Error al buscar: {e}")
        
        # ========== OPCIÓN 4: ACTUALIZAR ==========
        elif opcion == 4:
            try:
                print("\n--- ACTUALIZAR PRODUCTO ---")
                if not inventario:
                    print(" El inventario está vacío.")
                else:
                    nombre = pedir_texto(" Nombre del producto a actualizar: ")
                    actualizar(inventario, nombre)
            except KeyboardInterrupt:
                print("\n Actualización cancelada.")
            except Exception as e:
                print(f" Error al actualizar: {e}")
        
        # ========== OPCIÓN 5: ELIMINAR ==========
        elif opcion == 5:
            try:
                print("\n--- ELIMINAR PRODUCTO ---")
                if not inventario:
                    print(" El inventario está vacío.")
                else:
                    nombre = pedir_texto("  Nombre del producto a eliminar: ")
                    eliminar(inventario, nombre)
            except KeyboardInterrupt:
                print("\n Eliminación cancelada.")
            except Exception as e:
                print(f" Error al eliminar: {e}")
        
        # ========== OPCIÓN 6: ESTADÍSTICAS ==========
        elif opcion == 6:
            try:
                print("\n--- ESTADÍSTICAS DEL INVENTARIO ---")
                mostrar_estadisticas(inventario)
            except Exception as e:
                print(f" Error al calcular estadísticas: {e}")
        
        # ========== OPCIÓN 7: GUARDAR CSV ==========
        elif opcion == 7:
            try:
                print("\n--- GUARDAR INVENTARIO ---")
                guardar_csv(inventario, RUTA_CSV)
            except KeyboardInterrupt:
                print("\n Guardado cancelado.")
            except Exception as e:
                print(f" Error al guardar: {e}")
        
        # ========== OPCIÓN 8: CARGAR CSV ==========
        elif opcion == 8:
            try:
                print("\n--- CARGAR INVENTARIO ---")
                cargar_con_opciones(inventario, RUTA_CSV)
            except KeyboardInterrupt:
                print("\n Carga cancelada.")
            except Exception as e:
                print(f" Error al cargar: {e}")
        
        # ========== OPCIÓN 9: SALIR ==========
        elif opcion == 9:
            print("\n ¡Gracias por usar el Sistema de Inventario!")
            
            # Preguntar si desea guardar antes de salir
            if inventario:
                guardar_antes_salir = input("¿Deseas guardar el inventario antes de salir? (S/N): ").strip().upper()
                if guardar_antes_salir == 'S':
                    try:
                        guardar_csv(inventario, RUTA_CSV)
                    except Exception as e:
                        print(f" No se pudo guardar: {e}")
            
            print(" Programa finalizado.")
            break
        
        # ========== OPCIÓN INVÁLIDA ==========
        else:
            print(" Opción inválida. Por favor selecciona un número del 1 al 9.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Programa interrumpido por el usuario.")
        print(" Saliendo...")
    except Exception as e:
        print(f"\n Error crítico: {e}")
        print(" El programa se cerrará.")
    







