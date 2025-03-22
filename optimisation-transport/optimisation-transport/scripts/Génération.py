import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Paramètres pour simuler des données réalistes
np.random.seed(42)  # Pour reproductibilité
nb_lignes = 100  # Nombre d'enregistrements
dates = [datetime(2024, 1, 1) + timedelta(days=random.randint(0, 364)) for _ in range(nb_lignes)]
transporteurs = ["Transco1", "Transco2", "Transco3"]
zones = ["Tanger Centre", "Tétouan", "Asilah"]

# Génération des données
data = {
    "Date": dates,
    "Transporteur": [random.choice(transporteurs) for _ in range(nb_lignes)],
    "Zone_Destination": [random.choice(zones) for _ in range(nb_lignes)],
    "Distance_km": np.random.uniform(10, 100, nb_lignes).round(2),  # Distances entre 10 et 100 km
    "Cout_Total_MAD": np.random.uniform(50, 500, nb_lignes).round(2),  # Coûts entre 50 et 500 MAD
    "Temps_Trajet_h": np.random.uniform(0.5, 5, nb_lignes).round(2),  # Temps entre 0.5 et 5 heures
    "Volume_m3": np.random.uniform(1, 20, nb_lignes).round(2),  # Volume entre 1 et 20 m³
    "Tarif_Transporteur_MAD_km": [random.uniform(2, 5) for _ in range(nb_lignes)],  # Tarif par km
    "Prix_Carburant_MAD_L": np.random.uniform(10, 15, nb_lignes).round(2),  # Prix carburant
    "Indice_Trafic": np.random.uniform(1, 10, nb_lignes).round(1)  # 1 = fluide, 10 = congestionné
}

# Création du DataFrame
df = pd.DataFrame(data)

# Ajouter quelques données manquantes ou aberrantes pour simuler la réalité
df.loc[5, "Distance_km"] = -10  # Valeur aberrante
df.loc[10, "Cout_Total_MAD"] = np.nan  # Valeur manquante
df.loc[15, "Temps_Trajet_h"] = np.nan  # Valeur manquante

# Sauvegarde en CSV
df.to_csv("donnees_transport_ecommerce.csv", index=False)
print("Fichier CSV 'donnees_transport_ecommerce.csv' généré avec succès !")
print(df.head())