class Cliente:
    # variable de clase, mantiene el siguiente id, consecutivo
    _next_id = 1

    def __init__(self, tamaño_grupo):
        # el formato va  a estar C001, C002, etc.
        self.id = f"C{Cliente._next_id:03d}"
        Cliente._next_id += 1
        self.tamaño_grupo = tamaño_grupo
        self.pedido_actual = None

    def asignar_pedido(self, pedido):
        self.pedido_actual = pedido

    def obtener_total_actual(self):
        return self.pedido_actual_calcular_total() if self.pedido_actual else 0

    def limpiar_pedido(self):
        self.pedido_actual = None

    @classmethod  # modifica las variables de clases
    def reinicial_contador(cls):  # reinicia los clientes
        cls._next_id = 1
