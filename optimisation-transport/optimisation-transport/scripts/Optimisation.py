import pandas as pd
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, value
import networkx as nx
import matplotlib.pyplot as plt
import os
from itertools import permutations

# Définir le chemin du dossier
path = r"C:\Users\Lenovo\Desktop\transport_projet"
os.chdir(path)

# Charger les données nettoyées
df = pd.read_csv("donnees_transport_nettoyees.csv")

# 1. TSP : Optimisation des tournées
coords = {
    "Tanger Centre": [35.7595, -5.8340],
    "Tétouan": [35.5785, -5.3684],
    "Asilah": [35.4652, -6.0351]
}

def distance(coord1, coord2):
    return np.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2) * 111  # Conversion en km

dist_matrix = {}
for z1 in coords:
    for z2 in coords:
        dist_matrix[(z1, z2)] = distance(coords[z1], coords[z2]) if z1 != z2 else 0

def tsp_shortest_path(zones):
    min_dist = float("inf")
    best_path = None
    for perm in permutations(zones):
        total_dist = 0
        for i in range(len(perm) - 1):
            total_dist += dist_matrix[(perm[i], perm[i+1])]
        total_dist += dist_matrix[(perm[-1], perm[0])]  # Retour au départ
        if total_dist < min_dist:
            min_dist = total_dist
            best_path = perm
    return best_path, min_dist

zones = list(coords.keys())
best_path, min_dist = tsp_shortest_path(zones)
print(f"Meilleur itinéraire TSP : {best_path}, Distance totale : {min_dist:.2f} km")

# Visualisation améliorée du TSP
G = nx.DiGraph()  # Graphe dirigé pour montrer l'ordre
for i in range(len(best_path) - 1):
    G.add_edge(best_path[i], best_path[i+1], weight=dist_matrix[(best_path[i], best_path[i+1])])
G.add_edge(best_path[-1], best_path[0], weight=dist_matrix[(best_path[-1], best_path[0])])  # Retour

plt.figure(figsize=(8, 6))
pos = coords
nx.draw(G, pos, with_labels=True, node_color="lightblue", node_size=500, font_size=10, arrows=True)
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels={k: f"{v:.1f} km" for k, v in labels.items()})
plt.title("Tournée Optimale TSP")
plt.savefig("tsp_tour.png")
plt.show()

# 2. Programmation linéaire avec PuLP
transporteurs = df["Transporteur"].unique()
zones = df["Zone_Destination"].unique()
costs = df.groupby(["Transporteur", "Zone_Destination"])["Cout_par_km"].mean().unstack().fillna(10)

prob = LpProblem("Allocation_Transporteurs", LpMinimize)
x = LpVariable.dicts("Assign", [(t, z) for t in transporteurs for z in zones], cat="Binary")
prob += lpSum([costs.loc[t, z] * x[(t, z)] for t in transporteurs for z in zones])
for z in zones:
    prob += lpSum([x[(t, z)] for t in transporteurs]) == 1
for t in transporteurs:
    prob += lpSum([x[(t, z)] for z in zones]) <= 1

prob.solve()
print("\nStatut de la résolution :", prob.status)
for v in prob.variables():
    if value(v) == 1:
        print(f"{v.name} = {value(v)}")

total_cost_opt = value(prob.objective)
print(f"Coût total optimisé par km (PuLP) : {total_cost_opt:.2f} MAD/km")

# 3. Simulation de scénarios
# Scénario 1 : Coût actuel
current_cost = df["Cout_Total_MAD"].sum() / len(df) * len(zones)  # Coût moyen ajusté pour 3 zones
print(f"\nScénario actuel - Coût total : {current_cost:.2f} MAD")

# Scénario 2 : Optimisation (TSP + Allocation)
# Hypothèse : Réduction de 20% des coûts grâce à l'optimisation (à ajuster avec données réelles)
optimized_cost = current_cost * 0.8  # Réduction simulée
print(f"Scénario optimisé (TSP + Allocation) : {optimized_cost:.2f} MAD")

# Scénario 3 : Augmentation de la demande (+20% volume)
df_sim = df.copy()
df_sim["Volume_m3"] *= 1.2
sim_cost = df_sim["Cout_Total_MAD"].sum() / len(df_sim) * len(zones) * 1.1  # +10% coût par surcharge
print(f"Scénario demande +20% : {sim_cost:.2f} MAD")

# Graphique comparatif corrigé
scenarios = ["Actuel", "Optimisé", "Demande +20%"]
costs = [current_cost, optimized_cost, sim_cost]
plt.figure(figsize=(8, 5))
bars = plt.bar(scenarios, costs, color=["gray", "green", "orange"])
plt.title("Comparaison des Scénarios de Coûts")
plt.ylabel("Coût Total Moyen (MAD)")
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + 5, f"{yval:.0f}", ha="center")
plt.savefig("scenarios_costs.png")
plt.show()