import pandas as pd
import numpy as np

# Charger les données
df = pd.read_csv("donnees_transport_ecommerce.csv")
print("Données brutes :")
print(df.head())

# Étape 1 : Suppression des valeurs aberrantes
df = df[df["Distance_km"] > 0]  # Supprimer distances négatives
df = df[df["Cout_Total_MAD"] > 0]  # Supprimer coûts négatifs ou nuls
df = df[df["Temps_Trajet_h"] > 0]  # Supprimer temps négatifs ou nuls
print("\nAprès suppression des valeurs aberrantes :")
print(df.describe())

# Étape 2 : Gestion des données manquantes
df["Cout_Total_MAD"].fillna(df["Cout_Total_MAD"].median(), inplace=True)  # Remplir avec la médiane
df["Temps_Trajet_h"].fillna(df["Temps_Trajet_h"].median(), inplace=True)
print("\nAprès gestion des données manquantes :")
print(df.isnull().sum())  # Vérifier qu'il n'y a plus de NaN

# Étape 3 : Transformation des données
df["Cout_par_km"] = df["Cout_Total_MAD"] / df["Distance_km"]  # Ajouter une colonne calculée
df["Date"] = pd.to_datetime(df["Date"])  # Convertir en format datetime
df = df.round({"Cout_par_km": 2, "Distance_km": 2})  # Arrondir pour lisibilité

# Étape 4 : Vérification de la cohérence
# Vérifier si le coût/km est cohérent avec les tarifs des transporteurs
df["Cout_Attendu"] = df["Distance_km"] * df["Tarif_Transporteur_MAD_km"]
df["Ecart_Cout"] = abs(df["Cout_Total_MAD"] - df["Cout_Attendu"])
print("\nÉcarts de coût détectés :")
print(df[df["Ecart_Cout"] > 50][["Transporteur", "Cout_Total_MAD", "Cout_Attendu", "Ecart_Cout"]])

# Étape 5 : Organisation en tableau croisé dynamique
pivot_table = pd.pivot_table(
    df,
    values=["Cout_Total_MAD", "Distance_km", "Temps_Trajet_h"],
    index=["Transporteur"],
    columns=["Zone_Destination"],
    aggfunc="mean",
    fill_value=0
)
print("\nTableau croisé dynamique :")
print(pivot_table)

# Sauvegarde des données nettoyées
df.to_csv("donnees_transport_nettoyees.csv", index=False)
print("\nFichier CSV 'donnees_transport_nettoyees.csv' généré avec succès !")