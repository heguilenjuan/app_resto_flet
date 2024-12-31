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
        text = ft.Text("Sistema de restaurante iniciado", size=20, color="blue")
        
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
                    content=ft.Text("Contenido para Cocina")
                ),
                ft.Tab(
                    text="Caja",
                    icon=ft.icons.POINT_OF_SALE,
                    content=ft.Text("Contenido para Caja")
                ),
                ft.Tab(
                    text="Administración",
                    icon=ft.icons.ADMIN_PANEL_SETTINGS,
                    content=ft.Text("Contenido para Administración")
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
        return ft.Container(
            content=ft.Column([
                ft.Text(value="Mesas del restaurante", size=20, weight=ft.FontWeight.BOLD),
                self.grid_container
            ])
        )

    # Métodos internos de vistas
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
                                    ft.Icon(ft.icons.TABLE_RESTAURANT, color=color),
                                    ft.Text(value=f"Mesa {mesa.numero}", size=16, weight=ft.FontWeight.BOLD),
                                ]
                            ),
                            ft.Text(value=f"Capacidad: {mesa.tamaño} personas", size=14),
                            ft.Text(value=f"Estado: {estado}", size=14, color=color),
                        ]
                    ),
                )
            )
        return grid


def main(page: ft.Page):
    app = RestauranteGUI()
    app.main(page)


# Inicializar la aplicación Flet
ft.app(target=main)
