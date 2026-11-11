# Evidencia de Uso de Inteligencia Artificial (IA)

## Proyecto 3: Sistema de Trazabilidad y Gestión de Pedidos para Pastelería Artesanal (Dulce Arte)

- **Estudiante / Desarrollador:** Joaquín Alonso Bravo Valenzuela
- **Asistente de IA utilizado:** Antigravity (Google DeepMind - Modelos Gemini y Claude Sonnet)
- **Framework & Stack:** Python 3.12, Django 5.2, PostgreSQL / SQLite (local fallback), Bootstrap 5, WhiteNoise, Gunicorn, Nginx.

---

### Registro Estructurado de Prompts y Resultados

#### 1. Configuración de Base de Datos y Arquitectura de Datos (Criterio 1)
- **Prompt:**
  > *"Diseña e implementa el esquema relacional en Django para la pastelería artesanal Dulce Arte conectado a PostgreSQL en AWS EC2. Incluye modelos para inventario (insumos, categorías, movimientos de stock), pedidos personalizados, Lista de Materiales (BOM), Kanban para cocina y rutas de despacho con comprobante/firma."*
- **Herramienta / IA:** Antigravity.
- **Resultado Obtenido:**
  - Creación de 10 modelos distribuidos modularmente en 5 apps: `pedidos` (`Cliente`, `ProductoBase`, `BOM`, `Pedido`, `ItemPedidoPersonalizado`), `inventario` (`Categoria`, `Insumo`, `MovimientoInventario`), `cocina` (`TareaKanban`, `HistorialKanban`), `despacho` (`RutaDespacho`, `EntregaPedido`) y `cuentas` (`PerfilUsuario`).
  - Definición de llaves foráneas (`ForeignKey`, `OneToOneField`), índices, validadores de stock positivo y campos calculados.

#### 2. Personalización del Administrador de Django (Criterio 2)
- **Prompt:**
  > *"Implementa la personalización avanzada del Django Admin para todos los modelos del sistema Dulce Arte. Agrega list_display, list_filter, search_fields, inlines (BOM y entregas), campos enriquecidos con format_html (badges de estado, semáforo de stock bajo, miniaturas de fotos) y personaliza los encabezados y títulos del admin."*
- **Herramienta / IA:** Antigravity.
- **Resultado Obtenido:**
  - Registro íntegro en `admin.py` para cada app con inlines (`BOMInline`, `EntregaInline`, `ItemPersonalizadoInline`), badges visuales por colores según estado y configuración de marca en `admin_config.py` (`🎂 Dulce Arte - Panel de Administración`).

#### 3. Operaciones CRUD y Lógica de Negocio Específica (Criterio 3)
- **Prompt:**
  > *"Codifica la lógica de negocio completa para las 4 funcionalidades clave: (1) Cotización y registro de pedidos personalizados, (2) Tablero Kanban de cocina con 5 etapas y avance automático con historial, (3) Descuento automático de insumos según Lista de Materiales (BOM) con verificación de stock suficiente y registro de movimientos de inventario, (4) Creación de rutas de entrega y confirmación con firma digital y comprobante fotográfico."*
- **Herramienta / IA:** Antigravity.
- **Resultado Obtenido:**
  - Métodos `Pedido.descontar_inventario()`, `Insumo.descontar_stock()`, `TareaKanban.avanzar_estado()` y `EntregaPedido.confirmar_entrega()`.
  - Formularios y vistas CRUD para cada módulo (`pedidos`, `inventario`, `cocina`, `despacho`).
  - Creación y verificación de interfaz visual con tablero Kanban por columnas dinámicas.

#### 4. Seguridad, Autenticación y Manejo de Sesiones (Criterio 4)
- **Prompt:**
  > *"Asegura la aplicación restringiendo el acceso no autenticado mediante el decorador @login_required en todas las vistas de gestión. Crea un formulario y vista de login personalizado, redirecciones post-login/logout y roles de usuario (admin, vendedor, cocinero, bodeguero, repartidor)."*
- **Herramienta / IA:** Antigravity.
- **Resultado Obtenido:**
  - Implementación de `CustomLoginView` con template responsivo decorado al estilo pastelería.
  - Protección de endpoints con `@login_required` y roles asignados a través de `PerfilUsuario`.

#### 5. Script de Despliegue en AWS EC2 (Criterio 5)
- **Prompt:**
  > *"Genera un script bash automatizado (deploy_aws.sh) y guía de configuración para desplegar la aplicación en una instancia Ubuntu EC2 con PostgreSQL, Gunicorn como servicio systemd, Nginx como reverse proxy y WhiteNoise para estáticos."*
- **Herramienta / IA:** Antigravity.
- **Resultado Obtenido:**
  - Script ejecutable `deploy_aws.sh` con aprovisionamiento de PostgreSQL, entorno virtual, migraciones, configuración de Gunicorn y Nginx con puerto 80 abierto a la IP pública.
