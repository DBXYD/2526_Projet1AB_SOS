import tkinter
from tkinter import *
from tkinter import ttk
import pandas as pd
import serial
from serial import Serial


data = pd.ExcelFile("../Excel/2526_Stock_components.xlsx")

df = pd.read_excel("../Excel/2526_Stock_components.xlsx", sheet_name = 'components', header = 0, usecols='Q:U ', skiprows=None, na_values=['NA', '-', 'N/A'])
print(df)

loc = [room,drawer,column,raw]
[df[df['Room']==]]

'''root = Tk()
root.title("Gestion des inventaires")
# creates serial port and opens it
#ser = serial.Serial('/dev/ttyUSB0', 9600) #lirena_values=['NA', '-', 'N/A'])


# reads n bytes sent to port ser via usb
n= 
data= ser.read(n)

# or reads everything after waiting for data to be sent
while not ser.in_waiting:
    time.sleep(0.5)
data = ser.read_all()

loc = decode(data) # [room, furniture, drawer, column, row]

# closing connection
ser.close()




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