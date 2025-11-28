# ============================================================================
# ARCHIVO 3: inventario.py
# ============================================================================
# 
# PROPÓSITO: Este archivo maneja todo lo relacionado con el INVENTARIO
# de libros de la librería.
#
# ¿QUÉ HACE?
# ----------
# - Agregar nuevos libros
# - Actualizar información de libros existentes
# - Eliminar libros
# - Buscar libros
# - Mostrar el inventario completo
# - Guardar cambios en archivo JSON
#
# IMPORTACIONES NECESARIAS:
# -------------------------
from validacion import pedir_int, pedir_float, pedir_texto
# Importamos las funciones de validación que creamos en validacion.py
#
# ============================================================================


def mostrar_libro(libro):
    """
    EXPLICACIÓN DETALLADA:
    ----------------------
    Esta función muestra la información de UN libro en pantalla
    de forma bonita y organizada.
    
    PARÁMETROS:
    -----------
    - libro (dict): Un diccionario con la información del libro
      Ejemplo: {"titulo": "Python", "autor": "Juan", "precio": 25.99, ...}
    
    ¿QUÉ ES UN DICCIONARIO?
    -----------------------
    Un diccionario es como una ficha con información:
    {
        "titulo": "Python Básico",     # clave: "titulo", valor: "Python Básico"
        "autor": "Juan Pérez",         # clave: "autor", valor: "Juan Pérez"
        "categoria": "Programación",   # clave: "categoria", valor: "Programación"
        "precio": 25.99,               # clave: "precio", valor: 25.99
        "cantidad": 10                 # clave: "cantidad", valor: 10
    }
    
    Para acceder a un valor: libro["titulo"] -> "Python Básico"
    
    MÉTODO .get():
    -------------
    libro.get('titulo', 'N/A') significa:
    - Intenta obtener el valor de la clave 'titulo'
    - Si la clave no existe, devuelve 'N/A' (No Aplica)
    
    ¿Por qué usar .get() en lugar de libro['titulo']?
    - Si la clave no existe, libro['titulo'] da ERROR
    - Si la clave no existe, libro.get('titulo', 'N/A') devuelve 'N/A'
    """
    print(" Detalles del libro: ")
    print(f"  Titulo: {libro.get('titulo', 'N/A')}")
    print(f"  Autor: {libro.get('autor', 'N/A')}")
    print(f"  Categoria: {libro.get('categoria', 'N/A')}")
    print(f"  Precio: {libro.get('precio', 'N/A')}")
    print(f"  Cantidad: {libro.get('cantidad', 'N/A')}")
    print("---------------------------")
    # f"..." es un f-string, permite insertar variables dentro de texto
    # Ejemplo: nombre = "Juan"
    #          f"Hola {nombre}" -> "Hola Juan"
    
