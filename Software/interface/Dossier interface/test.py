import tkinter
from tkinter import *
from tkinter import ttk
import pandas as pd
import xlrd
import serial
from serial import Serial


data = pd.ExcelFile("../Excel/2526_Stock_components.xlsx")

df = pd.read_excel('2526_Stock_components.xlsx', sheet_name = 'components', header = 0, usecols='Q:U ', skiprows=None, na_values=['NA', '-', 'N/A'])


'''root = Tk()
root.title("Gestion des inventaires")
#ser = serial.Serial('/dev/ttyUSB0', 9600) #lirena_values=['NA', '-', 'N/A'])

#emplacement = ser.decode()



mainframe = ttk.Frame(root, padding=(3, 3, 100, 100))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))


ttk.Label(mainframe, text="Emplacement :" ).grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, text="MPN").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="SKU").grid(column=3, row=2, sticky=W)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)




root.mainloop()'''