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

        self.costo = lambda Xf,Yf,Xi,Yi,Der,Izq,Arr,Aba: np.sqrt( (Xi+Der-Izq-Xf)**2 + (Yi+Arr-Aba-Yf)**2 )
        self.der_coste_der = lambda Xf,Yf,Xi,Yi,Der,Izq,Arr,Aba: (Xi+Der-Izq-Xf)/np.sqrt( (Xi+Der-Izq-Xf)**2 + (Yi+Arr-Aba-Yf)**2 )
        self.der_coste_izq = lambda Xf,Yf,Xi,Yi,Der,Izq,Arr,Aba: (-Xi-Der+Izq+Xf)/np.sqrt( (Xi+Der-Izq-Xf)**2 + (Yi+Arr-Aba-Yf)**2 )
        self.der_coste_arr = lambda Xf,Yf,Xi,Yi,Der,Izq,Arr,Aba: (Yi+Arr-Aba-Yf)/np.sqrt( (Xi+Der-Izq-Xf)**2 + (Yi+Arr-Aba-Yf)**2 )
        self.der_coste_aba = lambda Xf,Yf,Xi,Yi,Der,Izq,Arr,Aba: (-Yi-Arr+Aba+Yf)/np.sqrt( (Xi+Der-Izq-Xf)**2 + (Yi+Arr-Aba-Yf)**2 )

        topologia = [4,10,10,10,4]

        sigmoide = lambda x: 1 / (1 + np.e ** (-x))
        relu = lambda x: np.maximum(0,x)
        dsigmoide= lambda x: x * (1 - x)
        drelu = lambda x: 1*(x>0)

        self.cerebro = NN(topologia,relu,drelu)

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
        if(resultado[0,0]>=0.5): #Condicional para la salida de la Der
            self.posicion[1] = self.posicion[1] + 1  # Derecha
        if(resultado[0,1]>=0.5): #Condicional para la salida de la izq
            self.posicion[1] = self.posicion[1] - 1  # Izquierda
        if(resultado[0,2]>=0.5): #Condicional para la salida de arriba
            self.posicion[0] = self.posicion[0] + 1  # Arriba
        if(resultado[0,3]>=0.5): #Condicional para la salida de abajo
            self.posicion[0] = self.posicion[0] - 1  # Abajo

    def obtener_salidas_procesadas(self,resultado):
        """Resultado es la salida de transmitir las entradas en el cerebro
        Esta funcion toma la salida final y se encarga de devolver el valor
        correspondiente a Der, Izq, Arr, Aba  en un vector con el orden
        correspondiente dado anteriormente"""
        salidas_procesadas = []
        if(resultado[0,0]>=0.5): #Condicional para la salida de la Der
            salidas_procesadas.append(1)
        else:
            salidas_procesadas.append(0)
        if(resultado[0,1]>=0.5): #Condicional para la salida de la izq
            salidas_procesadas.append(1)
        else:
            salidas_procesadas.append(0)
        if(resultado[0,2]>=0.5): #Condicional para la salida de arriba
            salidas_procesadas.append(1)
        else:
            salidas_procesadas.append(0)
        if(resultado[0,3]>=0.5): #Condicional para la salida de abajo
            salidas_procesadas.append(1)
        else:
            salidas_procesadas.append(0)
        return salidas_procesadas

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

    def calcular_der_costo(self,destino,valores_neuronas):
        """Destino debe estar en forma de lista con los valores naturales de la coordenada"""
        if(((self.posicion[0]+valores_neuronas[0]-valores_neuronas[1]-destino[0])**2 + (self.posicion[1]+valores_neuronas[2]-valores_neuronas[3]-destino[1])**2 )==0):
            dder=0
            dizq=0
            darr=0
            daba=0
        else:
            dder = self.der_coste_der(destino[0],destino[1],self.posicion[0],self.posicion[1],valores_neuronas[0],valores_neuronas[1],valores_neuronas[2],valores_neuronas[3])
            dizq = self.der_coste_izq(destino[0], destino[1], self.posicion[0], self.posicion[1],valores_neuronas[0],valores_neuronas[1],valores_neuronas[2],valores_neuronas[3])
            darr = self.der_coste_arr(destino[0], destino[1], self.posicion[0], self.posicion[1],valores_neuronas[0],valores_neuronas[1],valores_neuronas[2],valores_neuronas[3])
            daba = self.der_coste_aba(destino[0], destino[1], self.posicion[0], self.posicion[1],valores_neuronas[0],valores_neuronas[1],valores_neuronas[2],valores_neuronas[3])
        return np.r_[[[dder,dizq,darr,daba]]]

    def calcular_puntuacion(self,destino,parametros):
        if(self.posicion == destino):
            self.puntuacion = 0
        else:
            self.puntuacion = self.costo(destino[0],destino[1],self.posicion[0],self.posicion[1],parametros[0],parametros[1],parametros[2],parametros[3])

    def mover(self,destino):
        """Destino debe ser una lista de la coordenada final ([Xf,Yf])"""
        entrada = np.append(self.get_coor_normal(self.posicion),self.get_coor_normal(destino),axis=1)
        #objetivo = self.get_coor_normal(destino)

        salida = self.cerebro.transmitir_entradas(entrada)
        salida_procesada = self.obtener_salidas_procesadas(salida[-1][1])

        valor_der_coste = self.calcular_der_costo(destino,salida_procesada)
        tasa =0.1

        deltas = self.cerebro.retropropagacion(salida,valor_der_coste)
        self.cerebro.descenso_gradiente(salida,deltas,tasa)

        salida = salida[-1][1]

        self.posicionar(salida)

        self.calcular_puntuacion(destino,salida_procesada)

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