class GestorInventario:
    """
    EXPLICACIÓN DE ESTA CLASE:
    --------------------------
    Esta clase maneja todo lo relacionado con el inventario.
    Es como un "administrador" del inventario.
    
    ¿POR QUÉ USAR UNA CLASE?
    ------------------------
    - Organización: Todas las funciones del inventario están juntas
    - Estado: La clase "recuerda" el inventario actual
    - Modularidad: Podemos usar este código en otros proyectos fácilmente
    
    ATRIBUTOS DE LA CLASE:
    ----------------------
    Los atributos son VARIABLES que pertenecen a la clase.
    Se crean en el método __init__() y se acceden con self.
    
    - self.inventario: Lista con todos los libros
    - self.persistencia: Objeto para guardar/cargar datos
    - self.archivo: Nombre del archivo donde se guarda el inventario
    """
    def __init__(self, inventario: list, persistencia):
        """
        MÉTODO CONSTRUCTOR:
        -------------------
        __init__() es un método ESPECIAL que se ejecuta automáticamente
        cuando creamos un objeto de la clase.
        
        Es como la "inicialización" o "configuración inicial" del objeto.
        
        PARÁMETROS:
        -----------
        - self: Referencia al objeto mismo (obligatorio en todos los métodos)
        - inventario: Lista de libros que ya existen (puede estar vacía)
        - persistencia: Objeto GestorPersistencia para guardar/cargar datos
        
        EJEMPLO DE USO:
        ---------------
        gestor = GestorInventario([], mi_persistencia)
        # Al crear el objeto, se ejecuta automáticamente __init__()
        # y se configuran los atributos
        """
        self.inventario = inventario  # Guardamos la lista de libros
        self.persistencia = persistencia  # Guardamos el gestor de archivos
        self.archivo = "inventario.json"  # Nombre del archivo
        
        # Ahora self.inventario, self.persistencia y self.archivo
        # están disponibles en TODOS los métodos de la clase
    
    
    

    def agregar_libro(self):
        """
        AGREGAR UN NUEVO LIBRO:
        -----------------------
        Pide al usuario toda la información necesaria para crear
        un nuevo libro y lo agrega al inventario.
        """
        print("\n--- Agregar Nuevo Libro ---")
        
        # Pedir cada dato del libro usando las funciones de validación
        titulo = pedir_texto(" ¿Cual es el nombre del libro?: ")
        autor = pedir_texto(" ¿Cual es el autor?: ")
        categoria = pedir_texto(" ¿Cual es la categoria?: ")
        precio = pedir_float(" ¿Cual es el precio del titulo?: ")
        cantidad = pedir_int(" ¿Cual es la cantidad?: ")
        
        # Crear un DICCIONARIO con la información del libro
        libro = {
            "titulo": titulo,
            "autor": autor,
            "categoria": categoria,
            "precio": precio,
            "cantidad": cantidad
        }
        # Agregar el libro a la lista del inventario
        self.inventario.append(libro)
        # .append() agrega un elemento al final de una lista
        print(" libro agregado")
        
    def buscar_libro(self):
        """
        BUSCAR UN LIBRO POR TÍTULO:
        ---------------------------
        Busca un libro en el inventario por su título.
        Retorna el diccionario del libro si lo encuentra,
        o None si no lo encuentra.
        
        RETORNA:
        --------
        - dict: Diccionario con la información del libro (si se encuentra)
        - None: Si no se encuentra el libro
        """ 
        titulo = pedir_texto(" ¿Cual es el nombre del libro?: ")
        titulo_a_buscar = titulo.lower().strip()
        # Convertimos a minúsculas para que la búsqueda no distinga mayúsculas
        # "Python" == "python" == "PYTHON"
        
            # Recorrer todos los libros del inventario
        for libro in self.inventario:
            # Para cada libro, verificar si el título coincide
            
            # Obtener el título del libro actual y convertir a minúsculas
            titulo_libro = libro.get("titulo", "").lower().strip()
            if titulo_libro == titulo_a_buscar:
                    return libro  # ¡Libro encontrado! Retornar el diccionario
    
        # Si llegamos aquí, es porque no se encontró el libro
        print(f" Título: {titulo} no encontrado.")        
        return None  # Retornar None para indicar que no se encontró
        
        
    def eliminar_libro(self):
        """
        ELIMINAR UN LIBRO DEL INVENTARIO:
        ---------------------------------
        Busca un libro, muestra su información, pide confirmación
        y lo elimina si el usuario confirma.
        
        RETORNA:
        --------
        - True: Si el libro fue eliminado exitosamente
        - False: Si no se pudo eliminar (no existe o usuario canceló)
        """
        # PASO 1: Buscar el libro
        libro = self.buscar_libro()
    
        # PASO 2: Verificar si se encontró
        if libro is None:
            print(" No se puede eliminar un libro que no existe en el inventario.")
            return False
            
        # PASO 3: Mostrar información del libro
        mostrar_libro(libro) 
        
        # PASO 4: Pedir confirmación
        confirmacion = pedir_texto(f" ¿Seguro que deseas eliminar {libro.get("titulo")} ? (S/N): ").upper()
        
        # PASO 5: Verificar la respuesta
        if confirmacion not in  ("S", "si", "YES", "Y"):
            print(" Eliminación cancelada.")
            return False
        
        # PASO 6: Eliminar el libro
        self.inventario.remove(libro)
        # .remove() elimina un elemento específico de la lista
        
        print(f" libro eliminado exitosamente. ")
        return True
    
    def mostrar_inventario(self):
        """
        MOSTRAR TODOS LOS LIBROS:
        -------------------------
        Muestra la información de TODOS los libros en el inventario.
        """
        # Verificar si el inventario está vacío
        if not self.inventario:
            # 'not lista' es True si la lista está vacía
            print(" El inventario está vacío.")
            return # Salir de la función
        
        # Mostrar encabezado
        print(" Inventario de libros: ")
        
        # Recorrer todos los libros con enumerate()
        for conti, libro in enumerate(self.inventario, start=1):
            # enumerate() da tanto el índice como el elemento
            # start=1 hace que el conteo empiece en 1 (no en 0)
            # Ejemplo: [(1, libro1), (2, libro2), (3, libro3)]
            print(f" Libro {conti}: ")
            mostrar_libro(libro)
            
        # ===== FUNCIONES PARA ACTUALIZAR CADA CAMPO =====
        # Cada función actualiza UN campo específico del libro      

    def actualizar_titulo(self, libro): 
        """Actualiza el título del libro"""
        titulo_nuevo = pedir_texto("Nuevo título: ") 
        libro["titulo"] = titulo_nuevo  # Modificar el diccionario
        print(" Título actualizado.") 

    def actualizar_autor(self, libro):
        """Actualiza el autor del libro"""
        autor_nuevo = pedir_texto(" Nuevo autor: ")
        libro["autor"] = autor_nuevo
        print(" Autor actualizado. ")
        return

    def actualizar_categoria(self,libro):
        """Actualiza la categoría del libro"""
        categoria_nueva = pedir_texto(" Nueva categoria: ")
        libro["categoria"] = categoria_nueva
        print(" Categoria actualizada. ")
        return

    def actualizar_precio(self,libro):
        """Actualiza el precio del libro"""
        precio_nuevo = pedir_float(" Nuevo precio: ")
        libro["precio"] = precio_nuevo
        print(" precio actualizado. ")
        return  

    def actualizar_cantidad(self,libro):
        """Actualiza la cantidad del libro"""
        cantidad_nueva = pedir_int(" nueva cantidad:")   
        libro["cantidad"] = cantidad_nueva
        print(" cantidad actualizada. ")    
        return

    def actualizar_todas_opciones(self, libro):
        """Actualiza TODOS los campos del libro"""
        self.actualizar_titulo(libro)
        self.actualizar_autor(libro)
        self.actualizar_categoria(libro)
        self.actualizar_precio(libro)
        self.actualizar_cantidad(libro)
        print(" Se actualizó el libro completo.")
            
    def opcion_actualizar(self, libro, opcion):
        """
        EJECUTAR OPCIÓN DE ACTUALIZACIÓN:
        ----------------------------------
        Ejecuta la función correspondiente según la opción seleccionada.
        
        MATCH-CASE:
        -----------
        Es como un 'if-elif-else' más limpio.
        Compara 'opcion' con cada 'case' y ejecuta el código correspondiente.
        
        case _: es el caso por defecto (como 'else')
        """
        match opcion:
            case 0:
                print(" Actualización cancelada.")
                return None
            case 1:
                self.actualizar_titulo(libro)
            case 2:
                self.actualizar_autor(libro)
            case 3:
                self.actualizar_categoria(libro)   
            case 4:
                self.actualizar_precio(libro)
            case 5:
                self.actualizar_cantidad(libro)
            case 6:
                self.actualizar_todas_opciones(libro)
            case _:  # Cualquier otro número
                print(" Opción inválida.")
                
            
                        
    def menu_actualizar_libro(self, libro):
        """
        MENÚ DE ACTUALIZACIÓN:
        ----------------------
        Muestra las opciones de qué actualizar del libro.
        
        PARÁMETROS:
        -----------
        - libro (dict): El diccionario del libro a actualizar
        """
        print("\n¿Qué deseas actualizar?")
        print(" 0) cancelar. ")
        print(" 1) Titulo. ")
        print(" 2) Autor. ")
        print(" 3) Categoria. ")
        print(" 4) Precio. ")
        print(" 5) Cantidad. ")
        print(" 6) todas las opciones. ")
        
        opcion = pedir_int(" ¿Que opcion eliges?: ")
        self.opcion_actualizar(libro, opcion)
        return
    
    def actualizar_libro(self):
        """
        ACTUALIZAR UN LIBRO:
        --------------------
        Busca un libro y permite actualizar su información.
        
        RETORNA:
        --------
        - True: Si el libro fue actualizado
        - False: Si no se pudo actualizar (no existe)
        """
        # PASO 1: Buscar el libro
        libro = self.buscar_libro()
        
        # PASO 2: Verificar si existe
        if libro is None:
            print(" No se puede actualizar un libro que no existe en el inventario.")  
            return False
    
        # PASO 3: Mostrar menú de actualización
        self.menu_actualizar_libro(libro)
        return True    
    
    
    def menu(self):
        """
        MENÚ PRINCIPAL DEL INVENTARIO:
        -------------------------------
        Este método muestra el menú y ejecuta las opciones seleccionadas.
        
        Es un BUCLE INFINITO (while True) que solo termina cuando
        el usuario selecciona "Volver al menú principal".
        """
        while True:  # Bucle infinito
            # Mostrar el menú
            print("\n" + "="*50)  # Línea decorativa de 50 caracteres '='
            print(" GESTIÓN DE INVENTARIO")
            print("="*50)
            print("0. Volver al menú principal. ")
            print("1. Agregar libro. ")
            print("2. Actualizar libro. ")
            print("3. Eliminar libro. ")
            print("4. Buscar libro. ")
            print("5. Mostrar todos los libros. ")
             # Pedir al usuario que seleccione una opción
            opcion = pedir_int("\nSelecciona una opción: ")
            
            # Ejecutar la opción seleccionada
            if opcion == 1:
                self.agregar_libro()
            elif opcion == 2:
                self.actualizar_libro()
            elif opcion == 3:
                self.eliminar_libro()
            elif opcion == 4:
                libro = self.buscar_libro()
                if libro:  # Si se encontró un libro
                    mostrar_libro(libro)
            elif opcion == 5:
                self.mostrar_inventario()
            elif opcion == 0:
                self.guardar()  # Guardar antes de salir
                break  # Rompe el bucle while, sale del menú
            else:
                print(" Opción inválida")
                
    # ===== FUNCIONES AUXILIARES PARA OTROS MÓDULOS =====
    
    def obtener_libro_por_titulo(self, titulo):
        """
        Busca y retorna un libro por título (usado por el módulo de ventas).
        Similar a buscar_libro() pero sin imprimir mensajes.
        """
        titulo_a_buscar = titulo.lower().strip()
        for libro in self.inventario:
            if libro.get("titulo", "").lower().strip() == titulo_a_buscar:
                return libro
        return None 
    
    def actualizar_stock(self, titulo, cantidad):
        """
        Actualiza el stock de un libro (usado por el módulo de ventas).
        
        PARÁMETROS:
        -----------
        - titulo (str): Título del libro
        - cantidad (int): Cantidad a sumar (puede ser negativa para restar)
        """
        libro = self.obtener_libro_por_titulo(titulo)
        if libro:
            libro['cantidad'] += cantidad
            # += suma al valor actual
            # Ejemplo: si cantidad = 10 y cantidad = -3
            # entonces cantidad = 10 + (-3) = 7                       
    
    
    def guardar(self):
        """Guarda el inventario en el archivo JSON"""
        self.persistencia.guardar_datos(self.archivo, self.inventario)
        print(" Inventario guardado correctamente")        
            
           
