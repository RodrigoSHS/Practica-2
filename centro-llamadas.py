import random

class Cliente:
    """
    Un Cliente llega al centro de llamadas.
    """

    def __init__(self, tiempo_llegada, tipo):
        self.tiempo_llegada = tiempo_llegada
        self.tipo = tipo #  Tipo de cliente, puede ser "premier" o "regular"


class CentroLlamadas:
    """
    Simula un centro de llamadas.

    NUM_OPERADORES: El numero de lineas de operadores va cambiando dependiendo de las simulaciones
    """

    NUM_OPERADORES = 0

    def __init__(self):
        """
        Inicializa una nueva instancia de CentroLlamadas.
        """
        self.operadores = [0] * self.NUM_OPERADORES # Nueva lista de lineas de operadores
        self.cola = [] # Cola de Clientes
        self.tiempos_espera = {"premier": [], "regular": []}
        # Inicializa la lista para registrar la longitud de la cola en cada minuto
        self.longitud_de_cola = []

    def simular(self, tiempo_simulacion):
        """
        Ejecuta la simulación del centro de llamadas por un tiempo determinado.
        """
        tiempo_actual = 0 
        tiempo_llegada = 0

        while tiempo_actual < tiempo_simulacion: # Entra a un bucle mientras el tiempo actual sea menor a 24hrs de simulación
            if tiempo_llegada <= tiempo_actual:
                # Determina el tipo de cliente basado en una probabilidad (1/6 para 'premier')
                tipo_cliente = "premier" if random.random() < 1/6 else "regular"
                cliente = Cliente(tiempo_actual, tipo_cliente)
                print(f"Cliente {tipo_cliente} agregado en el minuto {int(tiempo_actual)}")
                
                # Agrega el cliente a la cola segun su tipo
                if cliente.tipo == "premier":
                    # Si es premier tiene prioridad y se agrega al inicio de la cola
                    self.cola.insert(0, cliente)
                else:
                    # sino entonces, simplemente se agrega a la lista
                    self.cola.append(cliente)
                
                # Programa a un proximo cliente entre 1 y 3 minutos
                tiempo_llegada = tiempo_actual + random.uniform(1, 3)

            # Asigna clientes a operadores disponibles
            for i in range(len(self.operadores)):
                if tiempo_actual >= self.operadores[i]:
                    if self.cola:
                        # Extrae el siguiente cliente de la cola
                        cliente = self.cola.pop(0)
                        # Calcula el tiempo de espera del cliente con un valor en el rango de [1,3]
                        tiempo_espera = tiempo_actual - cliente.tiempo_llegada
                        self.tiempos_espera[cliente.tipo].append(tiempo_espera)
                        # Genera una duración aleatoria para la llamada entre 1 y 81 minutos
                        duracion_llamada = random.uniform(1, 81)
                        # Actualiza el tiempo en que el operador estará disponible nuevamente
                        self.operadores[i] = tiempo_actual + duracion_llamada

            # Registra la longitud actual de la cola
            self.longitud_de_cola.append(len(self.cola))

            # Avanza el tiempo de la simulación en 1 minuto
            tiempo_actual += 1

    def resultados(self):
        """
        Muestra los resultados de la simulación, incluyendo tiempos de espera y longitud máxima de la cola.
        """
        for tipo in ["premier", "regular"]:
            tiempos = self.tiempos_espera[tipo]
            max_espera = max(tiempos) if tiempos else 0
            promedio_espera = sum(tiempos) / len(tiempos) if tiempos else 0
            print(
                f"Tiempo maximo de espera para clientes {tipo}: {int(max_espera)} minutos\n"
            )
            print(
                f"Tiempo promedio de espera para clientes {tipo}: {promedio_espera:.2f} minutos\n"
            )
        
        # Logitud maxima que alcanzo la cola durante la simulación
        max_longitud_cola = max(self.longitud_de_cola)if self.longitud_de_cola else 0
        print(f"Longitud maxima de la cola durante la simulación: {max_longitud_cola}")

if __name__ == "__main__":
    """
    Bloque principal que inicia la simulación del centro de llamadas.
    """
    OPERADORES_INICIALES = 0    # Numero inicial de operadores
    OPERADORES_MAXIMOS = 30     # Numero maximo de operadores a probar
    TIEMPO_SIMULACION = 1440    # Duración de la simulación en minutos (24 horas)

    # Itera desde el numero inicial hasta el maximo de operadores
    for operadores in range(OPERADORES_INICIALES, OPERADORES_MAXIMOS):
        CentroLlamadas.NUM_OPERADORES = operadores
        simulacion = CentroLlamadas()
        # Ejecuta la simulación
        simulacion.simular(TIEMPO_SIMULACION)
        cola_final = len(simulacion.cola)
        if cola_final == 0:
            print(
                f"\Minimo de líneas de operadores necesarias: {operadores}\n"
            )
            # Muestra los resultados de la simulación
            simulacion.resultados()
            break
