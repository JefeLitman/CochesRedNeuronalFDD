from Red_Neuronal import red_neuronal as NN
import numpy as np

class coche():
    def __init__(self,indice):

        self.indice = indice
        self.vivo = True #Estado en True para conocer si esta vivo o muerto
        self.puntuacion = 999 #Este es el valor de la funcion de coste

        self.posicion = [] #Lista que guarda las coordenadas naturales del coche

        self.max_x = 0
        self.max_y = 0

        self.costo = lambda Xf,Yf,Xi,Yi: np.sqrt( (Xi-Xf)**2 + (Yi-Yf)**2 )
        self.der_coste_x = lambda Xf, Yf, Xi, Yi: (Xi - Xf) / np.sqrt((Xi - Xf) ** 2 + (Yi - Yf) ** 2)
        self.der_coste_y = lambda Xf, Yf, Xi, Yi: (Yi - Yf) / np.sqrt((Xi - Xf) ** 2 + (Yi - Yf) ** 2)

        topologia = [4,6,6,2]

        sigmoide = lambda x: 1 / (1 + np.e ** (-x))
        dsigmoide= lambda x: x * (1 - x)

        self.cerebro = NN(topologia,sigmoide,dsigmoide)

    def normalizar(self,x,x_max):
        if (x < -x_max):
            x = -x_max
        elif (x > x_max):
            x = x_max
        return x / x_max

    def posicionar(self,resultado):
        """Resultado es la salida de la activacion del cerebro
        Esta funcion toma la salida de la activacion y re ubica
        el coche segun los resultados"""
        if (resultado[0, 0] > 0.6):
            self.posicion[0] = self.posicion[0] - 1  # Abajo
        elif (resultado[0, 0] <= 0.4):
            self.posicion[0] = self.posicion[0] + 1  # Arriba
        if (resultado[0, 1] > 0.6):
            self.posicion[1] = self.posicion[1] + 1  # Derecha
        elif (resultado[0, 1] <= 0.4):
            self.posicion[1] = self.posicion[1] - 1  # Izquierda

    def definir_limites(self,maximo_x,maximo_y):
        """Aqui se establece el tamaño del mapa en numeros normales (10x20)"""
        self.max_x = maximo_x - 1
        self.max_y = maximo_y - 1

    def get_limites(self):
        return [ self.max_x+1 , self.max_y+1 ]

    def get_indice(self):
        return self.indice

    def matar(self):
        self.vivo = False

    def get_coor_normal(self,coordenada):
        """Cordenada debe entegarse en forma de lista y esta funcion
        la retorna en forma de matrix lista para procesar"""
        x=coordenada[0]
        y=coordenada[1]
        x_normal = self.normalizar(x, self.max_x)
        y_normal = self.normalizar(y, self.max_y)
        return np.r_[[[x_normal, y_normal]]]

    def calcular_der_costo(self,destino):
        """Destino debe estar en forma de lista con los valores naturales de la coordenada"""
        dx = self.der_coste_x(destino[0],destino[1],self.posicion[0],self.posicion[1])
        dy = self.der_coste_y(destino[0], destino[1], self.posicion[0], self.posicion[1])

        return np.r_[[[dx,dy]]]

    def calcular_puntuacion(self,destino):
        if(self.posicion == destino):
            self.puntuacion = 0
        else:
            self.puntuacion = self.costo(destino[0],destino[1],self.posicion[0],self.posicion[1])

    def mover(self,destino):
        """Destino debe ser una lista de la coordenada final ([Xf,Yf])"""
        entrada = np.append(self.get_coor_normal(self.posicion),self.get_coor_normal(destino),axis=1)
        objetivo = self.get_coor_normal(destino)

        valor_der_coste = self.calcular_der_costo(destino)
        tasa = 0.5

        salida = self.cerebro.activar(entrada,objetivo,valor_der_coste,tasa)

        self.posicionar(salida)

        self.calcular_puntuacion(destino)

    def lugar_valido(self,mapa):
        """Mapa es una matrix de 0 y 1 donde 0 es una lugar invalido y 1 lo contrario
        Mapa es de tipo array"""
        if(self.posicion[0]<0 or self.posicion[0]>self.max_x):
            return False
        elif(self.posicion[1]<0 or self.posicion[1]>self.max_y):
            return False
        elif(mapa[self.posicion[0],self.posicion[1]] == 0):
            return False
        else:
            return True