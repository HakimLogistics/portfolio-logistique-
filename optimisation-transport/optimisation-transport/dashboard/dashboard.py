import pandas as pd
import numpy as np
import os
import streamlit as st
import plotly.express as px

# Définir le chemin du dossier
path = r"C:\Users\Lenovo\Desktop\transport_projet"
os.chdir(path)

# Charger les données nettoyées
df = pd.read_csv("donnees_transport_nettoyees.csv")
print("Données chargées avec succès")  # Vérification

# Titre du tableau de bord
st.title("Tableau de Bord Interactif - Optimisation des Coûts de Transport")
st.write("Tableau de bord démarré !")  # Confirmation dans l'interface

# Paramètres de simulation
st.sidebar.header("Paramètres d’Optimisation")
remplissage_boost = st.sidebar.slider("Augmentation du remplissage (%)", 0, 50, 20, step=5)
cout_km_reduction = st.sidebar.slider("Réduction du coût/km (%)", 0, 20, 10, step=5)
trajets_reduction = st.sidebar.slider("Réduction des trajets (%)", 0, 50, 30, step=5)

# Calcul du scénario optimisé
cout_actuel_total = df["Cout_Total_MAD"].sum()
df_opt = df.copy()
df_opt["Volume_m3"] *= (1 + remplissage_boost / 100)
df_opt["Cout_par_km"] *= (1 - cout_km_reduction / 100)
nb_trajets_opt = len(df_opt) * (1 - trajets_reduction / 100)
cout_opt_total = (df_opt["Cout_par_km"] * df_opt["Distance_km"]).sum() * (nb_trajets_opt / len(df_opt))
economie = cout_actuel_total - cout_opt_total

# Affichage des résultats
st.header("Résultats Généraux")
st.write(f"Coût Actuel Total : {cout_actuel_total:.2f} MAD")
st.write(f"Coût Optimisé Total : {cout_opt_total:.2f} MAD")
st.write(f"Économie Réalisée : {economie:.2f} MAD")

# Graphique de comparaison
fig = px.bar(
    x=["Actuel", "Optimisé"],
    y=[cout_actuel_total, cout_opt_total],
    color=["Actuel", "Optimisé"],
    color_discrete_map={"Actuel": "gray", "Optimisé": "green"},
    labels={"y": "Coût Total (MAD)"},
    title="Comparaison des Coûts"
)
st.plotly_chart(fig)
print("Graphique généré")  # Vérification