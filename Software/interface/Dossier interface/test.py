'''
import tkinter as tk
from tkinter import ttk
import pandas as pd
import serial
from serial import Serial


liste = pd.ExcelFile("../Excel/2526_Stock_components.xlsx")

df = pd.read_excel("../Excel/2526_Stock_components.xlsx", sheet_name = 'components', header = 0, usecols='A:U ', skiprows=1, na_values=['NA', '-', 'N/A'])
print(df)

room = "D265"
f="Tiro-clas"
drawer = 2
column = 9
raw=1
loc = [room,f,drawer,column,raw]
print(loc)

condition = (df['Room']==loc[0])&(df['Furniture']==loc[1])&(df['Drawer']==loc[2])&(df['Column']==loc[3])&(df['Raw']==loc[4])
print(df[condition])



# creates serial port and opens it
#ser = serial.Serial('/dev/ttyUSB0', 9600) #lirena_values=['NA', '-', 'N/A'])


# reads n bytes sent to port ser via usb

data= ser.read(n)

# or reads everything after waiting for data to be sent
while not ser.in_waiting:
    time.sleep(0.5)
data = ser.read_all()

loc = decode(data) # [room, furniture, drawer, column, row]

# closing connection
ser.close()



root = tk.Tk()
root.title("Gestion des inventaires")
mainframe = tk.ttk.Frame(root, padding=(3, 3, 100, 100))

ttk.Label(mainframe, text="Emplacement :" ).grid(column=2, row=2)

ttk.Label(mainframe, text="MPN", ).grid(column=1, row=2)
ttk.Label(mainframe, text="SKU").grid(column=3, row=2)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)




root.mainloop()

'''

import tkinter as tk
from tkinter import ttk
import pandas as pd
import serial
from serial import Serial
import time


def test(room, f, drawer,column, raw):
    return [room,f,drawer,column,raw]

def decode(data):
    # supp 1B salle et meuble; 1B tiroir; 1B col et ligne
    # returns array
    list_room= ["NaN","Patricia", "D265"] 
    list_f= ["NaN", "tiro-class"]
    loc= [0]*5
    loc[0]= list_room[int(data[:2], 16)]
    loc[1]= list_f[int(data[2:4], 16)]
    loc[2]= int(data[4:8], 16)
    loc[3]= int(data[8:10], 16)
    loc[4]= int(data[10:12], 16)
    return loc 

def search_info(loc):
    df = pd.read_excel("../Excel/2526_Stock_components.xlsx", sheet_name = 'components', header = 0, usecols='E:U ', skiprows=1 ,na_values=['NA', '-', 'N/A'])
    condition = (df['Room']==loc[0])&(df['Furniture']==loc[1])&(df['Drawer']==loc[2])&(df['Column']==loc[3])&(df['Raw']==loc[4])
    resultat = df[condition]
    MPN=(resultat['MPN'].values[0])
    SKU=(resultat['Supplier Ref'].values[0])    
    return MPN, SKU
    






def display_info(MPN, SKU,loc): 
    texte_mpn = tk.StringVar(value="MPN ")
    texte_loc = tk.StringVar(value="Emplacement ")
    texte_sku = tk.StringVar(value="SKU")
    texte_loc.set(f"Emplacement : Salle {loc[0]} {loc[1]} Tiroir {loc[2]} Colonne {loc[3]} Ligne {loc[4]}")
    texte_mpn.set(f"MPN : {MPN}")
    texte_sku.set(f"SKU : {SKU}")
        
#texte_loc.set(f"Emplacement : Salle {nonassigne('Room',0)} {nonassigne('Furniture',0)} Tiroir {nonassigne('Drawer',2)} Colonne {nonassigne('Column',3)} Ligne {nonassigne('Raw',4)}")

def display_base():
    root = tk.Tk()
    root.title("Gestion des inventaires")
    root.state('zoomed')
    mainframe = tk.ttk.Frame(root, padding=(3, 3, 100, 100))
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    
    texte_mpn = tk.StringVar(value="MPN ")
    texte_loc = tk.StringVar(value="Emplacement ")
    texte_sku = tk.StringVar(value="SKU")
    
    label_mpn = ttk.Label(mainframe, textvariable=texte_mpn)
    label_mpn.grid(column=1, row=2)
    
    label_loc = ttk.Label(mainframe, textvariable=texte_loc)
    label_loc.grid(column=2, row=2)
    
    label_sku = ttk.Label(mainframe, textvariable=texte_sku)
    label_sku.grid(column=3, row=2)
    
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    mainframe.columnconfigure(2, weight=1)
    # location = decode(data)
    location = test("D265","Tiro-clas",2,9,1)
    mpn, sku = search_info(location)    
    display_info(mpn,sku,location)

    root.mainloop()
    
def main ():
    
    display_base()

