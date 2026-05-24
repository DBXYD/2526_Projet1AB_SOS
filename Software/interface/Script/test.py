import tkinter as tk
from tkinter import ttk
import pandas as pd
import serial
import time



def scan():
    try :    
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        label_warning = ttk.Label(mainframe, text="¨Port USB connected",font=("Helvetica", 5))
        label_warning.grid(column=2, row=30)
        # attend que toutes les informations soient lues pour les envoyées
        while not ser.in_waiting:
            time.sleep(0.5)
        data = ser.read_all()
        # ferme la connexion 
        ser.close()
        return data
    except serial.serialutil.SerialException:
        label_warning = ttk.Label(mainframe, text="Warning : Port USB not connected",font=("Helvetica", 15))
        label_warning.grid(column=2, row=30)

        
def simu_scan(room, f, drawer,column, raw):
    # Fonction pourr tester le code sans connexion USB  
    return bytes([room,f,drawer,column,raw])

tableau_equiv= [["NaN","Patricia", "D265"] , ["NaN", "Tiro-clas"]]

def decode(data):
    # entree: bytes
    # supp 1B salle et meuble; 1B tiroir; 1B col et ligne
    # returns list
    data_hex= data.hex()
    loc= [0]*5
    loc[0]= tableau_equiv[0][ int( data_hex[:2], 16) ]
    loc[1]= tableau_equiv[1][ int( data_hex[2:4], 16) ]
    loc[2]= float(int( data_hex[4:6], 16))
    loc[3]= int( data_hex[6:8], 16)
    loc[4]= int( data_hex[8:10], 16)
    print(loc)
    return loc


def search_info(loc):
    df = pd.read_excel("../Source/2526_Stock_components.xlsx", header=0, skiprows=1, sheet_name='components', usecols="E:U")
    print(df)
    condition = (df['Room'] == loc[0]) & (df['Furniture'] == loc[1]) & (df['Drawer'] == loc[2]) & (
                df['Column'] == loc[3]) & (df['Raw'] == loc[4])
    resultat = df[condition]
    print("Resu:",resultat)
    mpn = (resultat['MPN'].values[0])
    sku = (resultat['Supplier Ref'].values[0])
    return mpn, sku


def display_info(mpn, sku, loc):

    texte_loc.set(f"Emplacement : Room {loc[0]} Furniture {loc[1]} Drawer {loc[2]} Column {loc[3]} Row {loc[4]}")
    texte_mpn.set(f"MPN : {mpn}")
    texte_sku.set(f"SKU : {sku}")


    
    

'''
def loc_a_ecrire():
    # demande quelle loc ecrire ds tag et la renvoie en bytes
    my_label= tk.Label(root, text="Enter Location in order room furniture drawer, column, row with spaces", font=("Helvetica", 15))
    my_label.grid(column=1, row=10)
    error_label = tk.Label(root, text="", font=("Helvetica", 20))
    error_label.grid(column=1, row=90)

    my_entry= tk.Entry(root, width=20, font=("Helvetica", 18))
    my_entry.grid(column=1, row=25)
    ok= 0
    loc_list= []

    while ok == 0:
        if my_entry.get():
            loc= my_entry.get()
            my_entry.delete(0, tk.END)
            loc_list= loc.rsplit(" ")
        if len(loc_list) != 5:
            error_label.config(text="Invalid Location")
            ok= 0
        else:
            ok= 1

    for i in range(2):
        loc_list[i]= tableau_equiv[i].index(loc[i])
    for i in range(2,5):
        loc_list[i]= int(loc_list[i])
    global loc_bytes
    loc_bytes= bytes(loc_list)
'''

def assign_tag(loc_bytes):
    # change ID tag pour loc en parametres
    # type bytes
    # attention timeout port
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600)
        ser.close()
        verif_label = tk.Label(root, text="Location sent" , font=("Helvetica", 15))
        verif_label.grid(column=1, row=35)
    except serial.serialutil.SerialException:
        label_warning = ttk.Label(mainframe, text="Warning : Port USB not connected",font=("Helvetica", 15))
        label_warning.grid(column=2, row=30)
        
    
    

root = tk.Tk()
    
root.title("Gestion des inventaires")

root.state(newstate='icon')
mainframe = ttk.Frame(root, padding=(3, 3, 100, 100))
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))

texte_mpn = tk.StringVar(value="MPN ")
texte_loc = tk.StringVar(value="Emplacement ")
texte_sku = tk.StringVar(value="SKU")


label_mpn = ttk.Label(mainframe, textvariable=texte_mpn)
label_mpn.grid(column=1, row=10)
    
label_loc = tk.ttk.Label(mainframe, textvariable=texte_loc)
label_loc.grid(column=2, row=10)
    
label_sku = ttk.Label(mainframe, textvariable=texte_sku)
label_sku.grid(column=3, row=10)

print("Step1")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)



print("begin")

    
def read_data():
    #data = scan()
    data= simu_scan(2,1,2,9,1) #exemple de localisation test
    loc_str= decode(data)
    mpn, sku= search_info(loc_str)
    display_info(mpn, sku, loc_str)
    root.update()
    

def write_loc():
    global loc_bytes
    def display_value():
        loc = my_entry.get()
        loc_list = loc.rsplit(" ")
            
        if len(loc_list) != 5:
            error_label= tk.Label(root, text="Invalid Location", font=("Helvetica", 18))
            error_label.grid(column=1, row=70)
        try :
            
            loc_list[0] = tableau_equiv[0].index(loc_list[0])
            loc_list[1] = tableau_equiv[1].index(loc_list[1])
            for i in range(2, 5):
                loc_list[i] = int(loc_list[i])
            loc_bytes = bytes(loc_list)
            root.update()
            assign_tag(loc_bytes)
            print("done")
        except ValueError :
            error_label= tk.Label(root, text="Invalid Location", font=("Helvetica", 18))
            error_label.grid(column=1, row=70)            
    
    my_label = tk.Label(root, text="Enter Location in order room furniture drawer, column, row with spaces", font=("Helvetica", 15))
    my_label.grid(column=1, row=40)
    my_label = tk.Label(root, text="Ex : D265 Tiro-clas 2 9 1", font=("Helvetica", 10))
    my_label.grid(column=1, row=45)
    
    my_entry = tk.Entry(root, width=20, font=("Helvetica", 18))
    my_entry.grid(column=1, row=50)
    button_done= tk.Button(root, text="Done", command= display_value)
    button_done.grid(column=1, row=60)

read_button = tk.Button(root, text="Search components' informations", command=read_data)

write_button = ttk.Button(root, text="Click to assign ID to tag", command=write_loc)


read_button.grid(column=1, row=20)
write_button.grid(column=1, row=30)

root.mainloop()
