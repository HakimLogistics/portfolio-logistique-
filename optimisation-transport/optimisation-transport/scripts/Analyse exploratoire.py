import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap
import os

# Définir le chemin du dossier
path = r"C:\Users\Lenovo\Desktop\transport_projet"
os.chdir(path)  # Changer le répertoire de travail

# Charger les données nettoyées
df = pd.read_csv("donnees_transport_nettoyees.csv")
print("Aperçu des données nettoyées :")
print(df.head())

# 1. Analyse des coûts par trajet, transporteur et distance
# Coût moyen par transporteur
cost_by_transporter = df.groupby("Transporteur")["Cout_Total_MAD"].mean().sort_values(ascending=False)
print("\nCoût moyen par transporteur :")
print(cost_by_transporter)

# Coût par km par transporteur
cost_per_km = df.groupby("Transporteur")["Cout_par_km"].mean().sort_values(ascending=False)
print("\nCoût par km par transporteur :")
print(cost_per_km)

# 2. Identification des trajets les plus coûteux
expensive_trips = df.nlargest(5, "Cout_Total_MAD")[["Date", "Transporteur", "Zone_Destination", "Distance_km", "Cout_Total_MAD"]]
print("\nTop 5 des trajets les plus coûteux :")
print(expensive_trips)

# 3. Visualisations
# Graphique 1 : Coût total par transporteur (Barplot)
plt.figure(figsize=(10, 6))
sns.barplot(x=cost_by_transporter.index, y=cost_by_transporter.values, palette="Blues_d")
plt.title("Coût Total Moyen par Transporteur")
plt.xlabel("Transporteur")
plt.ylabel("Coût Total Moyen (MAD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cout_par_transporteur.png")
plt.show()

# Graphique 2 : Coût par km vs Distance (Scatterplot)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="Distance_km", y="Cout_par_km", hue="Transporteur", size="Volume_m3", alpha=0.6)
plt.title("Coût par km en fonction de la Distance et du Volume")
plt.xlabel("Distance (km)")
plt.ylabel("Coût par km (MAD/km)")
plt.legend(title="Transporteur")
plt.tight_layout()
plt.savefig("cout_par_km_vs_distance.png")
plt.show()

# Graphique 3 : Boxplot des coûts par zone de destination
plt.figure(figsize=(10, 6))
sns.boxplot(x="Zone_Destination", y="Cout_Total_MAD", data=df, palette="Set2")
plt.title("Distribution des Coûts par Zone de Destination")
plt.xlabel("Zone de Destination")
plt.ylabel("Coût Total (MAD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("cout_par_zone.png")
plt.show()

# 4. Visualisation des itinéraires sur une carte (exemple simplifié avec coordonnées fictives)
# Coordonnées approximatives pour Tanger et ses environs
coords = {
    "Tanger Centre": [35.7595, -5.8340],
    "Tétouan": [35.5785, -5.3684],
    "Asilah": [35.4652, -6.0351]
}

# Créer une carte centrée sur Tanger
m = folium.Map(location=[35.7595, -5.8340], zoom_start=10)

# Ajouter des points pour chaque zone
for zone, coord in coords.items():
    folium.Marker(coord, popup=zone).add_to(m)

# Ajouter une heatmap basée sur les coûts
heat_data = [[coords[row["Zone_Destination"]][0], coords[row["Zone_Destination"]][1], row["Cout_Total_MAD"]] 
             for index, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

# Sauvegarder la carte
m.save("carte_couts_transport.html")
print("\nCarte interactive sauvegardée sous 'carte_couts_transport.html'")

# 5. Résumé des opportunités d’optimisation
print("\nOpportunités d’optimisation :")
print("- Transporteurs coûteux :", cost_by_transporter.index[:2].tolist())
print("- Zones avec coûts élevés :", df.groupby("Zone_Destination")["Cout_Total_MAD"].mean().idxmax())
print("- Trajets longs et coûteux à regrouper :", expensive_trips["Zone_Destination"].tolist())