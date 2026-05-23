tableau_equiv= [["NaN","Patricia", "D265"] , ["NaN", "tiro-class"] , [i for i in range(32)] , [i for i in range(16)] , [i for i in range(16)]]
import serial
from tkinter import Entry, Label, END

def decode(data):
    # entree: bytes
    # supp 1B salle et meuble; 1B tiroir; 1B col et ligne
    # returns list of string: location as text
    data_hex= data.hex()
    loc= [0]*5
    loc[0]= int( data_hex[:2], 16)
    loc[1]= int( data_hex[2:4], 16)
    loc[2]= int( data_hex[4:8], 16)
    loc[3]= int( data_hex[8:10], 16)
    loc[4]= int( data_hex[10:12], 16)

    loc_str= [ tableau_equiv[elt] for elt in loc ]
    return loc_str

def loc_a_ecrire():
    # demande quelle loc ecrire ds tag et la renvoie en bytes
    my_label= Label(root, text="Enter Location in order room furniture drawer, column, row with spaces", font=("Helvetica", 24))
    my_label.pack(pady=20)
    error_label = Label(root, text="", font=("Helvetica", 24))
    error_label.pack(pady=20)

    my_entry= Entry(root, width=20, font=("Helvetica", 24))
    my_entry.pack(20)
    ok= 0
    loc_list= []

    while ok == 0:
        if my_entry.get():
            loc= my_entry.get()
            my_entry.delete(0, END)
        loc_list= loc.rsplit(" ")
        if len(loc_list) != 5:
            error_label.config(text="Invalid Location")
            ok= 0
        else:
            ok= 1

    for i in range(5):
        loc_list[i]= tableau_equiv[i].index(loc[i])
    return bytes(loc_list)

def assign_tag(loc_bytes):
    # change ID tag pour loc en parametres
    # type bytes
    # attention timeout port
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    nb_bytes= ser.write(loc_bytes)
    ser.close()
    print("Sent "+ nb_bytes +" bytes.")