import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

# Définir le chemin du dossier
path = r"C:\Users\Lenovo\Desktop\transport_projet"
os.chdir(path)

# Charger les données nettoyées
df = pd.read_csv("donnees_transport_nettoyees.csv")

# 1. Stratégies d'optimisation
capacite_max_m3 = 20
df["Taux_Remplissage"] = df["Volume_m3"] / capacite_max_m3 * 100
mean_remplissage = df["Taux_Remplissage"].mean()
print(f"Taux de remplissage moyen actuel : {mean_remplissage:.2f}%")
if mean_remplissage < 80:
    print("Recommandation : Augmenter le taux de remplissage à >80%.")

cost_by_transporter = df.groupby("Transporteur")[["Cout_par_km", "Temps_Trajet_h"]].mean()
best_transporter = cost_by_transporter["Cout_par_km"].idxmin()
print(f"\nMeilleur transporteur : {best_transporter}")
print(cost_by_transporter)

trajets_par_zone = df.groupby("Zone_Destination").size()
print(f"\nNombre de trajets par zone :\n{trajets_par_zone}")
print("Recommandation : Regrouper les commandes par zone.")

# 2. Simulation d'impact
cout_actuel_total = df["Cout_Total_MAD"].sum()
print(f"\nCoût total actuel : {cout_actuel_total:.2f} MAD")

df_opt = df.copy()
df_opt["Volume_m3"] *= 1.2
df_opt["Cout_par_km"] *= 0.9
nb_trajets_opt = len(df_opt) * 0.7
cout_opt_total = (df_opt["Cout_par_km"] * df_opt["Distance_km"]).sum() * (nb_trajets_opt / len(df_opt))
print(f"Coût total optimisé : {cout_opt_total:.2f} MAD")
print(f"Économie estimée : {cout_actuel_total - cout_opt_total:.2f} MAD")

# 3. Visualisations statiques
plt.figure(figsize=(8, 5))
plt.bar(["Actuel", "Optimisé"], [cout_actuel_total, cout_opt_total], color=["gray", "green"])
plt.title("Comparaison des Coûts")
plt.ylabel("Coût Total (MAD)")
plt.savefig("cost_comparison.png")
plt.show()

plt.figure(figsize=(8, 5))
cost_by_transporter["Cout_par_km"].plot(kind="bar", color="blue")
plt.title("Coût par km par Transporteur")
plt.ylabel("Coût par km (MAD)")
plt.savefig("cost_by_transporter.png")
plt.show()