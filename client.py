import socket
import pickle
from phe import paillier
from pyope.ope import OPE

cle_pub, cle_priv = paillier.generate_paillier_keypair()
ope = OPE(b'secret_key_pro_16') 

def send(data):
    s = socket.socket()
    s.connect(("127.0.0.1", 5050))
    s.send(pickle.dumps(data))
    res = s.recv(10240)
    s.close()
    return res

while True:
    print("\n 1. Ajouter \n 2. Comparer \n 3. Somme \n 4. Quitter")
    choice = input("-> ")

    if choice == "1":
        nom = input("Nom : ")
        salaire = int(input("Salaire : "))
        
        # Chiffrement local
        paillier_chiffre = cle_pub.encrypt(salaire)
        ope_chiffre = ope.encrypt(salaire)

        paquet = {
            "action": "ajout",
            "nom": nom,
            "chiffre_paillier": pickle.dumps(paillier_chiffre),
            "chiffre_ope": ope_chiffre
        }
        if send(paquet) == b"OK":
            print(f"Utilisateur ajouté !")

    elif choice == "2":
        a = input("Nom 1 : ")
        b = input("Nom 2 : ")
        res = send({"action": "comparer", "nom_a": a, "nom_b": b}).decode()
        
        if res == "?":
            print("Erreur : utilisateur non trouvé")
        else:
            print(f" {a} a un salire {res} a celui de {b}")

    elif choice == "3":
        reponse_serveur = send({"action": "somme"})
        if reponse_serveur:
            total_objet = pickle.loads(reponse_serveur)
            if total_objet is None:
                print("Il n'y a pas de salaire !")
            else:
                # Déchiffrement final par le client
                total_reel = cle_priv.decrypt(total_objet)
                print(f"Somme totale = {total_reel}")

    elif choice == "4":
        print("Stop")
        break