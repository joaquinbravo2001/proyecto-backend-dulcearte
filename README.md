# Dulce Arte - Sistema de Gestión para Pastelería Artesanal

**Autor:** Joaquín Alonso Bravo Valenzuela  
**Proyecto:** Sistema de Trazabilidad y Gestión de Pedidos - Pastelería Artesanal  
**Tecnologías:** Python 3.12, Django 5.2, PostgreSQL / SQLite, Gunicorn y Nginx  

---

## Sobre el proyecto

Dulce Arte es una aplicación web pensada para resolver los problemas típicos de coordinación en una pastelería: desde que el cliente pide una torta personalizada, pasando por la verificación de ingredientes en bodega y la preparación en cocina, hasta la entrega final a domicilio.

### Módulos principales

- **Pedidos y cotizaciones:** Registro de clientes, especificaciones de diseño (sabores, colores, dedicatorias) y seguimiento de anticipos y saldos pendientes.
- **Taller de cocina (Kanban):** Tablero visual para organizar los pedidos por etapas (Recibido, En preparación, Horneado/Decorado, Control de calidad y Listo) con asignación de responsables y prioridades.
- **Inventario y recetas (BOM):** Descuento automático de stock según la receta técnica de cada producto y alertas cuando un insumo está bajo el mínimo.
- **Rutas de despacho:** Planificación de entregas con repartidor asignado, confirmación con firma digital y foto del comprobante.
- **Roles y seguridad:** Accesos diferenciados para Administrador, Vendedor, Cocinero, Bodeguero y Repartidor.

---

## Cómo ejecutarlo en local

1. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Preparar base de datos y cargar datos iniciales:**
   ```powershell
   # En PowerShell con SQLite:
   $env:USE_SQLITE="True"; python manage.py migrate
   $env:USE_SQLITE="True"; python datos_iniciales.py
   ```

3. **Iniciar el servidor:**
   ```powershell
   $env:USE_SQLITE="True"; python manage.py runserver
   ```
   *(También puedes hacer doble clic en `iniciar_servidor.bat`)*

- Aplicación: `http://localhost:8000/`
- Panel de Administración: `http://localhost:8000/admin/`

---

## Despliegue en AWS EC2

El proyecto cuenta con el script `deploy_aws.sh` para configurar automáticamente una instancia Ubuntu (22.04 / 24.04) con PostgreSQL, Gunicorn y Nginx:

1. Conectarse a la instancia por SSH:
   ```bash
   ssh -i "llave.pem" ubuntu@<ip-o-dns-instancia>
   ```
2. Copiar los archivos en `/home/ubuntu/dulce_arte`.
3. Ejecutar el instalador:
   ```bash
   cd /home/ubuntu/dulce_arte
   chmod +x deploy_aws.sh
   ./deploy_aws.sh
   ```
4. Recordar habilitar los puertos 22 (SSH) y 80 (HTTP) en el Security Group de AWS.

---

## Usuarios de prueba

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | admin | admin123 |
| Vendedor | vendedor1 | dulce123 |
| Cocinero | cocinero1 | dulce123 |
| Bodeguero | bodeguero1 | dulce123 |
| Repartidor | repartidor1 | dulce123 |
