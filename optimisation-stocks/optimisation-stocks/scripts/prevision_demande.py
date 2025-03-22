import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import xgboost as xgb

# Définir le répertoire de travail
base_path = "C:/Users/Lenovo/Desktop/Projet_Gestion_Stock"
os.chdir(base_path)
print("Répertoire de travail actuel :", os.getcwd())

# Créer un dossier pour les résultats s'il n'existe pas
if not os.path.exists("Figures"):
    os.makedirs("Figures")

# 1. Charger les données nettoyées
df_ventes = pd.read_csv("Données_Nettoyées/ventes_nettoye.csv", encoding="utf-8-sig")

# 2. Préparer les données : Agréger les ventes par mois
df_ventes["Date de commande"] = pd.to_datetime(df_ventes["Date de commande"])
ventes_par_mois = df_ventes.groupby(df_ventes["Date de commande"].dt.to_period("M"))["Quantité vendue"].sum().reset_index()
ventes_par_mois.columns = ["Mois", "Quantité vendue"]
ventes_par_mois["Mois"] = ventes_par_mois["Mois"].dt.to_timestamp()

# Ajouter une variable temporelle numérique pour la régression
ventes_par_mois["Mois_num"] = np.arange(len(ventes_par_mois))

# 3. Séparer les données en jeu d’entraînement (80%) et de test (20%)
X = ventes_par_mois[["Mois_num"]]  # Variable explicative (temps)
y = ventes_par_mois["Quantité vendue"]  # Variable cible
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 4. Modélisation et prévision
# a. Random Forest
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
print(f"RMSE Random Forest : {rf_rmse:.2f}")

# b. XGBoost
xgb_model = xgb.XGBRegressor(objective="reg:squarederror", n_estimators=100, random_state=42)
xgb_model.fit(X_train, y_train)
xgb_pred = xgb_model.predict(X_test)
xgb_rmse = np.sqrt(mean_squared_error(y_test, xgb_pred))
print(f"RMSE XGBoost : {xgb_rmse:.2f}")

# 5. Visualisation avec un graphique en barres
# Préparer les données pour le graphique
mois_test = ventes_par_mois["Mois"].iloc[-len(y_test):].reset_index(drop=True)
data_plot = pd.DataFrame({
    "Mois": mois_test,
    "Données réelles": y_test.values,
    "Random Forest": rf_pred,
    "XGBoost": xgb_pred
})

# Créer le graphique en barres
plt.figure(figsize=(12, 6))
bar_width = 0.25
index = np.arange(len(data_plot))

plt.bar(index, data_plot["Données réelles"], bar_width, label="Données réelles", color="blue")
plt.bar(index + bar_width, data_plot["Random Forest"], bar_width, label="Random Forest", color="green")
plt.bar(index + 2 * bar_width, data_plot["XGBoost"], bar_width, label="XGBoost", color="red")

plt.xlabel("Mois")
plt.ylabel("Quantité vendue")
plt.title("Comparaison des prévisions et des données réelles")
plt.xticks(index + bar_width, data_plot["Mois"].dt.strftime("%Y-%m"), rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig("Figures/previsions_demande_barres.png")
plt.show()

# 6. Prévision pour le mois suivant (Mars 2025)
next_mois_num = np.array([[len(ventes_par_mois)]])
print(f"Prévision pour le mois suivant (Mars 2025) :")
print(f"- Random Forest : {rf_model.predict(next_mois_num)[0]:.2f}")
print(f"- XGBoost : {xgb_model.predict(next_mois_num)[0]:.2f}")