import pandas as pd

# 1. Importer les données avec gestion explicite de l'encodage
try:
    df_ventes = pd.read_csv("Données_Brutes/historique_ventes.csv", sep=",", encoding="utf-8")
except UnicodeDecodeError:
    print("Problème d'encodage détecté dans historique_ventes.csv. Tentative avec un autre encodage...")
    df_ventes = pd.read_csv("Données_Brutes/historique_ventes.csv", sep=",", encoding="latin-1")  # Alternative si UTF-8 échoue

df_stock = pd.read_excel("Données_Brutes/stock_actuel.xlsx")  # Excel gère généralement bien UTF-8

# Vérifier les premières lignes pour voir les caractères
print("Aperçu des ventes avant nettoyage :")
print(df_ventes.head())
print("Aperçu du stock avant nettoyage :")
print(df_stock.head())

# Afficher les noms des colonnes pour vérification
print("Colonnes dans df_ventes :", df_ventes.columns.tolist())

# 2. Nettoyer les données
# a. Vérifier les valeurs manquantes
print("Valeurs manquantes dans les ventes :")
print(df_ventes.isnull().sum())

print("Valeurs manquantes dans le stock :")
print(df_stock.isnull().sum())

# b. Supprimer les lignes avec des dates manquantes
df_ventes.dropna(subset=["Date de commande"], inplace=True)

# c. Convertir les dates en format datetime
df_ventes["Date de commande"] = pd.to_datetime(df_ventes["Date de commande"], format="%d/%m/%Y")

# d. Ajouter une colonne "mois" pour faciliter l'analyse
df_ventes["mois"] = df_ventes["Date de commande"].dt.to_period("M")

# 3. Exporter les données nettoyées avec encodage UTF-8 et BOM pour compatibilité Excel
df_ventes.to_csv("Données_Nettoyées/ventes_nettoye.csv", index=False, encoding="utf-8-sig")
df_stock.to_csv("Données_Nettoyées/stock_nettoye.csv", index=False, encoding="utf-8-sig")

print("Données nettoyées exportées avec succès dans 'Données_Nettoyées/' !")
print("Vérifiez les fichiers avec un éditeur de texte ou Excel pour confirmer l'affichage des 'é'.")