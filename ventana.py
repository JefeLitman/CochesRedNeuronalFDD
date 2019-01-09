import tkinter as tk
from tkinter import messagebox
from time import sleep
from Gen_Alg import genetica as genes
import numpy as np


class Application(tk.Frame):
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        self.master.title("DROTIUM BRAIN")
        self.master.resizable(0,0)
        self.master.geometry("926x404+50+20")
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        top=self.winfo_toplevel()
        top.rowconfigure(0,weight= 1)
        top.rowconfigure(1, weight = 1)
        top.columnconfigure(0, weight = 3)
        top.columnconfigure(1, weight = 1)

        self.ejecutandose = False
        self.pausado = False
        self.i = 1
        self.logro = False

        self.createWidgets()

        self.map = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          ])

    def createWidgets(self): #Ventana principal
        self.mapa = tk.Canvas(master=self,bg ="#D5E8D4",bd=0,width=800,height=400)
        self.init_mapa()
        self.mapa.grid(row=0,column=0,rowspan=2,sticky=tk.N + tk.S + tk.E + tk.W)

        self.botones_parametros = tk.Frame(master = self)
        self.init_boton_parametros()
        self.botones_parametros.grid(row=0,column=1,sticky=tk.N + tk.S + tk.E + tk.W)

        self.botones_control = tk.Frame(master = self)
        self.init_boton_control()
        self.botones_control.grid(row=1,column=1,sticky=tk.N + tk.S + tk.E + tk.W)

        self.init_poblacion()


    def init_mapa(self):
        """Funcion que va crear la grid de los botones para el mapa
        ya cargado por csv"""
        for i in range(9):
            self.mapa.create_line(0, (i+1)*40, 800, (i+1)*40, fill="#888", state=tk.DISABLED)
        for j in range(19):
            self.mapa.create_line((j+1)*40,0,(j+1)*40,400,fill="#888",state=tk.DISABLED)

        self.set_puntos()

        #D5E8D4 Color verde
        #F8CECC Color Rojo

    def init_boton_parametros(self):
        """Funcion que va crear los botones dentro del frame de botones
        de los parametros de la aplicacion"""
        self.botones_parametros.rowconfigure(0,weight=1)
        self.botones_parametros.rowconfigure(1, weight=1)
        self.botones_parametros.rowconfigure(2, weight=1)
        self.botones_parametros.columnconfigure(0,weight=1)

        cargar_mapa = tk.Button(self.botones_parametros,text="Cargar Mapa",bd=1,bg="#D8B4E7",state = tk.DISABLED,command=None)
        cargar_mapa.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)

        cargar_coche = tk.Button(self.botones_parametros, text="Cargar Mejor Coche",bd=1,bg="#D8B4E7",state = tk.DISABLED, command=None)
        cargar_coche.grid(row=1,column=0,sticky=tk.N+tk.S+tk.E+tk.W)

        guardar_coche = tk.Button(self.botones_parametros, text="Guardar Mejor Coche",bd=1,bg="#D8B4E7",state = tk.DISABLED, command=None)
        guardar_coche.grid(row=2,column=0,sticky=tk.N+tk.S+tk.E+tk.W)
    
    def init_boton_control(self):
        """Funcion que va crear los botones dentro del frame de botones 
        de control de la aplcacion"""
        self.botones_control.rowconfigure(0, weight=1)
        self.botones_control.rowconfigure(1, weight=1)
        self.botones_control.rowconfigure(2, weight=1)
        self.botones_control.rowconfigure(3, weight=1)
        self.botones_control.columnconfigure(0, weight=1)
        self.botones_control.columnconfigure(1, weight=1)

        play = tk.Button(self.botones_control,text="Play",bd=1,bg="#B4E8B0",command=self.init_ejecucion)
        play.grid(row=0,column=0,sticky=tk.N+tk.S+tk.E+tk.W)

        reset = tk.Button(self.botones_control, text="Reset", bd=1, bg="#F8A59F", command=self.reset_ejecucion)
        reset.grid(row=0, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.pause = tk.Button(self.botones_control, text="Pause", bd=1, bg="#FCFFAB",command=self.pausar_ejecucion)
        self.pause.grid(row=1, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        self.iteracion = tk.Label(self.botones_control,text="Iteracion: 0",bd=2,bg="#F7D18F")
        self.iteracion.grid(row=2,column=0, columnspan=2,sticky=tk.N+tk.S+tk.E+tk.W)

        self.generacion = tk.Label(self.botones_control,text="Generacion: 0",bd=2,bg="#F7D18F")
        self.generacion.grid(row=3, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

    def pausar_ejecucion(self):
        self.pausado = True
        if(self.ejecutandose):
            self.ejecutandose = False
            self.pause["text"]="Reanudar"
            self.update()
        else:
            self.pause["text"] = "Pause"
            self.update()
            self.init_ejecucion()

    def set_puntos(self):
        """Funcion que define los PI y PF de forma aleatoria"""
        pi_x = np.random.randint(20)
        pi_y = np.random.randint(10)
        pf_x = np.random.randint(20)
        pf_y = np.random.randint(10)

        while ([pi_x, pi_y] == [pf_x, pf_y]):
            pi_x = np.random.randint(20)
            pi_y = np.random.randint(10)
            pf_x = np.random.randint(20)
            pf_y = np.random.randint(10)

        """pi_x = 10
        pi_y = 4
        pf_x = 0
        pf_y = 9"""

        self.mapa.create_rectangle(pi_x * 40, pi_y * 40, pi_x * 40 + 40, pi_y * 40 + 40, width=0, fill="#C7DCFC",
                                   tags="PI")
        self.mapa.create_rectangle(pf_x * 40, pf_y * 40, pf_x * 40 + 40, pf_y * 40 + 40, width=0, fill="#F7D18F",
                                   tags="PF")

    def reset_ejecucion(self):
        """Esta funcion reiniciara la ejecucion del todos lso coches."""
        self.limpiar_pantalla()

        """Se reiniciaran los parametros"""
        self.ejecutandose = False
        self.pausado = False
        self.i = 1
        self.logro = False
        self.pause["text"]="Pause"
        self.set_puntos()
        self.init_poblacion()

    def limpiar_pantalla(self):
        """Se eliminaran los dibujos de los coches y puntos"""
        self.mapa.delete("PI")
        self.mapa.delete("PF")
        for i in range(10):
            coche = "Coche" + str(i)
            self.mapa.delete(coche)

    def set_posicion_inicial(self):
        """Esta funcion me posiciona y dibuja los coches en la posicion inicial """
        pi = self.mapa.coords('PI')[:2]

        """Si se esta ejecutando posiciono los coches visualmente en el PI, de lo contrario los creo"""
        color = ["#F00","#FF6D05","#FF0","#9807E8","#00F","#07CAE8","#000","#FFF","#0F0","#676A73"]
        for i in range(10):
            coche = "Coche" + str(i)
            if(self.pausado):
                pos = self.mapa.coords(coche)[:2]
                self.mapa.move(coche, pi[0]- pos[0],pi[1]-pos[1])
            else:
                self.mapa.create_oval(pi[0], pi[1], pi[0] + 40, pi[1] + 40, fill=color[i],width=0, tags=coche)
            self.update()

        pi = [int(i / 40) for i in pi][::-1]
        self.genes.set_posicion_inicial(pi)
        self.update()

    def init_poblacion(self):
        """Funcion que creara la poblacion y la dibujara en el canvas"""
        self.genes = genes(10,4,(10,20))

        self.set_posicion_inicial()

    def init_ejecucion(self):
        """Funcion que va iniciar la ejecucion de la poblacion con hasta que alguno llegue al punto
        final e iniciara con nuevos puntos iniciales y finales"""
        self.ejecutandose = True
        self.pause["text"] = "Pause"

        if(self.pausado == False):
            self.i=1
            self.logro = False

        while self.ejecutandose:
            pf = self.mapa.coords('PF')[:2]
            pf = [int(i / 40) for i in pf][::-1]

            """Verifico antes que no exista ningun individuo en el PF"""
            for i,pos in enumerate(self.genes.get_posiciones()):
                if(pos == pf):
                    messagebox.showinfo("Felicidades","El coche "+str(i)+" lo logro")
                    self.logro = True
                    self.limpiar_pantalla()
                    self.set_puntos()
                    self.set_posicion_inicial()

            """En este punto activo los coches y ellos se moveran"""
            self.genes.activar_individuos(punto_final=pf, mapa=self.map)

            """Ahora viene la animacion de movimiento para cada coche"""
            self.animacion_movimiento()

            """Ahora se procede a verificar si la poblacion se puede evolucionar"""
            if (self.genes.evolucionar_poblacion() == False):
                self.pausado = True
                if(np.random.random()<np.random.random() and self.logro == False):
                    self.reset_ejecucion()
                    self.ejecutandose = True
                else:
                    self.set_posicion_inicial()
                    self.genes.revivir_poblacion()
                    self.pausado = False

            self.iteracion["text"]="Iteracion: "+str(self.i)
            self.generacion["text"]="Generacion: "+str(self.genes.iteracion)
            self.i = self.i + 1
            self.update()

    def animacion_movimiento(self):
        posicion =self.genes.get_posiciones()
        for i,pos in enumerate(posicion):
            coche = "Coche" + str(i)
            if(self.genes.get_estados()[i] == True):
                pos_ini = self.mapa.coords(coche)[:2]
                pos_fin = pos[::-1]
                pos_fin = [i*40 for i in pos_fin]
                for t in range(4):
                    self.mapa.move(coche, (pos_fin[0]-pos_ini[0])/4, (pos_fin[1]-pos_ini[1])/4)
                    if(t%2 == 0):
                        if(self.genes.get_estados()[i] == False):
                            self.mapa.itemconfigure(coche,fill="")
                    sleep(0.02)
                    self.update()

app=Application()
app.mainloop()