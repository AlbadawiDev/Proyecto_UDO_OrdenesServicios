# run.py
"""
Punto de entrada de la aplicación
"""
from app import create_app

app = create_app() 

if __name__ == '__main__':
    print(" Iniciando Sistema de Órdenes de Servicio...")
    print(" URL: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)