import flet as ft
from restaurante import Restaurante
from mesa import Mesa
from clientes import Cliente


class RestauranteGUI:
    def __init__(self):
        self.restaurante = Restaurante()
        capacidades = [2, 2, 4, 5, 6, 7]
        for i in range(1, 7):
            self.restaurante.agregar_mesa(Mesa(i, capacidades[i - 1]))

    def main(self, page: ft.Page):
        # Configuración inicial de la página
        page.title = "Sistema de restaurante"
        page.padding = 20
        page.theme_mode = ft.ThemeMode.DARK

        # Texto de bienvenida
        text = ft.Text("Sistema de restaurante iniciado",
                       size=20, color="blue")

        # Tabs con contenido
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Mesera",
                    icon=ft.icons.PERSON,
                    content=self.crear_vista_mesera()
                ),
                ft.Tab(
                    text="Cocina",
                    icon=ft.icons.RESTAURANT,
                    content=self.crear_vista_cocina()
                ),
                ft.Tab(
                    text="Caja",
                    icon=ft.icons.POINT_OF_SALE,
                    content=self.crear_vista_caja()
                ),
                ft.Tab(
                    text="Administración",
                    icon=ft.icons.ADMIN_PANEL_SETTINGS,
                    content=self.crear_vista_admin()
                ),
            ],
            expand=1
        )

        # Agregar componentes a la página
        page.add(text, tabs)

    # Métodos de vistas
    def crear_vista_mesera(self):
        self.grid_container = ft.Container(
            content=self.crear_grid_mesas(),
            width=700,
            expand=True
        )
        return ft.Row(
            controls=[
                ft.Container(
                    width=700,
                    content=ft.Column(controls=[
                        ft.Text(value="Mesas del Restaurante",
                                size=20, weight=ft.FontWeight.BOLD),
                        self.grid_container
                    ], expand=True),
                    expand=True
                ),
                ft.VerticalDivider(),
                ft.Container(
                    width=400,
                    content=self.crear_panel_gestion(),
                    expand=True
                )
            ],
            expand=True,
            spacing=0
        )
    def crear_vista_cocina(self):
        self.lista_pedidos_cocina = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True
        )
        def cambiar_estado_pedido(e, pedido, nuevo_estado):
                pedido.cambiar_estado(nuevo_estado)
                self.actualizar_vista_cocina()
                self.actualizar_ui(e.page)
                e.page.update()

        def crear_item_pedido(pedido):
            return ft.Container(
                content=ft.Column([
                    ft.Text(value=f"Mesa {pedido.mesa.numero}",size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(pedido.obtener_resumen()),
                    ft.Row([
                        ft.ElevatedButton(
                            text="En preparacion",
                            on_click=lambda e, p=pedido: cambiar_estado_pedido(e, p, "En Preparacion"),
                            disabled=pedido.estado != "Pendiente",
                            style=ft.ButtonStyle( bgcolor=ft.Colors.ORANGE_700,color=ft.Colors.WHITE,)
                            ),
                        ft.ElevatedButton(
                            text="Listo",
                            on_click=lambda e, p=pedido: cambiar_estado_pedido(e, p, "Listo"),
                            disabled=pedido.estado != "En Preparacion",
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE
                            )),
                        ft.Text(value=f"Estado:{pedido.estado}", color=ft.Colors.BLUE_200)
                        ])
                ]),
                bgcolor=ft.Colors.BLUE_GREY_900,
                padding=10,
                border_radius=10
            )
        def actualizar_vista_cocina():
            self.lista_pedidos_cocina.controls.clear()
            for pedido in self.restaurante.pedidos_activos:
                if pedido.estado in ["Pendiente", "En Preparacion"]:
                    self.lista_pedidos_cocina.controls.append(crear_item_pedido(pedido))
                    
        self.actualizar_vista_cocina = actualizar_vista_cocina
        return ft.Container(
            content=ft.Column([
                ft.Text(value="Pedidos Pedientes", size=24, weight=ft.FontWeight.BOLD),
                self.lista_pedidos_cocina
            ]),
            expand=True
        )
    def crear_vista_caja(self):
        self.lista_caja = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True
        )
        def procesar_pago(e, mesa):
            if mesa.pedido_actual:
                self.restaurante.liberar_mesa(mesa.numero)
                self.actualizar_ui(e.page)
                
        def crear_item_cuenta(mesa):
            if not mesa.pedido_actual:
                return None
            return ft.Container(
                content=ft.Column([
                    ft.Text(f"Mesa {mesa.numero}",size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Cliente: {mesa.cliente.id}"),
                    ft.Text(mesa.pedido_actual.obtener_resumen()),
                    ft.ElevatedButton(
                        text="Procesar Pago",
                        on_click=lambda e, m=mesa: procesar_pago(e,m),
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE,
                        )
                    )
                ]),
                bgcolor=ft.Colors.BLUE_GREY_900,
                padding=10,
                border_radius=10
        )
        def actualizar_vista_caja():
            self.lista_caja.controls.clear()
            for mesa in self.restaurante.mesas:
                if mesa.ocupada and mesa.pedido_actual:
                    item=crear_item_cuenta(mesa)
                    if item:
                        self.lista_caja.controls.append(item)
        self.actualizar_vista_caja = actualizar_vista_caja   
        return ft.Container(
            content=ft.Column([
                ft.Text("Cuentas Activas", size=24, weight=ft.FontWeight.BOLD),
                self.lista_caja
            ]),
            expand=True
        )
    def crear_vista_admin(self):
        self.tipo_item_admin = ft.Dropdown(
            label="Tipo de Item",
            options=[
                ft.dropdown.Option("Entrada"),
                ft.dropdown.Option("Plato Principal"),
                ft.dropdown.Option("Postre"),
                ft.dropdown.Option("Bebida"),
            ],
            width=200,
        )
        self.nombre_item = ft.TextField(label="Nombre del Item", width=200,)
        self.precio_item = ft.TextField(label="Precio", width=200,input_filter=ft.NumbersOnlyInputFilter)
        self.tipo_item_eliminar = ft.Dropdown(
            label="Tipo de Item",
            options=[
                ft.dropdown.Option("Entrada"),
                ft.dropdown.Option("Plato Principal"),
                ft.dropdown.Option("Postre"),
                ft.dropdown.Option("Bebida"),
            ],
            width=200,
            on_change=self.actualizar_items_eliminar
        )
        self.item_eliminar = ft.Dropdown(
            label="Seleccionar item a eliminar",
            width=200,
        )
        
        def agregar_item(e):
            tipo = self.tipo_item_admin.value
            nombre = self.nombre_item.value
            try:
                precio = float(self.precio_item.value)
                if tipo and nombre and precio > 0:
                    if tipo == "Entrada":
                        self.restaurante.menu.agregar_entrada(nombre, precio)
                    elif tipo == "Plato Principal":
                        self.restaurante.menu.agregar_platos_principales(nombre,precio)
                    elif tipo == "Postre":
                        self.restaurante.menu.agregar_postres(nombre, precio)
                    elif tipo == "Bebida":
                        self.restaurante.menu.agregar_bebidas(nombre, precio)
                    
                    self.nombre_item.value = ""
                    self.precio_item.value = ""

                    self.actualizar_items_menu(None)
                    self.actualizar_items_eliminar(None)
                    e.page.update()
            except ValueError:
                pass
               
        def eliminar_item(e):
            tipo = self.tipo_item_eliminar.value
            nombre = self.item_eliminar.value
            if tipo and nombre:
                self.restaurante.menu.eliminar_item(tipo, nombre)
                self.actualizar_items_menu(None)
                self.actualizar_items_eliminar(None)
                e.page.update()     
                
        return ft.Container(
            content=ft.Column([
                ft.Text("Agregar Item al Menu", size=20, weight=ft.FontWeight.BOLD),
                self.tipo_item_admin,
                self.nombre_item,
                self.precio_item,
                ft.ElevatedButton(
                    text="Agregar Item",
                    on_click=agregar_item,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.GREEN_700,
                        color=ft.Colors.WHITE,
                    )
                ),
                ft.Divider(),
                ft.Text("Eliminar item del menu", size=20, weight=ft.FontWeight.BOLD),
                self.tipo_item_eliminar,
                self.item_eliminar,
                ft.ElevatedButton(
                    text="Eliminar item",
                    on_click=eliminar_item,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.RED_700,
                        color=ft.Colors.WHITE,
                    )
                ),
            ], spacing=20),
            padding=20,
            bgcolor=ft.Colors.BLUE_GREY_900,
        )
    # Métodos internos de vistas
    def actualizar_items_eliminar(self, e):
        tipo = self.tipo_item_eliminar.value
        self.item_eliminar.options= []
        
        if tipo == "Entrada":
            items = self.restaurante.menu.entradas
        elif tipo == "Plato Principal":
            items = self.restaurante.menu.platos_principales
        elif tipo == "Postre":
            items = self.restaurante.menu.postres
        elif tipo == "Bebida":
            items = self.restaurante.menu.bebidas            
        else:
            items = []
        self.item_eliminar.options = [
            ft.dropdown.Option(item.nombre) for item in items
        ]
        if e and e.page:
            e.page.update()
            
            
        

    def crear_grid_mesas(self):
        grid = ft.GridView(
            expand=1,
            runs_count=2,
            max_extent=200,  # Tamaño máximo de cada elemento de la grilla
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
            padding=10
        )
        for mesa in self.restaurante.mesas:
            color = ft.colors.GREEN_400 if not mesa.ocupada else ft.colors.RED_700
            estado = "LIBRE" if not mesa.ocupada else "OCUPADA"
            grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.icons.TABLE_RESTAURANT,
                                            color="black"),
                                    ft.Text(
                                        value=f"Mesa {mesa.numero}", size=16, weight=ft.FontWeight.BOLD),
                                ]
                            ),
                            ft.Text(
                                value=f"Capacidad: {mesa.tamaño} personas", size=14),
                            ft.Text(
                                value=f"Estado: {estado}", size=14, color=ft.Colors.WHITE, width=ft.FontWeight.BOLD),
                        ]
                    ),
                    bgcolor=color,
                    border_radius=10,
                    padding=15,
                    ink=True,  # da efecto de presionar el botón
                    on_click=lambda e, num=mesa.numero: self.seleccionar_mesa(e, num),
                )
            )
        return grid
    def actualizar_ui(self, page):
        nuevo_grid = self.crear_grid_mesas()
        self.grid_container.content = nuevo_grid
        if self.mesa_seleccionada:
            if self.mesa_seleccionada.ocupada and self.mesa_seleccionada.pedido_actual:
                self.resumen_pedido.value = self.mesa_seleccionada.pedido_actual.obtener_resumen()
            else:
                self.resumen_pedido.value = ""
            self.asignar_btn.disabled = self.mesa_seleccionada.ocupada
            self.agregar_item_btn.disabled = not self.mesa_seleccionada.ocupada
            self.liberar_btn.disabled = not self.mesa_seleccionada.ocupada
            
        self.actualizar_vista_cocina()
        self.actualizar_vista_caja()
        page.update()

    def seleccionar_mesa(self, e, numero_mesa):
        self.mesa_seleccionada = self.restaurante.buscar_mesa(numero_mesa)
        mesa = self.mesa_seleccionada

        self.mesa_info.value = f"Mesa {mesa.numero} - Capacidad {mesa.tamaño} personas."
        self.asignar_btn.disabled = mesa.ocupada
        self.agregar_item_btn.disabled = not mesa.ocupada
        self.liberar_btn.disabled = not mesa.ocupada

        if mesa.ocupada and mesa.pedido_actual:
            self.resumen_pedido.value = mesa.pedido_actual.obtener_resumen()
        else:
            self.resumen_pedido.value = ""

        e.page.update()
        return None

    def crear_panel_gestion(self):
        self.mesa_seleccionada = None
        self.mesa_info = ft.Text(value="", size=16, weight=ft.FontWeight.BOLD)
        self.tamaño_grupo_input = ft.TextField(
            label="Tamaño del Grupo",
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.Icons.PEOPLE,
        )
        self.tipo_item_dropdown = ft.Dropdown(
            label="Tipo de Item",
            options=[
                ft.dropdown.Option("Entrada"),
                ft.dropdown.Option("Plato Principal"),
                ft.dropdown.Option("Postre"),
                ft.dropdown.Option("Bebida")
            ],
            width=200,
            on_change=self.actualizar_items_menu
        )
        self.items_dropdown = ft.Dropdown(
            label="Seleccionar Item",
            width=200,
        )
        self.asignar_btn = ft.ElevatedButton(
            text="Asignar Cliente",
            on_click=self.asignar_cliente,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
            )
        )
        self.liberar_btn = ft.ElevatedButton(
            text="Liberar Mesa",
            on_click=self.liberar_mesa,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE,
            )
        )
        self.agregar_item_btn = ft.ElevatedButton(
            text="Agregar Item",
            on_click=self.agregar_item_pedido,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE
            )
        )
        self.resumen_pedido = ft.Text("", size=14)
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.mesa_info,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=10,
                    ),
                    ft.Container(height=20),
                    self.tamaño_grupo_input,
                    self.asignar_btn,
                    ft.Divider(),
                    self.tipo_item_dropdown,
                    self.items_dropdown,
                    self.agregar_item_btn,
                    ft.Divider(),
                    self.liberar_btn,
                    ft.Divider(),
                    ft.Text(value="Resumen del pedido",
                            size=16, weight=ft.FontWeight.BOLD),
                    ft.Container(
                        content=self.resumen_pedido,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=10,
                    ),

                ],
                spacing=10,
                expand=True
            ),
            padding=20,
            expand=True
        )

    def agregar_item_pedido(self, e):
        if not self.mesa_seleccionada or not self.mesa_seleccionada.pedido_actual:
            return

        tipo = self.tipo_item_dropdown.value
        nombre_item = self.items_dropdown.value

        if tipo and nombre_item:
            item = self.restaurante.obtener_item_menu(tipo, nombre_item)
            if item:
                self.mesa_seleccionada.pedido_actual.agregar_item(item)
                self.actualizar_ui(e.page)

    def liberar_mesa(self, e):
        if self.mesa_seleccionada:
            self.restaurante.liberar_mesa(self.mesa_seleccionada.numero)
            self.actualizar_ui(e.page)

    def asignar_cliente(self, e):
        if not self.mesa_seleccionada:
            return
        try:
            tamaño_grupo = int(self.tamaño_grupo_input.value)
            if tamaño_grupo <= 0:
                return
            cliente = Cliente(tamaño_grupo)
            resultado = self.restaurante.asignar_cliente_a_mesa(
                cliente, self.mesa_seleccionada.numero)

            if "asignado" in resultado:
                self.restaurante.crear_pedido(self.mesa_seleccionada.numero)
                self.tamaño_grupo_input.value = ""
                self.actualizar_ui(e.page)
        except ValueError:
            pass

    def actualizar_items_menu(self, e):
        tipo = self.tipo_item_dropdown.value
        self.items_dropdown.options = []
        if tipo == "Entrada":
            items = self.restaurante.menu.entradas
        elif tipo == "Plato Principal":
            items = self.restaurante.menu.platos_principales
        elif tipo == "Postre":
            items = self.restaurante.menu.postres
        elif tipo == "Bebida":
            items = self.restaurante.menu.bebidas
        else:
            items = []

        self.items_dropdown.options = [
            ft.dropdown.Option(item.nombre) for item in items
        ]
        
        if e and e.page:
            e.page.update()


def main(page: ft.Page):
    app = RestauranteGUI()
    app.main(page)


# Inicializar la aplicación Flet
ft.app(target=main)
