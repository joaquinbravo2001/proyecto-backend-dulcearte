"""
Script para cargar datos iniciales de prueba en Dulce Arte.
Ejecutar con: python manage.py shell < datos_iniciales.py
O como script: python datos_iniciales.py (si se configura Django)
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dulce_arte.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Categoria, Insumo
from pedidos.models import Cliente, ProductoBase, BOM

print("Creando superusuario...")
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@dulcearte.cl', 'admin123')
    print("  ✓ admin / admin123")

print("Creando usuarios...")
roles_usuarios = [
    ('vendedor1', 'vendedor', 'Ana', 'González'),
    ('cocinero1', 'cocinero', 'Carlos', 'Rodríguez'),
    ('camila.valenzuela', 'cocinero', 'Camila', 'Valenzuela'),
    ('matias.herrera', 'cocinero', 'Matías', 'Herrera'),
    ('sofia.miranda', 'cocinero', 'Sofía', 'Miranda'),
    ('ignacio.pasteles', 'cocinero', 'Ignacio', 'Alarcón'),
    ('bodeguero1', 'bodeguero', 'María', 'López'),
    ('repartidor1', 'repartidor', 'Pedro', 'Soto'),
]
from cuentas.models import PerfilUsuario
for username, rol, first, last in roles_usuarios:
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username, f'{username}@dulcearte.cl', 'dulce123', first_name=first, last_name=last)
        PerfilUsuario.objects.create(usuario=u, rol=rol)
        print(f"  ✓ {username} / dulce123")

print("Creando categorías...")
cats = {
    'Harinas': Categoria.objects.get_or_create(nombre='Harinas', defaults={'descripcion': 'Harinas y almidones'})[0],
    'Lácteos': Categoria.objects.get_or_create(nombre='Lácteos', defaults={'descripcion': 'Leche, crema, mantequilla'})[0],
    'Azúcares': Categoria.objects.get_or_create(nombre='Azúcares', defaults={'descripcion': 'Azúcares y endulzantes'})[0],
    'Huevos': Categoria.objects.get_or_create(nombre='Huevos y Derivados', defaults={'descripcion': 'Huevos frescos'})[0],
    'Saborizantes': Categoria.objects.get_or_create(nombre='Saborizantes', defaults={'descripcion': 'Vainilla, cacao, etc.'})[0],
    'Decoración': Categoria.objects.get_or_create(nombre='Decoración', defaults={'descripcion': 'Fondant, colorantes, perlas'})[0],
}

print("Creando insumos...")
insumos_data = [
    ('Harina de trigo', 'Harinas', 'kg', 25, 5, 850),
    ('Mantequilla sin sal', 'Lácteos', 'kg', 8, 2, 4200),
    ('Azúcar blanca', 'Azúcares', 'kg', 20, 5, 650),
    ('Azúcar flor', 'Azúcares', 'kg', 10, 3, 1200),
    ('Huevos frescos', 'Huevos', 'u', 120, 24, 150),
    ('Leche entera', 'Lácteos', 'l', 15, 5, 950),
    ('Crema de leche', 'Lácteos', 'l', 8, 2, 2800),
    ('Extracto de vainilla', 'Saborizantes', 'ml', 500, 100, 8),
    ('Cacao en polvo', 'Saborizantes', 'kg', 3, 1, 5500),
    ('Fondant blanco', 'Decoración', 'kg', 5, 1, 7000),
    ('Colorantes alimentarios', 'Decoración', 'u', 20, 5, 1500),
    ('Chocolate cobertura', 'Lácteos', 'kg', 4, 1, 8500),
    ('Polvo de hornear', 'Saborizantes', 'kg', 2, 0.5, 3200),
    ('Sal fina', 'Saborizantes', 'kg', 3, 1, 400),
]
insumos_obj = {}
for nombre, cat_key, unidad, stock, stock_min, costo in insumos_data:
    obj, _ = Insumo.objects.get_or_create(nombre=nombre, defaults={
        'categoria': cats[cat_key], 'unidad_medida': unidad,
        'stock_actual': stock, 'stock_minimo': stock_min, 'costo_unitario': costo
    })
    insumos_obj[nombre] = obj
print(f"  ✓ {len(insumos_obj)} insumos")

print("Creando clientes...")
clientes_data = [
    ('Valentina Muñoz', '+56912345678', 'valeria@gmail.com', 'Av. Providencia 1234, Santiago'),
    ('Rodrigo Fernández', '+56987654321', 'rodrigo@empresa.cl', 'Las Condes 567, Santiago'),
    ('Daniela Castro', '+56911223344', '', 'Ñuñoa 890, Santiago'),
    ('Empresa Eventos SA', '+56922334455', 'eventos@empresa.cl', 'Vitacura 2345, Santiago'),
]
clientes = []
for nombre, tel, email, dir in clientes_data:
    c, _ = Cliente.objects.get_or_create(nombre=nombre, defaults={'telefono': tel, 'email': email, 'direccion': dir})
    clientes.append(c)
print(f"  ✓ {len(clientes)} clientes")

print("Creando productos base...")
productos_data = [
    ('Torta de Chocolate', 'Torta húmeda de chocolate con ganache y decoración personalizada', 35000, 8),
    ('Torta de Vainilla', 'Torta esponjosa de vainilla con crema chantilly y fresas', 28000, 6),
    ('Cupcakes x12', 'Docena de cupcakes decorados temáticamente', 18000, 4),
    ('Torta Fondant Personalizada', 'Torta multicapa con fondant y decoración personalizada 3D', 65000, 12),
    ('Pie de Limón', 'Pie de limón con merengue tostado', 15000, 3),
]
productos = []
for nombre, desc, precio, tiempo in productos_data:
    p, _ = ProductoBase.objects.get_or_create(nombre=nombre, defaults={
        'descripcion': desc, 'precio_base': precio, 'tiempo_preparacion_horas': tiempo
    })
    productos.append(p)
print(f"  ✓ {len(productos)} productos")

print("Creando BOM (Lista de Materiales)...")
bom_data = {
    'Torta de Chocolate': [
        ('Harina de trigo', '0.5'), ('Mantequilla sin sal', '0.2'), ('Azúcar blanca', '0.3'),
        ('Huevos frescos', '4'), ('Cacao en polvo', '0.1'), ('Leche entera', '0.25'),
        ('Polvo de hornear', '0.01'), ('Sal fina', '0.005'), ('Chocolate cobertura', '0.3'),
    ],
    'Torta de Vainilla': [
        ('Harina de trigo', '0.5'), ('Mantequilla sin sal', '0.2'), ('Azúcar blanca', '0.3'),
        ('Huevos frescos', '4'), ('Leche entera', '0.25'), ('Extracto de vainilla', '15'),
        ('Polvo de hornear', '0.01'), ('Crema de leche', '0.3'),
    ],
    'Cupcakes x12': [
        ('Harina de trigo', '0.3'), ('Mantequilla sin sal', '0.15'), ('Azúcar blanca', '0.2'),
        ('Huevos frescos', '3'), ('Leche entera', '0.15'), ('Extracto de vainilla', '10'),
        ('Polvo de hornear', '0.008'), ('Azúcar flor', '0.2'),
    ],
    'Torta Fondant Personalizada': [
        ('Harina de trigo', '0.8'), ('Mantequilla sin sal', '0.4'), ('Azúcar blanca', '0.5'),
        ('Huevos frescos', '8'), ('Fondant blanco', '1'), ('Colorantes alimentarios', '3'),
        ('Extracto de vainilla', '20'), ('Crema de leche', '0.5'),
    ],
}
for prod_nombre, items in bom_data.items():
    prod = ProductoBase.objects.filter(nombre=prod_nombre).first()
    if prod:
        for insumo_nombre, cant in items:
            insumo = insumos_obj.get(insumo_nombre)
            if insumo:
                BOM.objects.get_or_create(producto=prod, insumo=insumo, defaults={'cantidad': cant})
print("  ✓ BOM creados")

print("\n✅ DATOS INICIALES CARGADOS CORRECTAMENTE")
print("\nUsuarios disponibles:")
print("  admin / admin123 (Superusuario)")
print("  vendedor1 / dulce123")
print("  cocinero1 / dulce123")
print("  bodeguero1 / dulce123")
print("  repartidor1 / dulce123")
