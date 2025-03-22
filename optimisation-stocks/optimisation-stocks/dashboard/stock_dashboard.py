import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Définir le répertoire de travail
base_path = "C:/Users/Lenovo/Desktop/Projet_Gestion_Stock"
os.chdir(base_path)

# 1. Charger les données
df_stock = pd.read_csv("Données_Nettoyées/recommandations_stock.csv", encoding="utf-8-sig")

# 2. Titre du tableau de bord
st.title("Tableau de bord : Optimisation des stocks")

# 3. Filtre interactif pour choisir un produit
produit = st.selectbox("Choisir un produit", df_stock["Produit"].unique())

# 4. Afficher les recommandations pour le produit sélectionné
st.subheader(f"Recommandations pour {produit}")
stock_produit = df_stock[df_stock["Produit"] == produit]
st.write(stock_produit[["Quantité en stock", "Point de commande", "Quantité à commander", "Coût total estimé"]])

# 5. Graphique en barres pour le produit sélectionné
st.subheader("Comparaison visuelle")
fig, ax = plt.subplots(figsize=(8, 5))
x = ["Quantité en stock", "Point de commande"]
y = stock_produit[["Quantité en stock", "Point de commande"]].values[0]
ax.bar(x, y, color=["blue", "orange"])
ax.set_title(f"Stock actuel vs Point de commande pour {produit}")
ax.set_ylabel("Quantité")
ax.grid(True, axis="y", linestyle="--", alpha=0.7)
st.pyplot(fig)

# 6. Indicateurs clés (KPI)
st.subheader("Indicateurs clés")
quantite_stock = stock_produit["Quantité en stock"].values[0]
point_commande = stock_produit["Point de commande"].values[0]
if quantite_stock < point_commande:
    st.warning(f"Risque de rupture : Stock ({quantite_stock}) < Point de commande ({point_commande})")
elif quantite_stock > point_commande * 1.2:
    st.warning(f"Surstockage potentiel : Stock ({quantite_stock}) > 120% du Point de commande")
else:
    st.success("Stock optimal")

# 7. Tableau complet (optionnel)
st.subheader("Vue d’ensemble de tous les produits")
st.dataframe(df_stock)