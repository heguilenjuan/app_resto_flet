from menu import Menu


class Restaurante:
    def __init__(self):
        self.mesas=[]
        self.cliente = []
        self.pedidos_activos=  []
        self.menu = Menu()
        self._inicializar_menu()
    
    #agregar datos manualmente    
    def _inicializar_menu(self):
        self.menu.agregar_entrada(nombre="Papas fritas", precio=5000)
        self.menu.agregar_entrada(nombre="Nachos",precio=4500)
        
        self.menu.agregar_platos_principales(nombre="Tortilla de papa", precio=10000)
        self.menu.agregar_platos_principales(nombre="Pollo a la criolla", precio=12000)
        
        self.menu.agregar_postres(nombre="Tiramisu", precio=5000)
        self.menu.agregar_postres(nombre="CheeseCake", precio=7500)
        
        self.menu.agregar_bebidas(nombre="CocaCola", precio=2500)
        self.menu.agregar_bebidas(nombre="CocaCola Zero", precio=2500)
        
    def agregar_mesa(self, mesa):
        self.mesas.append(mesa)
        return f"Mesa {mesa.numero} (capacidad: {mesa.tamaño}) agregada exitosamente"
    
    def asignar_cliente_a_mesa(self, cliente, numero_mesa):
        mesa = self.buscar_mesa(numero_mesa)
        if not mesa:
            return "Mesa no encontrada"
        if mesa.ocupada:
            return "Mesa no disponible"
        if cliente.tamaño_grupo > mesa.tamaño:
            return f"Grupo demasiado grande para la mesa (capacidad maxima:{mesa.tamaño})"
        if mesa.asignar_cliente(cliente):
            self.clientes.append(cliente)
            return f"Cliente {cliente.id} asignado a maesa  {numero_mesa}"
        return "No se pudo asignar el cliente a la mesa"
    
    def buscar_mesa(self, numero_mesa):
        for mesa in self.mesas:
            if mesa.numero == numero_mesa:
                return mesa
            return None
    
    def crear_pedido(self, numero_mesa):
        mesa = self.buscar_mesa(numero_mesa)
        if mesa and mesa.ocupada:
            pedido = Pedido(mesa)
            self.pedidos_activos.append(pedido)
            mesa.pedido_actual = pedido
            mesa.cliente.asignar_pedido(pedido)
            return pedido
        return None
    