import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Définir le répertoire de travail
base_path = "C:/Users/Lenovo/Desktop/Projet_Gestion_Stock"
os.chdir(base_path)

# Créer le dossier Données_Brutes s'il n'existe pas
os.makedirs("Données_Brutes", exist_ok=True)

# Liste des 10 produits phares (uniques)
produits = [
    "Robe été", "Robe printemps", "Robe automne", "Robe hiver", "Robe cocktail",
    "Manteau hiver", "Manteau mi-saison", "Manteau léger", "Écharpe laine", "Ceinture cuir"
]

# Régions possibles
regions = ["Nord", "Sud", "Est", "Ouest", "Centre"]

# Fonction pour générer une date aléatoire
def random_date():
    start_date = datetime(2024, 3, 1)
    end_date = datetime(2025, 2, 28)
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + timedelta(days=random_days)

# Tableau 1 : Historique des ventes (200 lignes)
data_tableau1 = {
    "Date de commande": [random_date().strftime("%d/%m/%Y") for _ in range(200)],
    "Produit": [random.choice(produits) for _ in range(200)],
    "Quantité vendue": [random.randint(1, 20) for _ in range(200)],
    "Région": [random.choice(regions) for _ in range(200)]
}
df_tableau1 = pd.DataFrame(data_tableau1)

# Tableau 2 : Stock actuel (10 lignes, produits uniques)
data_tableau2 = {
    "Produit": produits,
    "Quantité en stock": [random.randint(5, 50) for _ in range(10)],
    "Coût de stockage par produit (€)": [round(random.uniform(0.5, 3.5), 2) for _ in range(10)]
}
df_tableau2 = pd.DataFrame(data_tableau2)

# Exportation
df_tableau1.to_csv("Données_Brutes/historique_ventes.csv", index=False, encoding="utf-8-sig")
df_tableau1.to_excel("Données_Brutes/historique_ventes.xlsx", index=False)
df_tableau2.to_csv("Données_Brutes/stock_actuel.csv", index=False, encoding="utf-8-sig")
df_tableau2.to_excel("Données_Brutes/stock_actuel.xlsx", index=False)

print("Fichiers générés avec succès : stock_actuel sans doublons.")