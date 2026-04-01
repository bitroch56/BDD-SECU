import mysql.connector
import numpy as np
import pickle

def effectuer_attaque_sur_bdd():
    # 1. Connexion à TA base de données
    try:
        bdd = mysql.connector.connect(
            host="localhost",
            user="Chaveneau",
            password="mysql",
            database="TP_SecuBDD_Menez_Chaveneau"
        )
        curseur = bdd.cursor()
        
        # 2. Récupération de TOUTES les valeurs OPE (l'ordre)
        # On récupère aussi le nom pour vérifier si l'estimation est cohérente
        curseur.execute("SELECT nom, salaire_ordre FROM employes")
        resultats = curseur.fetchall()
        bdd.close()

        if not resultats:
            print("La base de données est vide. Ajoutez des employés avant d'attaquer !")
            return

        # On sépare les noms et les valeurs chiffrées
        noms = [r[0] for r in resultats]
        valeurs_ope = [r[1] for r in resultats]

        # 3. LE MODÈLE STATISTIQUE (Distribution publique supposée)
        # Imaginons que l'attaquant sache que la moyenne est 40k et l'écart-type 15k
        nb_points_modele = 100
        modele_public = np.random.normal(loc=2000, scale=500, size=nb_points_modele)
        modele_public.sort()

        # 4. TRI DES DONNÉES CHIFFRÉES
        # On trie les couples (valeur_ope, nom) pour garder la correspondance
        donnees_triees = sorted(zip(valeurs_ope, noms))
        nb_employes = len(donnees_triees)

        print(f"\n=== RÉSULTATS DE L'ATTAQUE SUR {nb_employes} EMPLOYÉS ===")
        print(f"{'Nom':<15} | {'Valeur OPE':<15} | {'Estimation':<15}")
        print("-" * 50)

        for i, (val_ope, nom) in enumerate(donnees_triees):
            # On calcule le rang percentile
            index_modele = int((i / nb_employes) * nb_points_modele)
            estimation = modele_public[index_modele]
            
            print(f"{nom:<15} | {val_ope:<15} | {estimation:,.2f}€")

    except Exception as e:
        print(f"Erreur lors de l'attaque : {e}")

if __name__ == "__main__":
    effectuer_attaque_sur_bdd()