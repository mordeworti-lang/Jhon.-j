# ============================================================================
# ARCHIVO 6: reportes.py
# ============================================================================
# 
# PROPÓSITO: Este archivo maneja la generación de REPORTES y ESTADÍSTICAS
# del sistema.
#
# ¿QUÉ HACE?
# ----------
# - Mostrar historial de compras de UN cliente específico
# - Mostrar historial de TODOS los clientes
# - Calcular y mostrar los 3 libros más vendidos
# - Agrupar ventas por autor
# - Generar estadísticas útiles para el negocio
#
# IMPORTACIONES NECESARIAS:
# -------------------------
from validacion import pedir_int, pedir_texto
# Importamos las funciones de validación
#
# ============================================================================


class GestorReportes:
    """
    EXPLICACIÓN DE ESTA CLASE:
    --------------------------
    Esta clase genera reportes y estadísticas basados en los datos
    de clientes y ventas.
    
    NO MODIFICA DATOS, solo los LEE y los presenta de forma útil.
    
    RESPONSABILIDADES:
    ------------------
    1. Mostrar historial individual de clientes
    2. Mostrar historial de todos los clientes
    3. Calcular libros más vendidos
    4. Agrupar ventas por autor
    5. Generar estadísticas de negocio
    
    ATRIBUTOS DE LA CLASE:
    ----------------------
    - self.clientes: Referencia al gestor de clientes
    - self.ventas: Referencia al gestor de ventas
    
    NOTA:
    -----
    Esta clase NO guarda datos, solo consulta los gestores
    de clientes y ventas para generar reportes.
    """
    
    def __init__(self, gestor_clientes, gestor_ventas):
        """
        CONSTRUCTOR DE LA CLASE:
        ------------------------
        Inicializa el gestor de reportes.
        
        PARÁMETROS:
        -----------
        - gestor_clientes: Objeto GestorClientes (para acceder a clientes)
        - gestor_ventas: Objeto GestorVentas (para acceder a ventas)
        
        COMPOSICIÓN:
        ------------
        Esta clase NECESITA acceso a otros gestores para generar reportes.
        No tiene sus propios datos, consulta los datos de otros módulos.
        """
        self.clientes = gestor_clientes
        self.ventas = gestor_ventas
    
    
    def menu(self):
        """
        MENÚ DE REPORTES:
        -----------------
        Menú principal con todas las opciones de reportes disponibles.
        """
        while True:
            print("\n" + "="*50)
            print(" REPORTES Y ESTADÍSTICAS")
            print("="*50)
            print("1. Ver historial de un cliente")
            print("2. Ver todos los clientes y sus compras")
            print("3. Top 3 libros más vendidos")
            print("4. Ventas agrupadas por autor")
            print("5. Volver al menú principal")
            
            opcion = pedir_int("\nSelecciona una opción: ")
            
            if opcion == 1:
                self.ver_historial_cliente()
            elif opcion == 2:
                self.ver_todos_clientes()
            elif opcion == 3:
                self.libros_mas_vendidos()
            elif opcion == 4:
                self.ventas_por_autor()
            elif opcion == 5:
                break  # Volver al menú principal
            else:
                print(" Opción inválida")
    
    
    def ver_historial_cliente(self):
        """
        VER HISTORIAL DE UN CLIENTE:
        ----------------------------
        Busca un cliente específico y muestra TODAS sus compras.
        
        MUESTRA:
        --------
        - Datos del cliente (nombre, ID, fecha registro)
        - Total gastado
        - Número de compras
        - Detalle de cada compra:
          * Fecha y hora
          * Productos comprados
          * Total de la compra
        """
        print("\n--- Buscar Cliente ---")
        termino = pedir_texto("Ingresa nombre o ID del cliente: ")
        
        # Buscar el cliente
        id_encontrado, cliente_encontrado = self.clientes.buscar_cliente(termino)
        # Esto retorna una TUPLA: (id, datos) o (None, None)
        
        # Verificar si se encontró
        if not cliente_encontrado:
            print(" Cliente no encontrado")
            return  # Salir de la función
        
        # Mostrar información del cliente
        print("\n" + "="*50)
        print(f" CLIENTE: {cliente_encontrado['nombre']}")
        print("="*50)
        print(f"ID: {id_encontrado}")
        print(f"Fecha de registro: {cliente_encontrado['fecha_registro']}")
        print(f"Total gastado: ${cliente_encontrado['total_gastado']:.2f}")
        print(f"Número de compras: {len(cliente_encontrado['compras'])}")
        # len() da la longitud de una lista
        
        # Verificar si tiene compras
        if cliente_encontrado['compras']:
            print("\n HISTORIAL DE COMPRAS:")
            
            # Mostrar cada compra
            for i, compra in enumerate(cliente_encontrado['compras'], 1):
                # enumerate() da el índice y el elemento
                # start=1 hace que empiece en 1
                
                print(f"\n--- Compra #{i} ---")
                print(f"Fecha: {compra['fecha']}")
                print("Productos:")
                
                # Mostrar cada producto de la compra
                for prod in compra['productos']:
                    print(f"  - {prod['titulo']} x{prod['cantidad']} = ${prod['subtotal']:.2f}")
                
                print(f"Total: ${compra['total']:.2f}")
        else:
            print("\n Este cliente no tiene compras registradas")
    
    
    def ver_todos_clientes(self):
        """
        VER TODOS LOS CLIENTES:
        -----------------------
        Muestra la información de TODOS los clientes registrados,
        incluyendo su historial completo de compras.
        
        FORMATO:
        --------
        Para cada cliente:
        - Información básica (nombre, ID, registro)
        - Estadísticas (total gastado, número de compras)
        - Historial completo de compras
        
        SEPARACIÓN:
        -----------
        Cada cliente se muestra en su propia sección, claramente
        separada para facilitar la lectura.
        """
        # Verificar si hay clientes
        if not self.clientes.clientes:
            print("\n No hay clientes registrados")
            return
        
        # Mostrar encabezado
        print("\n" + "="*50)
        print(f" TODOS LOS CLIENTES ({len(self.clientes.clientes)})")
        print("="*50)
        
        # Recorrer todos los clientes
        for id_cliente, datos in self.clientes.clientes.items():
            # .items() da pares (clave, valor)
            
            # Separador visual entre clientes
            print(f"\n{'='*50}")
            print(f"👤 {datos['nombre']} (ID: {id_cliente})")
            print(f"{'='*50}")
            
            # Información básica
            print(f"Registro: {datos['fecha_registro']}")
            print(f"Total gastado: ${datos['total_gastado']:.2f}")
            print(f"Compras realizadas: {len(datos['compras'])}")
            
            # Historial de compras
            if datos['compras']:
                print("\n Historial:")
                
                # Mostrar cada compra
                for i, compra in enumerate(datos['compras'], 1):
                    print(f"\n  Compra #{i} - {compra['fecha']}")
                    
                    # Mostrar productos de la compra
                    for prod in compra['productos']:
                        print(f"    • {prod['titulo']} x{prod['cantidad']} (${prod['subtotal']:.2f})")
                    
                    print(f"    Total: ${compra['total']:.2f}")
            else:
                print("\n   Sin compras registradas")
    
    
    def libros_mas_vendidos(self):
        """
        TOP 3 LIBROS MÁS VENDIDOS:
        ---------------------------
        Calcula cuáles son los 3 libros más vendidos del sistema.
        
        PROCESO:
        --------
        1. Recorrer TODAS las ventas
        2. Contar cuántas unidades se vendieron de cada libro
        3. Calcular ingresos generados por cada libro
        4. Ordenar por cantidad vendida
        5. Mostrar los 3 primeros
        
        MUESTRA:
        --------
        Para cada libro:
        - Título y autor
        - Unidades vendidas
        - Ingresos generados
        
        ESTRUCTURA DE DATOS:
        --------------------
        Usamos un DICCIONARIO para acumular las ventas:
        {
            "Python Básico": {
                "titulo": "Python Básico",
                "autor": "Juan López",
                "cantidad": 15,      # Total de unidades vendidas
                "ingresos": 389.85   # Total de dinero generado
            },
            "JavaScript Pro": {
                ...
            }
        }
        """
        ventas_por_libro = {}  # Diccionario vacío
        
        # PASO 1: Recorrer todas las ventas
        for venta in self.ventas.obtener_ventas():
            # Cada venta tiene una lista de productos
            
            # Recorrer cada producto de la venta
            for prod in venta['productos']:
                titulo = prod['titulo']
                
                # PASO 2: Si es la primera vez que vemos este libro, inicializarlo
                if titulo not in ventas_por_libro:
                    ventas_por_libro[titulo] = {
                        'titulo': prod['titulo'],
                        'autor': prod['autor'],
                        'cantidad': 0,
                        'ingresos': 0
                    }
                
                # PASO 3: Acumular cantidad e ingresos
                ventas_por_libro[titulo]['cantidad'] += prod['cantidad']
                ventas_por_libro[titulo]['ingresos'] += prod['subtotal']
                # += suma al valor actual
        
        # Verificar si hay ventas
        if not ventas_por_libro:
            print("\n No hay ventas registradas")
            return
        
        # PASO 4: Ordenar por cantidad vendida
        # sorted() ordena una lista
        # key=lambda x: x[1]['cantidad'] significa "ordenar por cantidad"
        # reverse=True significa orden descendente (mayor a menor)
        # [:3] toma solo los primeros 3 elementos
        top_libros = sorted(
            ventas_por_libro.items(),  # Convertir a lista de tuplas
            key=lambda x: x[1]['cantidad'],  # Criterio de ordenamiento
            reverse=True  # Mayor a menor
        )[:3]  # Solo los primeros 3
        
        # LAMBDA EXPLICADA:
        # -----------------
        # lambda x: x[1]['cantidad'] es una función anónima
        # x es una tupla: (titulo, datos)
        # x[1] es el segundo elemento: datos
        # x[1]['cantidad'] es el valor de cantidad
        # 
        # Es equivalente a:
        # def obtener_cantidad(tupla):
        #     return tupla[1]['cantidad']
        
        # PASO 5: Mostrar resultados
        print("\n" + "="*50)
        print(" TOP 3 LIBROS MÁS VENDIDOS")
        print("="*50)
        
        for i, (titulo, datos) in enumerate(top_libros, 1):
            # i es la posición (1, 2, 3)
            # titulo es el título del libro
            # datos es el diccionario con la información
            
            print(f"\n{i}. {datos['titulo']}")
            print(f"   Autor: {datos['autor']}")
            print(f"   Unidades vendidas: {datos['cantidad']}")
            print(f"   Ingresos generados: ${datos['ingresos']:.2f}")
    
    
    def ventas_por_autor(self):
        """
        VENTAS AGRUPADAS POR AUTOR:
        ---------------------------
        Muestra estadísticas de ventas agrupadas por autor.
        
        MUESTRA:
        --------
        Para cada autor:
        - Nombre del autor
        - Libros diferentes que vendió
        - Títulos de esos libros
        - Total de unidades vendidas
        - Total de ingresos generados
        
        PROCESO:
        --------
        1. Recorrer todas las ventas
        2. Agrupar por autor
        3. Acumular libros, unidades e ingresos
        4. Ordenar por ingresos
        5. Mostrar resultados
        
        ESTRUCTURA DE DATOS:
        --------------------
        {
            "Juan López": {
                "libros": {"Python Básico", "Python Avanzado"},  # SET
                "unidades": 25,
                "ingresos": 650.00
            },
            "María García": {
                ...
            }
        }
        
        SET EXPLICADO:
        --------------
        Un SET es una colección que NO permite duplicados.
        Si agregamos "Python Básico" dos veces, solo queda una vez.
        Ejemplo:
        libros = set()
        libros.add("Python")
        libros.add("Java")
        libros.add("Python")  # No se agrega (duplicado)
        print(libros)  # {"Python", "Java"}
        """
        ventas_autores = {}  # Diccionario vacío
        
        # PASO 1: Recorrer todas las ventas
        for venta in self.ventas.obtener_ventas():
            # Recorrer cada producto
            for prod in venta['productos']:
                autor = prod['autor']
                
                # PASO 2: Si es la primera vez que vemos este autor, inicializarlo
                if autor not in ventas_autores:
                    ventas_autores[autor] = {
                        'libros': set(),  # SET para evitar duplicados
                        'unidades': 0,
                        'ingresos': 0
                    }
                
                # PASO 3: Acumular datos
                ventas_autores[autor]['libros'].add(prod['titulo'])  # Agregar título al SET
                ventas_autores[autor]['unidades'] += prod['cantidad']
                ventas_autores[autor]['ingresos'] += prod['subtotal']
        
        # Verificar si hay ventas
        if not ventas_autores:
            print("\n📭 No hay ventas registradas")
            return
        
        # PASO 4: Ordenar por ingresos (mayor a menor)
        autores_ordenados = sorted(
            ventas_autores.items(),
            key=lambda x: x[1]['ingresos'],
            reverse=True
        )
        
        # PASO 5: Mostrar resultados
        print("\n" + "="*50)
        print(" VENTAS AGRUPADAS POR AUTOR")
        print("="*50)
        
        for autor, datos in autores_ordenados:
            print(f"\n {autor}")
            print(f"   Libros diferentes vendidos: {len(datos['libros'])}")
            print(f"   Títulos: {', '.join(datos['libros'])}")
            # ', '.join() une los elementos de un SET con comas
            # Ejemplo: {"Python", "Java"} -> "Python, Java"
            
            print(f"   Unidades totales: {datos['unidades']}")
            print(f"   Ingresos generados: ${datos['ingresos']:.2f}")


