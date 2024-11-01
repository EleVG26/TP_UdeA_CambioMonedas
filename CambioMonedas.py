#Importar libreria para operaciones estadisticas
import pandas as pd
#Importar libreria para interfaz grafica de usuario
from tkinter import*
from tkinter.ttk import Notebook
from tkinter import messagebox
#importar libreria para manejo de fechas y tiempo
from datetime import *
#importar libreria para crear gráficas
from matplotlib import pyplot as plt
#importar libreria util
import Util


iconos= ["./iconos/grafica.png",
         "./iconos/datos.png"]
textosBotones = ["Gráfica Cambio vs Fecha","Datos Estadísticos"]

df = None

def obtenerMonedas():
    global df
    df = pd.read_csv("Cambios Monedas.csv") #dataframe es una estructura matricial
    monedas = df["Moneda"].tolist()
    #return(dict.fromkeys(monedas)) #creacion de diccionario para obtener valores sin repetirse
    return(list(set(monedas)))

def graficar():
    if cmbMoneda.current() >=0:
        nb.select(0)
        df.sort_values(by="Fecha", ascending=False).head() #ordenar los datos por fechas
        cambios = df[df["Moneda"]==monedas[cmbMoneda.current()]]
        y = cambios["Cambio"]
        
        fechas = cambios["Fecha"]
        x = [datetime.strptime(f, "%d/%m/%Y").date() for f in fechas] #leer a partir de una cadena de texto una fecha
        
        #crear grafica
        plt.clf()
        plt.title("Cambios de la moneda "+ monedas[cmbMoneda.current()] )
        plt.ylabel("Cambios")
        plt.ylabel("Fechas")
        fig = plt.gcf()  # Obtener la figura actual
        fig.set_size_inches(7, 7)  # Ajustar el tamaño de la figura en pulgadas (ancho, alto)
        plt.plot(x,y)
        nombreArchivo = "Grafica Cambios Moneda.png"
        plt.savefig( nombreArchivo)
        
        #mostrar la grafica
        Util.agregarImagen(paneles[0], nombreArchivo, 0, 0 )
    else:
        messagebox.showerror("Error graficando", "No ha seleccionado la moneda")

def estadisticas():
    if cmbMoneda.current() >=0:
        nb.select(1)
        # Limpiar el panel de estadísticas
        for widget in paneles[1].winfo_children():
            widget.destroy()
        # Obtener los datos de la moneda seleccionada   
        cambios = df[df["Moneda"]==monedas[cmbMoneda.current()]]
        
        #Mostrar promedio
        Util.agregarEtiqueta(paneles[1], "Promedio:", 0, 0)
        Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(cambios["Cambio"].mean()), 0, 1)
        
        #mostrar desviación estandar
        Util.agregarEtiqueta(paneles[1], "Desviación:", 1, 0)
        Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(cambios["Cambio"].std()), 1, 1)
        
        #mostrar el máximo
        Util.agregarEtiqueta(paneles[1], "Máximo:", 2, 0)
        Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(cambios["Cambio"].max()), 2, 1)
        
        #mostrar el mínimo
        Util.agregarEtiqueta(paneles[1], "Mínimo:", 3, 0)
        Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(cambios["Cambio"].min()), 3, 1)
        
        #mostrar la moda
        Util.agregarEtiqueta(paneles[1], "Moda:", 4, 0)
        f= 4
        for moda in cambios["Cambio"].mode():
            Util.agregarEtiqueta(paneles[1], "{0:,.2f}".format(moda), f, 1)
            f+=1
        
        
    else:
        messagebox.showerror("Error en estadisticas", "No ha seleccionado la moneda")
        

#crear una vertana
v = Util.crearVentana("CAMBIO DE MONEDAS", "700x800")

#Agregar una barra de herramientas basada en una lista de archivos con imagenes
botones = Util.agregarBarra(v,iconos, textosBotones)
botones[0].configure(command = graficar)
botones[1].configure(command = estadisticas)

#Agregar contenedor para la lista que permite escoger la moneda a procesar
frm = Frame(v)
frm.pack(side=TOP, fill=X)
Util.agregarEtiqueta(frm, "Moneda:",0,0)

monedas = obtenerMonedas()
cmbMoneda = Util.agregarLista(frm, monedas, 0,1)

#Agregar panel de pestañas para mostrar resultados
nb = Notebook(v)
#Rellenar en ambos lados
nb.pack(fill=BOTH, expand=YES)
#Pestañas basadas en frames, vector con encabezados
encabezados = ["Gráfica","Datos"]
paneles = []
for e in encabezados:
    frm = Frame(v) #para cada marco en la ventana
    paneles.append(frm) #agregar paneles a un vector
    nb.add(frm, text=e)

v.mainloop()
