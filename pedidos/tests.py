from django.test import TestCase
from django.utils import timezone
from inventario.models import Categoria, Insumo
from pedidos.models import Cliente, ProductoBase, BOM, Pedido
from cocina.models import TareaKanban
from despacho.models import RutaDespacho, EntregaPedido

class DulceArteIntegrationTests(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Harinas')
        self.harina = Insumo.objects.create(
            nombre='Harina Especial', categoria=self.cat, unidad_medida='kg',
            stock_actual=10, stock_minimo=2, costo_unitario=1000
        )
        self.cliente = Cliente.objects.create(nombre='Ana Perez', telefono='+56999999999')
        self.producto = ProductoBase.objects.create(nombre='Torta de Fresa', precio_base=25000)
        self.bom = BOM.objects.create(producto=self.producto, insumo=self.harina, cantidad=0.5)

    def test_flujo_completo_pedido_bom_cocina_despacho(self):
        # 1. Crear Pedido
        pedido = Pedido.objects.create(
            cliente=self.cliente, producto=self.producto, cantidad=2,
            descripcion_personalizada='Decoración con fresas frescas',
            fecha_entrega=timezone.now() + timezone.timedelta(days=1),
            precio_total=50000, estado='confirmado'
        )
        self.assertTrue(pedido.numero.startswith('DA-'))

        # 2. Descuento automático de inventario según BOM
        pedido.descontar_inventario()
        self.harina.refresh_from_db()
        self.assertEqual(float(self.harina.stock_actual), 9.0)  # 10 - (0.5 * 2)

        # 3. Flujo Kanban Cocina
        tarea = TareaKanban.objects.create(pedido=pedido)
        self.assertEqual(tarea.estado, 'recibido')
        tarea.avanzar_estado()  # en_preparacion
        tarea.avanzar_estado()  # horneado_decorado
        tarea.avanzar_estado()  # control_calidad
        tarea.avanzar_estado()  # listo
        self.assertEqual(tarea.estado, 'listo')
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, 'listo')

        # 4. Despacho y entrega
        ruta = RutaDespacho.objects.create(nombre='Ruta Mañana', fecha_despacho=timezone.now().date())
        entrega = EntregaPedido.objects.create(
            ruta=ruta, pedido=pedido, orden_entrega=1, direccion_entrega='Av. Central 123'
        )
        entrega.confirmar_entrega(receptor='Ana Perez')
        self.assertEqual(entrega.estado, 'entregado')
        pedido.refresh_from_db()
        self.assertEqual(pedido.estado, 'entregado')
