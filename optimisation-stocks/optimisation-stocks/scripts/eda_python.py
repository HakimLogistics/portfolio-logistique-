import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurer Seaborn pour des graphiques esthétiques
sns.set(style="whitegrid")

# Définir le répertoire de travail
base_path = "C:/Users/Lenovo/Desktop/Projet_Gestion_Stock"
os.chdir(base_path)
print("Répertoire de travail actuel :", os.getcwd())

# Créer le dossier Figures s'il n'existe pas
if not os.path.exists("Figures"):
    os.makedirs("Figures")

# 1. Charger les données nettoyées avec gestion d’encodage
try:
    df_ventes = pd.read_csv("Données_Nettoyées/ventes_nettoye.csv", encoding="utf-8-sig")
except UnicodeDecodeError:
    print("Erreur UTF-8 pour ventes_nettoye.csv, tentative avec latin-1...")
    df_ventes = pd.read_csv("Données_Nettoyées/ventes_nettoye.csv", encoding="latin-1")

try:
    df_stock = pd.read_csv("Données_Nettoyées/stock_nettoye.csv", encoding="utf-8-sig")
except UnicodeDecodeError:
    print("Erreur UTF-8 pour stock_nettoye.csv, tentative avec latin-1...")
    df_stock = pd.read_csv("Données_Nettoyées/stock_nettoye.csv", encoding="latin-1")

# Vérification des données pour l'histogramme
print("Vérification de 'Quantité vendue' :")
print(df_ventes["Quantité vendue"].describe())
df_ventes["Quantité vendue"] = pd.to_numeric(df_ventes["Quantité vendue"], errors="coerce")

# 2. Visualisation des tendances de la demande
# a. Histogramme de la quantité vendue par produit
plt.figure(figsize=(12, 6))
sns.histplot(data=df_ventes, x="Quantité vendue", bins=20, kde=True)
plt.title("Distribution des quantités vendues")
plt.xlabel("Quantité vendue")
plt.ylabel("Fréquence")
plt.savefig("Figures/hist_quantite_vendue.png")
plt.show()

# b. Courbe de tendance des ventes par mois
ventes_par_mois = df_ventes.groupby("mois")["Quantité vendue"].sum().reset_index()
ventes_par_mois["mois"] = ventes_par_mois["mois"].astype(str)
plt.figure(figsize=(12, 6))
sns.lineplot(data=ventes_par_mois, x="mois", y="Quantité vendue", marker="o")
plt.title("Tendance des ventes par mois (Mars 2024 - Février 2025)")
plt.xlabel("Mois")
plt.ylabel("Quantité vendue totale")
plt.xticks(rotation=45)
plt.savefig("Figures/tendance_ventes_mois.png")
plt.show()

# 3. Analyse de la saisonnalité
ventes_region_mois = df_ventes.pivot_table(index="Région", columns="mois", values="Quantité vendue", aggfunc="sum")
plt.figure(figsize=(12, 6))
sns.heatmap(ventes_region_mois, annot=True, cmap="YlGnBu", fmt=".0f")
plt.title("Saisonnalité des ventes par région et mois")
plt.xlabel("Mois")
plt.ylabel("Région")
plt.savefig("Figures/heatmap_saisonnalite.png")
plt.show()

# 4. Identification des corrélations
# a. Corrélation entre mois et quantité vendue par région
df_ventes["mois_num"] = pd.to_datetime(df_ventes["Date de commande"]).dt.month
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_ventes, x="mois_num", y="Quantité vendue", hue="Région", size="Quantité vendue")
plt.title("Corrélation entre mois et quantité vendue par région")
plt.xlabel("Mois (1-12)")
plt.ylabel("Quantité vendue")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("Figures/correlation_mois_ventes.png")
plt.show()

# b. Corrélation entre stock et coût de stockage
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_stock, x="Quantité en stock", y="Coût de stockage par produit (€)", hue="Produit")
plt.title("Corrélation entre stock et coût de stockage")
plt.xlabel("Quantité en stock")
plt.ylabel("Coût de stockage (€)")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("Figures/correlation_stock_cout.png")
plt.show()

print("Analyse exploratoire terminée. Graphiques corrigés enregistrés dans 'Projet_Gestion_Stock/Figures/'.")