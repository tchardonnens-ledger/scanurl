import socket
from ipwhois import IPWhois
import csv
import requests
import urllib

def analyse_redirections(url, depth=0, max_depth=100):
    # Envoi d'une requête HTTP HEAD à l'URL spécifiée
    r = requests.head(url)

    # Vérification de la réponse HTTP
    if r.status_code != requests.codes.ok:
        print(f"Erreur HTTP {r.status_code} à la profondeur {depth}: {url}")
        return

    # Récupération de l'URL de redirection (si elle existe)
    redirect_url = r.headers.get("location")

    # Si une URL de redirection est trouvée, on l'analyse à son tour
    if redirect_url:
        # Vérification de la validité de l'URL de redirection
        try:
            r = requests.head(redirect_url)
        except requests.exceptions.MissingSchema:
            print(f"Erreur: URL de redirection non valide à la profondeur {depth}: {redirect_url}")
            return

        # Contrôle du nombre de redirections suivies
        if depth >= max_depth:
            print(f"Erreur: Trop de redirections à la profondeur {depth}: {redirect_url}")
            return

        print(f"Redirection trouvée à la profondeur {depth}: {redirect_url}")
        analyse_redirections(redirect_url, depth=depth + 1, max_depth=max_depth)
    else:
        print("Aucune redirection trouvée")