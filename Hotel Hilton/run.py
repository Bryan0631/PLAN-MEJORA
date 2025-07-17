# run.py
from App import create_app, db # Importa create_app y db desde tu paquete App
import os # Aunque no lo usemos directamente aquí, es una buena práctica mantenerlo si se usó antes.

# Crea una instancia de la aplicación Flask
app = create_app()

if __name__ == '__main__':
    # Esto es útil para crear la base de datos y las tablas.
    # Se descomenta y ejecuta UNA SOLA VEZ la primera vez que configuras la aplicación.
    # Luego, se vuelve a COMENTAR (añadiendo el # al principio de cada línea)
    # para evitar que intente crear las tablas cada vez que inicias la app.
     with app.app_context():
         db.create_all()
         print("Base de datos y tablas creadas (si no existían).")
    
    # Inicia la aplicación Flask.
    # debug=True activa el modo de depuración (útil para desarrollo).
    # port=5000 es el puerto predeterminado.
    
app.run(debug=True, port=5000)