import socket
import pickle
import mysql.connector

# Connexion à la base de données
bdd = mysql.connector.connect(
    host="localhost", 
    user="test", 
    password="test", 
    database="TP_SecuBDD_Menez_Chaveneau"
)
curseur = bdd.cursor(buffered=True)

def demarrer_serveur():
    serveur_socket = socket.socket()
    serveur_socket.bind(("127.0.0.1", 5050))
    serveur_socket.listen(5)
    print("Serveur sue le port 5050...")

    while True:
        connexion, adresse = serveur_socket.accept()
        try:
            donnees_brutes = connexion.recv(10240) 
            if not donnees_brutes: continue
            requete = pickle.loads(donnees_brutes)

            action = requete.get("action")

            # AJOUT d'un employé
            if action == "ajout":
                curseur.execute(
                    "INSERT INTO employes (nom, salaire_chiffre, salaire_ordre) VALUES (%s, %s, %s)",
                    (requete["nom"], requete["chiffre_paillier"], requete["chiffre_ope"])
                )
                bdd.commit()
                connexion.send(b"OK")

            # COMPARAISON de deux salaires
            elif action == "comparer":
                curseur.execute("SELECT salaire_ordre FROM employes WHERE nom=%s", (requete["nom_a"],))
                res_a = curseur.fetchone()
                curseur.execute("SELECT salaire_ordre FROM employes WHERE nom=%s", (requete["nom_b"],))
                res_b = curseur.fetchone()

                if res_a and res_b:
                    val_a, val_b = res_a[0], res_b[0]
                    signe = ">" if val_a > val_b else "<" if val_a < val_b else "="
                    connexion.send(signe.encode())
                else:
                    connexion.send(b"?")

            # SOMME homomorphe des salaires
            elif action == "somme":
                curseur.execute("SELECT salaire_chiffre FROM employes")
                lignes = curseur.fetchall()
                
                total_chiffre = None
                for (blob,) in lignes:
                    objet_chiffre = pickle.loads(blob)
                    if total_chiffre is None:
                        total_chiffre = objet_chiffre
                    else:
                        # Addition homomorphe (Paillier)
                        total_chiffre += objet_chiffre 
                
                connexion.send(pickle.dumps(total_chiffre))

        except Exception as e:
            print(f"Erreur serveur : {e}")
        finally:
            connexion.close()

if __name__ == "__main__":
    demarrer_serveur()
