import json
import os 

def gamemode_directory(gamemode): # Bestimmt passendes Verzeichnis mit Fragen anhand des gewählten Spielmodus aus

    if gamemode == "l4d_1-40":
        mode_directory = ['l4d', '1-40']
    elif gamemode == "l4d_41-80":
        mode_directory = ['l4d', '41-80']
    elif gamemode == "l4d_81-136":
        mode_directory = ['l4d', '81-136']
    elif gamemode == "l4d_complete":
        print("not available yet") # Wird im späteren Verlauf integriert   
        pass
    elif gamemode == "xt":
        mode_directory = ["xt"]
    else:
        print("Error: Mode not found")
        mode_directory = "Error"
    
    act_path = os.path.dirname(os.path.abspath(__file__))
    dict_path = os.path.dirname(act_path)
    mode_path = [dict_path,"data","questions"]+ mode_directory
    directory = os.path.join("/".join(mode_path))
    return directory


