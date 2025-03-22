import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Définir le répertoire de travail
base_path = "C:/Users/Lenovo/Desktop/Projet_Gestion_Stock"
os.chdir(base_path)
print("Répertoire de travail actuel :", os.getcwd())

# Créer un dossier pour les résultats
if not os.path.exists("Figures"):
    os.makedirs("Figures")

# 1. Charger les données
df_ventes = pd.read_csv("Données_Nettoyées/ventes_nettoye.csv", encoding="utf-8-sig")
df_stock = pd.read_csv("Données_Nettoyées/stock_nettoye.csv", encoding="utf-8-sig")

# 2. Supprimer les doublons dans stock (prendre la moyenne et arrondir à l'entier)
df_stock = df_stock.groupby("Produit").agg({
    "Quantité en stock": lambda x: int(round(x.mean())),
    "Coût de stockage par produit (€)": "mean"
}).reset_index()

# 3. Calcul des statistiques par produit
ventes_par_produit = df_ventes.groupby("Produit")["Quantité vendue"].agg(["mean", "std"]).reset_index()
ventes_par_produit.columns = ["Produit", "Demande moyenne", "Écart-type"]

# Hypothèse : Délai d’approvisionnement moyen en jours
delai_approvisionnement = 7

# 4. Calcul du stock de sécurité et point de commande (entiers)
Z = 1.65  # Niveau de service 95%
ventes_par_produit["Stock de sécurité"] = (Z * ventes_par_produit["Écart-type"] * np.sqrt(delai_approvisionnement)).astype(int)
ventes_par_produit["Point de commande"] = ((ventes_par_produit["Demande moyenne"] * delai_approvisionnement / 30) + ventes_par_produit["Stock de sécurité"]).astype(int)

# Fusionner avec le stock actuel
stock_optimal = df_stock.merge(ventes_par_produit, on="Produit", how="left")

# 5. Simulation de scénarios (entier)
stock_optimal["Quantité à commander"] = stock_optimal.apply(
    lambda row: max(0, row["Point de commande"] - row["Quantité en stock"]), axis=1
).astype(int)

# 6. Calcul du coût total estimé (arrondi à 2 décimales, car c’est une valeur monétaire)
stock_optimal["Coût total estimé"] = (stock_optimal["Quantité à commander"] * stock_optimal["Coût de stockage par produit (€)"]).round(2)

# Vérification avant exportation
print("Aperçu des données avant exportation :")
print(stock_optimal[["Produit", "Quantité en stock", "Point de commande", "Quantité à commander", "Coût total estimé"]].head())

# 7. Exportation avec format adapté
stock_optimal.to_csv("Données_Nettoyées/recommandations_stock.csv", index=False, encoding="utf-8-sig")
print("Recommandations exportées dans 'Données_Nettoyées/recommandations_stock.csv'.")

# 8. Visualisation
plt.figure(figsize=(12, 6))
plt.bar(stock_optimal["Produit"], stock_optimal["Quantité en stock"], label="Stock actuel", color="blue", width=0.4)
plt.bar(stock_optimal["Produit"], stock_optimal["Point de commande"], label="Point de commande", color="orange", width=0.2, alpha=0.7)
plt.title("Stock actuel vs Point de commande par produit")
plt.xlabel("Produit")
plt.ylabel("Quantité")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)
plt.grid(True, axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("Figures/stock_vs_point_commande_corrige.png")
plt.show()