# ============================================================================
# RESUMEN DE ESTE ARCHIVO:
# ============================================================================
# 
# CLASE: GestorReportes
# ---------------------
# Genera reportes y estadísticas del sistema.
# 
# ATRIBUTOS:
# ----------
# - self.clientes: Referencia al gestor de clientes
# - self.ventas: Referencia al gestor de ventas
# 
# MÉTODOS:
# --------
# - menu(): Menú de reportes
# - ver_historial_cliente(): Historial de UN cliente
# - ver_todos_clientes(): Historial de TODOS los clientes
# - libros_mas_vendidos(): Top 3 libros más vendidos
# - ventas_por_autor(): Estadísticas agrupadas por autor
# 
# CONCEPTOS CLAVE:
# ----------------
# 1. LECTURA DE DATOS: Esta clase NO modifica datos, solo los lee
# 2. COMPOSICIÓN: Necesita acceso a otros gestores
# 3. DICCIONARIOS: Para acumular estadísticas
# 4. SET: Para evitar duplicados (libros por autor)
# 5. SORTED: Para ordenar listas
# 6. LAMBDA: Funciones anónimas para criterios de ordenamiento
# 7. ENUMERATE: Para obtener índice y elemento
# 8. COMPRENSIONES: Para procesar listas de forma concisa
# 
# FUNCIONES DE AGREGACIÓN:
# ------------------------
# 1. CONTAR: len(lista) - cantidad de elementos
# 2. SUMAR: total += valor - acumular valores
# 3. AGRUPAR: usar diccionarios para juntar datos relacionados
# 4. ORDENAR: sorted() con key y reverse
# 
# TÉCNICAS DE PRESENTACIÓN:
# -------------------------
# 1. Separadores visuales (=, -, líneas)#
# 2. Formato de números (:.2f para decimales)
# 3. Indentación para jerarquía
# 4. Encabezados claros
# 
# VENTAJAS:
# ---------
# - Información útil para tomar decisiones de negocio
# - Fácil identificar productos populares
# - Seguimiento de clientes individuales
# - Estadísticas por autor
# - Reportes bien formateados y legibles
# 
# ============================================================================