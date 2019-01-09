import numpy as np

class capa_neuronal():
    def __init__(self, n_conexiones, n_neuronas):
        self.b = np.random.random((1, n_neuronas))
        self.W = np.random.random((n_conexiones, n_neuronas))

class red_neuronal():

    def __init__(self,topologia,fun_act,der_fun_act):
        self.red_neuronal = self.crear_red(topologia)
        self.fun_act = fun_act #Funcion de Activacion
        self.dfun_act = der_fun_act #Derivada de la funcion de activacion

    def crear_red(self,topologia):
        red = []
        for capa in range(len(topologia[:-1])):
            red.append(capa_neuronal(topologia[capa],topologia[capa+1]))
        return red
            
    def transmitir_entradas(self,entradas):
        #Entradas debe ser una matrix
        salida = [(None,entradas)]

        for capa in range(len(self.red_neuronal)):
            z = salida[-1][1] @ self.red_neuronal[capa].W + self.red_neuronal[capa].b
            a = self.fun_act(z)
            salida.append((z,a))
        
        return salida

    def retropropagacion(self,salida,der_coste):

        deltas = []

        for capa in reversed(range(len(self.red_neuronal))):
            a = salida[capa + 1][1] #El uno es porque es donde esta el a de la capa siguiente
            
            if (capa == len(self.red_neuronal) - 1):
                deltas.insert(0, der_coste * self.dfun_act(a))
            else:
                deltas.insert(0, deltas[0] @ self.red_neuronal[capa+1].W.T * self.dfun_act(a))

        return deltas

    def descenso_gradiente(self,salida,deltas,tasa_aprendizaje=0.5):
        
        for capa in range(len(self.red_neuronal)):
            self.red_neuronal[capa].b = self.red_neuronal[capa].b - deltas[capa] * tasa_aprendizaje
            self.red_neuronal[capa].W = self.red_neuronal[capa].W - salida[capa][1].T @ deltas[capa] * tasa_aprendizaje

    def activar(self,entradas,objetivo,valor_dfun_coste,tasa_aprendizaje=0.5):
        """El valor_dfun_coste debe ser un valor o una lista dependiendo de la
        cantidad de salidas (Lista con derivadas parciales con el mismo indice y
        orden que las variables de entrada)
        La entradas y objetivo ya deben estar normalizadas y ser del mismo tamaño 
        y tipo
        """
        if (np.array_equal(entradas,objetivo)):
            return entradas
        else:
            salidas = self.transmitir_entradas(entradas)
            deltas = self.retropropagacion(salidas,valor_dfun_coste)
            self.descenso_gradiente(salidas,deltas,tasa_aprendizaje)
            return salidas[-1][1]