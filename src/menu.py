
class ItemMenu:
    def __init__(self, nombre, precio, cantidad=1):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

    def calcular_subtotal(self):
        return self.precio * self.cantidad


class Entrada(ItemMenu):
    def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = "Entrada"


class PlatoPrincipal(ItemMenu):
    def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = "Plato Principal"


class Postre(ItemMenu):
    def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = "Postre"


class Bebida(ItemMenu):
    def __init__(self, nombre, precio, cantidad=1):
        super().__init__(nombre, precio, cantidad)
        self.tipo = "Bebida"


class Menu:
    def __init__(self):
        self.entradas = []
        self.platos_principales = []
        self.postres = []
        self.bebidas = []
    # metodos

    def agregar_entrada(self, nombre, precio, cantidad):
        entrada = Entrada(nombre, precio, cantidad)
        self.entradas.apprend(entrada)
        return entrada

    def agregar_platos_principales(self, nombre, precio, cantidad):
        plato_principal = PlatoPrincipal(nombre, precio, cantidad)
        self.platos_principales.append(plato_principal)
        return plato_principal

    def agregar_postres(self, nombre, precio, cantidad):
        postre = Postre(nombre, precio, cantidad)
        self.postres.append(postre)
        return postre

    def agregar_bebidas(self, nombre, precio, cantidad):
        bebida = Bebida(nombre, precio, cantidad)
        self.bebidas.append(bebida)
        return bebida

    def eliminar_item(self, tipo, nombre):
        if tipo == "Entrada":
            items = self.entradas
        elif tipo == "Plato Principal":
            items = self.platos_principales
        elif tipo == "Postre":
            items = self.postres
        elif tipo == "Bebida":
            items = self.bebidas
        else:
            return False

        for item in items[:]:
            if item.nombre == nombre:
                items.remove(item)
                return True
        return False

    def eliminar_entrada(self, nombre):
        return self.eliminar_item(tipo="Entrada", nombre=nombre)

    def eliminar_plato_principal(self, nombre):
        return self.eliminar_item(tipo="Plato Principal", nombre=nombre)

    def eliminar_postre(self, nombre):
        return self.eliminar_item(tipo="Postre", nombre=nombre)

    def eliminar_bebida(self, nombre):
        return self.eliminar_item(tipo="Bebida", nombre=nombre)

    def obtener_item(self, tipo, nombre):
        if tipo == "Entrada":
            items = self.entradas
        elif tipo == "Plato Principal":
            items = self.platos_principales
        elif tipo == "Postre":
            items = self.postres
        elif tipo == "Bebida":
            items = self.bebidas
        else:
            return False

        for item in items[:]:
            if item.nombre == nombre:
                return item
        return False