# ============================================================================
# RESUMEN DE ESTE ARCHIVO:
# ============================================================================
# 
# FUNCIÓN GLOBAL:
# ---------------
# - mostrar_libro(libro): Muestra la información de un libro
# 
# CLASE: GestorInventario
# -----------------------
# Maneja todo lo relacionado con el inventario de libros.
# 
# ATRIBUTOS:
# ----------
# - self.inventario: Lista de libros
# - self.persistencia: Gestor para guardar/cargar datos
# - self.archivo: Nombre del archivo JSON
# 
# MÉTODOS PRINCIPALES:
# --------------------
# - menu(): Menú interactivo del inventario
# - agregar_libro(): Agrega un nuevo libro
# - buscar_libro(): Busca un libro por título
# - eliminar_libro(): Elimina un libro con confirmación
# - mostrar_inventario(): Muestra todos los libros
# - actualizar_libro(): Actualiza información de un libro
# 
# MÉTODOS DE ACTUALIZACIÓN:
# -------------------------
# - menu_actualizar_libro(): Menú de opciones de actualización
# - opcion_actualizar(): Ejecuta la opción seleccionada (usa match-case)
# - actualizar_titulo(), actualizar_autor(), etc.: Actualizan campos específicos
# 
# MÉTODOS AUXILIARES:
# -------------------
# - obtener_libro_por_titulo(): Para uso del módulo de ventas
# - actualizar_stock(): Para uso del módulo de ventas
# - guardar(): Guarda el inventario en JSON
# 
# CONCEPTOS CLAVE:
# ----------------
# 1. CLASE: Agrupa funciones y datos relacionados
# 2. SELF: Referencia al objeto mismo
# 3. __init__(): Constructor que inicializa el objeto
# 4. DICCIONARIO: Estructura de datos clave-valor
# 5. LISTA: Colección ordenada de elementos
# 6. MATCH-CASE: Estructura para comparar valores
# 7. MÉTODOS: Funciones dentro de una clase
# 
# ============================================================================       
            