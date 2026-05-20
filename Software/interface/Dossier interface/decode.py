tableau_equiv= [["NaN","Patricia", "D265"] , ["NaN", "tiro-class"]]


def decode(data):
    # supp 1B salle et meuble; 1B tiroir; 1B col et ligne
    # returns array
    loc= [0]*5
    loc[0]= int(data[:2], 16)
    loc[1]= int(data[2:4], 16)
    loc[2]= int(data[4:8], 16)
    loc[3]= int(data[8:10], 16)
    loc[4]= int(data[10:12], 16)
    returns loc



def message(emplacement):