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



class AppStock:


        # --- Zone d'affichage des résultats ---
        self.result_frame = tk.LabelFrame(root, text=" Informations Composant ", padx=20, pady=20)
        self.result_frame.pack(padx=20, pady=20, fill="both", expand=True)

        self.lbl_mpn = tk.Label(self.result_frame, text="Modèle : -", font=("Arial", 12, "bold"))
        self.lbl_mpn.pack(anchor="w")

        self.lbl_stock = tk.Label(self.result_frame, text="Stock : -", font=("Arial", 12))
        self.lbl_stock.pack(anchor="w")

        self.lbl_loc = tk.Label(self.result_frame, text="Emplacement : -", font=("Arial", 12), fg="blue")
        self.lbl_loc.pack(anchor="w")

        self.btn_quitter = tk.Button(root, text="Quitter", command=root.quit)
        self.btn_quitter.pack(pady=10)

    def rechercher(self, event=None):
        recherche = self.entree.get().strip()
        fichier = '2526_Stock_components(components).csv'
        trouve = False

        try:
            with open(fichier, mode='r', encoding='utf-8') as f:
                # Utilisation du délimiteur ; comme dans ton fichier
                lecteur = csv.DictReader(f, delimiter=';')
                for ligne in lecteur:
                    # On cherche dans MPN, Value ou une colonne RFID
                    if (recherche.lower() in ligne.get('MPN', '').lower() or 
                        recherche.lower() in ligne.get('Value', '').lower()):
                        
                        self.afficher_infos(ligne)
                        trouve = True
                        break
            
            if not trouve:
                messagebox.showwarning("Non trouvé", f"Aucun composant pour : {recherche}")
            
            self.entree.delete(0, tk.END) # Efface pour le prochain scan
            
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier CSV introuvable !")

    def afficher_infos(self, ligne):
        self.lbl_mpn.config(text=f"Modèle : {ligne['MPN']}")
        self.lbl_stock.config(text=f"Stock actuel : {ligne['Quantity']} pièces")
        
        # On combine les infos d'emplacement de ton fichier
        loc = f"Tiroir {ligne['Drawer']} / Col {ligne['Column']} / Rang {ligne['Raw']}"
        self.lbl_loc.config(text=f"Emplacement : {loc}")

# Lancement de l'interface
root = tk.Tk()
app = AppStock(root)
root.mainloop()

'''

import tkinter as tk
from tkinter import ttk
import pandas as pd
import serial
import time

tableau_equiv= [["NaN","Patricia", "D265"] , ["NaN", "Tiro-clas"]]


def simu_scan(room, f, drawer,column, raw):
    return bytes([room,f,drawer,column,raw])


def scan():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    # reads everything after waiting for data to be sent
    while not ser.in_waiting:
        time.sleep(0.5)
    data = ser.read_all()
    # closing connection
    ser.close()
    return data


def decode(data):
    # entree: bytes
    # supp 1B salle et meuble; 1B tiroir; 1B col et ligne
    # returns list of string: location as text
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
    df = pd.read_excel("../Excel/2526_Stock_components.xlsx", header=0, skiprows=1, sheet_name='components', usecols="E:U")
    print(df)
    condition = (df['Room'] == loc[0]) & (df['Furniture'] == loc[1]) & (df['Drawer'] == loc[2]) & (
                df['Column'] == loc[3]) & (df['Raw'] == loc[4])
    resultat = df[condition]
    print("Resu:",resultat)
    mpn = (resultat['MPN'].values[0])
    sku = (resultat['Supplier Ref'].values[0])
    return mpn, sku


def display_info(mpn, sku, loc):
    # texte_mpn = tk.StringVar(value="MPN ")
    # texte_loc = tk.StringVar(value="Emplacement ")
    # texte_sku = tk.StringVar(value="SKU")
    texte_loc.set(f"Emplacement : Salle {loc[0]} Furniture {loc[1]} Tiroir {loc[2]} Colonne {loc[3]} Ligne {loc[4]}")
    texte_mpn.set(f"MPN : {mpn}")
    texte_sku.set(f"SKU : {sku}")


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


def assign_tag():
    # change ID tag pour loc en parametres
    # type bytes
    # attention timeout port
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    nb_bytes= ser.write(loc_bytes)
    ser.close()
    ttk.Label(mainframe, text="Sent {nb_bytes} bytes." ,).grid(column=1, row=70)


#texte_loc.set(f"Emplacement : Salle {nonassigne('Room',0)} {nonassigne('Furniture',0)} Tiroir {nonassigne('Drawer',2)} Colonne {nonassigne('Column',3)} Ligne {nonassigne('Raw',4)}")

'''def init_interface():
    root = tk.Tk()
    
    root.title("Gestion des inventaires")
    
    root.state('zoomed')
    mainframe = tk.ttk.Frame(root, padding=(3, 3, 100, 100))
    mainframe.grid(column=0, row=3, sticky=(tk.N, tk.W, tk.E, tk.S))
    

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

    root.mainloop()'''

root = tk.Tk()
    
root.title("Gestion des inventaires")

root.state(newstate='icon')
mainframe = ttk.Frame(root, padding=(3, 3, 100, 100))
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
 
texte_mpn = tk.StringVar(value="MPN ")
texte_loc = tk.StringVar(value="Emplacement ")

texte_sku = tk.StringVar(value="SKU")
ttk.Label(mainframe, text="Scannez un nouveau composant " ,).grid(column=2, row=0)
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
def start():
    data= simu_scan(2,1,2,9,1)
    loc_str= decode(data)
    mpn, sku= search_info(loc_str)
    display_info(mpn, sku, loc_str)
    root.update()
    button= ttk.Button(mainframe, text="Click to assign ID to tag", command=loc_a_ecrire)
    button.grid(column=1, row=80)
    root.update()
    assign_tag()

start_button = tk.Button(root, text="Start scanning", command=start)
start_button.grid(column=1, row=50)
root.mainloop()