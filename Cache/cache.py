import os , json

DOSSIER_CACHE="Cache"

def charge_cache(id_livre,tache):

    """ Fonction de chargement de du cache si existant """

    chemin_fichier = os.path.join(DOSSIER_CACHE, f"{id_livre}_{tache}.json")

    try : 
        if os.path.exists(chemin_fichier):
            with open(chemin_fichier, "r", encoding="utf-8") as file:
                return json.load(file)
        return None
    except :
        print(f"Erreur chache , Impossible de recherche le livre {id_livre} en cache")

def sauvegarde_cache(id_livre, tache, data):

    """Creation du cache avec ID et fonction utilisé , cache en json"""
    
    if not os.path.exists(DOSSIER_CACHE):
        os.makedirs(DOSSIER_CACHE)
    
    try :
        chemin_fichier = os.path.join(DOSSIER_CACHE,f"{id_livre}_{tache}.json")
        with open(chemin_fichier,"w", encoding="utf-8") as f:
            json.dump(data,f, indent=4, ensure_ascii=False)
    except:
        print("Sauvegare du cache impossible pour le livre : {id_livre} avec le fonction : {tache}" )
        

