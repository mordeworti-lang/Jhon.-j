from PIL import Image

# Abre la imagen (usa el nombre correcto)
imagen = Image.open("flujo 1.jpg")

# Convierte y guarda como PDF
imagen.convert("RGB").save("diagrama.pdf")

print("✅ Se creó correctamente el archivo diagrama.pdf")
