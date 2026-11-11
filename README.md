# 🎂 Dulce Arte — Sistema de Trazabilidad y Gestión de Pedidos para Pastelería Artesanal

**Desarrollado por:** Joaquín Alonso Bravo Valenzuela  
**Asignatura / Proyecto:** Sistema de Trazabilidad y Gestión de Pedidos - Pastelería Artesanal Dulce Arte  
**Año:** 2026

Sistema integral end-to-end desarrollado en **Python 3.12** y **Django 5.2** para resolver la falta de coordinación entre la toma de pedidos personalizados, disponibilidad de insumos en bodega y tiempos de cocina.

---

## 🚀 Resumen del Sistema y Funcionalidades Clave

1. **Cotización y Registro de Pedidos Personalizados**:
   - Registro de clientes, productos base, especificaciones de diseño personalizadas (sabores, colores, textos).
   - Generación automática de número de pedido (`DA-YYYY-XXXX`), control de anticipos, saldo pendiente y fechas/horas de entrega.
2. **Tablero Kanban Digital para Taller de Cocina**:
   - Estados de flujo: `Recibido`, `En Preparación`, `Horneado/Decorado`, `Control de Calidad` y `Listo`.
   - Prioridades visuales (Baja, Normal, Alta, Urgente), asignación de repostero/cocinero responsable y registro histórico de transiciones (`HistorialKanban`).
3. **Lista de Materiales (BOM - Bill of Materials) y Control de Inventario**:
   - Cada producto base tiene su receta técnica con cantidades de insumos.
   - Descuento automático de stock de bodega al confirmar el pedido, con validación de stock disponible y registro de trazabilidad en `MovimientoInventario`.
   - Alertas de stock bajo el mínimo en Dashboard e Inventario.
4. **Módulo de Gestión de Rutas de Despacho**:
   - Planificación de rutas con repartidor asignado y cola de entregas ordenadas.
   - Confirmación de entrega mediante receptor, **firma digital** y **comprobante fotográfico**, sincronizando el estado final del pedido a `Entregado`.
5. **Seguridad y Control de Acceso por Roles**:
   - Vistas protegidas con `@login_required`.
   - Perfiles de usuario por rol: Administrador, Vendedor, Cocinero, Bodeguero y Repartidor.
6. **Administrador de Django Personalizado**:
   - Registro completo de modelos con filtros, búsquedas, inlines tabulares (`BOMInline`, `EntregaInline`, `ItemPersonalizadoInline`) y semáforos/badges visuales renderizados con `format_html`.

---

## 📁 Estructura del Proyecto

```text
tema 3/
├── manage.py
├── requirements.txt
├── .env.example
├── deploy_aws.sh                  # Script de despliegue automatizado en AWS EC2
├── prompts_ia.md                  # Evidencia y registro de uso de IA (Criterio 4)
├── datos_iniciales.py             # Script de carga de datos iniciales
├── dulce_arte/                    # Configuración principal de Django
│   ├── settings.py                # Conexión PostgreSQL (AWS) / Fallback SQLite local
│   ├── urls.py
│   ├── wsgi.py
│   └── admin_config.py            # Personalización de marca en Admin
├── pedidos/                       # Cotizaciones, pedidos y BOM
├── inventario/                    # Insumos, categorías y movimientos
├── cocina/                        # Tablero Kanban e historial de producción
├── despacho/                      # Rutas de despacho, firma y fotos
├── cuentas/                       # Autenticación, perfiles y roles
├── templates/                     # Templates Bootstrap 5 responsivos
└── static/                        # CSS temático de pastelería artesanal
```

---

## 🛠️ Ejecución en Entorno Local

1. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Aplicar migraciones**:
   - En local con SQLite:
     ```bash
     # En PowerShell:
     $env:USE_SQLITE="True"; python manage.py migrate
     $env:USE_SQLITE="True"; python datos_iniciales.py
     ```
   - O con PostgreSQL local: configurar variables en entorno y ejecutar `python manage.py migrate`.
3. **Iniciar servidor de desarrollo**:
   ```bash
   $env:USE_SQLITE="True"; python manage.py runserver
   ```
4. **Acceder**:
   - Sistema Web: `http://localhost:8000/`
   - Panel de Administración: `http://localhost:8000/admin/`

---

## ☁️ Despliegue en AWS EC2 (PostgreSQL + Gunicorn + Nginx)

El script `deploy_aws.sh` automatiza el 100% de la configuración en una instancia Ubuntu EC2:

1. Conéctate a tu instancia EC2 por SSH:
   ```bash
   ssh -i "tu-llave.pem" ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
   ```
2. Clona o copia los archivos del proyecto en `/home/ubuntu/dulce_arte`.
3. Ejecuta el script de despliegue:
   ```bash
   cd /home/ubuntu/dulce_arte
   chmod +x deploy_aws.sh
   bash deploy_aws.sh
   ```
4. Asegúrate de tener habilitado el puerto **80** (HTTP) y **5432** (PostgreSQL si aplica) en el **Security Group** de AWS.

---

## 👥 Credenciales de Prueba (Precargadas)

| Rol | Usuario | Contraseña |
|---|---|---|
| **Administrador (Superuser)** | `admin` | `admin123` |
| **Vendedor** | `vendedor1` | `dulce123` |
| **Cocinero / Taller** | `cocinero1` | `dulce123` |
| **Bodeguero / Inventario** | `bodeguero1` | `dulce123` |
| **Repartidor / Despacho** | `repartidor1` | `dulce123` |
