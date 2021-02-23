import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import os

import numpy as np
from sys import exit
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

color_boton=("navajo white")
color_etiqueta=("black")
color_ventana=("Darkgoldenrod1")

ventana=Tk()
ventana.title("Las 5 vocales")
ventana.resizable(0,0)
#ventana.iconbitmap("Fourier.ico");
ventana.geometry("670x300")
ventana.configure(background=color_ventana)

fm = 16384
d = 2
#sd.default.device=2,4

def FFT(señal):
    N = len(señal)
    if (N==2):
        return np.append([señal[0]+señal[1]],[señal[0]-señal[1]])
    else:
        FFT_pares = FFT(señal[::2])
        FFT_impares = FFT(señal[1::2])
        k=np.arange(int(N/2))
        W_N_k = np.exp(-2j*np.pi*k/N)
        t1=FFT_pares+W_N_k*FFT_impares
        t2=FFT_pares-W_N_k*FFT_impares
        return np.append(t1,t2)

def eMag(afft):
	global fm
	res = np.array([])
	for i in range(fm):
		res = np.append(res,abs(complex(afft[i])))
	return res



#########################################################################################################################################
opcion = 0
def callbackFunc(event):
    global opcion
    opcion=combo.current()+1

def clear():
    print("funcion clear")
    global ffEntry
    global ltrEntry
    opcion=1
    combo.current(0)
    ffEntry.set("")
    ltrEntry.set("")

def salir():
    exit()

def escucha():
    rec = sd.rec(int(d*fm), fm, 1)
    sd.wait()
    global ffEntry
    global ltrEntry

    trans = FFT(rec)            #Aplica la transformada de fourier al arreglo de la muestra
    magns = eMag(trans)         #Obtiene el espectro de magnitud a la resultante de la FFT

    plt.plot(magns);plt.title('Espectro de magnitud')

    print("Fundamental")
    fund=np.argmax(magns)
    print(fund)

    ffEntry.set(str(fund))
    opcion=combo.current()+1
    

    letra = ''


    if opcion == 1:
        if np.amax(magns[600:800])<25:
            if np.amax(magns[400:600])<75:
                letra = 'a'
                ltrEntry.set("A")
            else:
                letra = 'e'
                ltrEntry.set("E")
        elif np.amax(magns[600:800])<50:
            if np.amax(magns[400:600])>105:
                letra = 'i'
                ltrEntry.set("I")
            else:
                letra = 'e'
                ltrEntry.set("E")
        else:
            if np.amax(magns[400:600])>205:
                letra = 'u'
                ltrEntry.set("U")
            else:
                if np.amax(magns[600:800])<75:
                    letra = 'e'
                    ltrEntry.set("E")
                else:
                    letra = 'o'
                    ltrEntry.set("O")        

    if opcion == 2:
        if np.amax(magns[600:800])<40:
            if np.amax(magns[400:600])<100:
                letra = 'a'
                ltrEntry.set("A")
            else:
                letra = 'e'
                ltrEntry.set("E")
        elif np.amax(magns[600:800])<70:
            letra = 'i'
            ltrEntry.set("I")
        else:
            if np.amax(magns[400:600])>190:
                letra = 'u'
                ltrEntry.set("U")
            else:
                letra = 'o'
                ltrEntry.set("O")        

    

    print('letra:' + letra)
    print(np.amax(magns[600:800]))
    print(np.amax(magns[400:600]))


def espectro():
    print("Espectro")
    plt.show()

#########################################################################################################################################

ancho_botonE=9
alto_botonE=1

ancho_boton=9
alto_boton=1

ffEntry=StringVar()
ltrEntry=StringVar()

lblTitulo=Label(ventana,text="Proyecto Final",bg=color_ventana)
lblTitulo.place(x=230,y=5)
lblTitulo.config(fg=color_etiqueta, bg=color_ventana,font=("Times",20,"italic", "bold"),height=1) 


combo=ttk.Combobox(ventana,values=["Soy un hombre","Soy una mujer"],state="readonly")
combo.place(x=10,y=80)
combo.config(font=("Times",15))
combo.current(0)
combo.bind("<<ComboboxSelected>>", callbackFunc)

clear()

Button(ventana,text="Escuchar",bg=color_boton,fg=color_etiqueta,width=ancho_botonE,height=alto_botonE,command=escucha,font=("Times",20)).place(x=55,y=140)
Button(ventana,text="Espectro de magnitud",bg=color_boton,width=18,fg=color_etiqueta,height=alto_boton,command=espectro,font=("Times",11)).place(x=480,y=210)
Button(ventana,text="Limpiar",bg=color_boton,width=ancho_boton,fg=color_etiqueta,height=alto_boton,command=clear,font=("Times",10)).place(x=440,y=260)
Button(ventana,text="Salir",bg=color_boton,width=ancho_boton,fg=color_etiqueta,height=alto_boton,command=salir,font=("Times",10)).place(x=550,y=260)

lblFrec=Label(ventana,text="Fundamental:",bg=color_ventana,justify="left", fg=color_etiqueta, font=("Times",15),height=1, width=11)
lblFrec.place(x=295,y=160)
txtfrecF=Entry(ventana,font=('Times',15),width=10,bg=color_boton,fg=color_etiqueta,textvariable=ffEntry,justify="center").place(x=412,y=160)
lblFrec=Label(ventana,text="Hz",bg=color_ventana,justify="left", fg=color_etiqueta, font=("Times",15),height=1, width=2)
lblFrec.place(x=500,y=160)

lblFrec=Label(ventana,text="Letra:",bg=color_ventana,justify="left", fg=color_etiqueta, font=("Times",15),height=1, width=6)
lblFrec.place(x=350,y=210)
txtLetra=Entry(ventana,font=('Times',15),width=5,bg=color_boton,fg=color_etiqueta,textvariable=ltrEntry,justify="center",).place(x=412,y=210)


lblInstr=Label(ventana,text="- Presione el botón escuchar.\n- La letra identificada se muestra en area de texto correspondiente. \n- Presione el botón espectro de magnitud para  desplegar la gráfica.",bg=color_ventana,justify="left")
lblInstr.place(x=250,y=50)
lblInstr.config(fg=color_etiqueta, bg=color_ventana,font=("Times",12),height=5)

lblInstr2=Label(ventana,text="- Hable mientras el botón \" Escuchar  \" \n  se encuentre en resaltado en blanco. ",bg=color_ventana,justify="left")
lblInstr2.place(x=10,y=210)
lblInstr2.config(fg=color_etiqueta, bg=color_ventana,font=("Times",12),height=2)  


ventana.mainloop()

