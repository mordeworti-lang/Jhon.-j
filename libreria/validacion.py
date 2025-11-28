# ============================================================================
# ARCHIVO 1: validacion.py
# ============================================================================
# 
# PROPÓSITO: Este archivo contiene funciones auxiliares para validar datos
# que el usuario ingresa por teclado. Estas funciones se usan en TODOS los
# demás módulos para asegurar que los datos sean correctos.
#
# ============================================================================

def validacion(pregunta, tipo):
    """
    EXPLICACIÓN DETALLADA:
    ----------------------
    Esta es la función MÁS IMPORTANTE de validación. Se encarga de:
    1. Mostrar una pregunta al usuario
    2. Recibir su respuesta
    3. Verificar que la respuesta sea del tipo correcto (texto, número entero, decimal)
    4. Si la respuesta es incorrecta, volver a preguntar
    
    PARÁMETROS:
    -----------
    - pregunta (str): El texto que se le muestra al usuario
      Ejemplo: "¿Cuál es tu edad?: "
    
    - tipo (type): El tipo de dato que esperamos recibir
      Puede ser: str (texto), int (número entero), float (número decimal)
      Ejemplo: int, str, float
    
    RETORNA:
    --------
    El valor convertido al tipo solicitado
    
    CÓMO FUNCIONA PASO A PASO:
    --------------------------
    """
    while True:  # Este bucle se repite hasta que el usuario ingrese algo válido
        
        # PASO 1: Pedir al usuario que escriba algo
        opcion = input(pregunta)
        
        # PASO 2: Verificar que no esté vacío
        if opcion.strip() == "":  # .strip() quita espacios al inicio y final
            print("Inválido, escribe algo.")
            continue  # Vuelve al inicio del bucle (vuelve a preguntar)
        
        # PASO 3: Si esperamos un número (int o float), verificar que no sea negativo
        if tipo in (int, float) and opcion.startswith("-"):
            print("No puedes ingresar números negativos.")
            continue  # Vuelve a preguntar
         
        # PASO 4: Si el tipo es texto (str), devolver el texto en minúsculas y sin espacios
        if tipo == str:
            return opcion.lower().strip()
            # .lower() convierte a minúsculas: "HOLA" -> "hola"
            # .strip() quita espacios: "  hola  " -> "hola"
        
        # PASO 5: Intentar convertir el texto a número
        try:  
            return tipo(opcion)  # Convierte el texto al tipo solicitado
            # Si pedimos int: "25" -> 25
            # Si pedimos float: "19.99" -> 19.99
        
        # PASO 6: Si no se puede convertir, mostrar error y volver a preguntar
        except ValueError:
            print(f"No permitido, debe ser un {tipo.__name__}.")
            # tipo.__name__ da el nombre del tipo: int -> "int", float -> "float"


def pedir_int(pregunta):
    """
    EXPLICACIÓN DETALLADA:
    ----------------------
    Esta función pide un número ENTERO y POSITIVO al usuario.
    Es útil para pedir cantidades, edades, IDs, etc.
    
    PARÁMETROS:
    -----------
    - pregunta (str): El texto que se muestra al usuario
    
    RETORNA:
    --------
    Un número entero positivo (>= 0)
    
    EJEMPLO DE USO:
    ---------------
    cantidad = pedir_int("¿Cuántos libros?: ")
    # Si el usuario escribe "5" -> devuelve 5
    # Si el usuario escribe "-3" -> pide de nuevo
    # Si el usuario escribe "abc" -> pide de nuevo
    """
    while True:  # Bucle que se repite hasta obtener un número válido
        
        # Usar la función validacion() para obtener un entero
        numero = validacion(pregunta, int)
        
        # Verificar que sea positivo o cero
        if numero >= 0:
            return numero  # Si es válido, devolver el número
        else:
            print("Inválido, debe ser un número mayor o igual a 0.")
            # Si es negativo, volver a preguntar

    
def pedir_float(pregunta):
    """
    EXPLICACIÓN DETALLADA:
    ----------------------
    Esta función pide un número DECIMAL y POSITIVO al usuario.
    Es útil para pedir precios, pesos, medidas, etc.
    
    PARÁMETROS:
    -----------
    - pregunta (str): El texto que se muestra al usuario
    
    RETORNA:
    --------
    Un número decimal positivo (>= 0)
    
    EJEMPLO DE USO:
    ---------------
    precio = pedir_float("¿Cuál es el precio?: ")
    # Si el usuario escribe "19.99" -> devuelve 19.99
    # Si el usuario escribe "-5.5" -> pide de nuevo
    # Si el usuario escribe "abc" -> pide de nuevo
    """
    while True:  # Bucle que se repite hasta obtener un número válido
        
        # Usar la función validacion() para obtener un decimal
        numero = validacion(pregunta, float)
        
        # Verificar que sea positivo o cero
        if numero >= 0:
            return numero  # Si es válido, devolver el número
        else:
            print("Inválido, debe ser un número mayor o igual a 0.")
            # Si es negativo, volver a preguntar


def pedir_texto(pregunta):
    """
    EXPLICACIÓN DETALLADA:
    ----------------------
    Esta función pide un TEXTO al usuario.
    Es útil para pedir nombres, títulos, categorías, etc.
    
    PARÁMETROS:
    -----------
    - pregunta (str): El texto que se muestra al usuario
    
    RETORNA:
    --------
    Un texto en minúsculas y sin espacios al inicio/final
    
    EJEMPLO DE USO:
    ---------------
    nombre = pedir_texto("¿Cómo te llamas?: ")
    # Si el usuario escribe "  JUAN  " -> devuelve "juan"
    # Si el usuario escribe "María" -> devuelve "maría"
    """
    return validacion(pregunta, str)
    # Simplemente llama a validacion() con tipo str
    # validacion() ya se encarga de convertir a minúsculas y quitar espacios


# ============================================================================
# RESUMEN DE ESTE ARCHIVO:
# ============================================================================
# 
# Este archivo contiene 4 funciones:
# 
# 1. validacion(pregunta, tipo)
#    - Función base que valida cualquier tipo de dato
#    - Se asegura de que el usuario ingrese algo válido
#    - Maneja errores y vuelve a preguntar si es necesario
#
# 2. pedir_int(pregunta)
#    - Pide un número ENTERO positivo
#    - Usa validacion() internamente
#    - Ejemplo: cantidades, edades, IDs
#
# 3. pedir_float(pregunta)
#    - Pide un número DECIMAL positivo
#    - Usa validacion() internamente
#    - Ejemplo: precios, pesos, medidas
#
# 4. pedir_texto(pregunta)
#    - Pide un TEXTO
#    - Usa validacion() internamente
#    - Ejemplo: nombres, títulos, categorías
#
# VENTAJAS DE TENER ESTAS FUNCIONES:
# -----------------------------------
# - No repetimos código de validación en todo el programa
# - Garantizamos que TODOS los datos ingresados sean válidos
# - Si queremos cambiar cómo se validan los datos, solo modificamos este archivo
# - El código es más limpio y fácil de entender
#
# ============================================================================