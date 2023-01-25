import socket
from ipwhois import IPWhois
import requests
import tldextract


def get_ip(url):
    extracted_domain = tldextract.extract(url)
    domain = extracted_domain.domain + '.' + extracted_domain.suffix
    ip_address = socket.gethostbyname(domain)
    return ip_address


def get_reverse_dns(ip_address):
    reverse_dns = socket.gethostbyaddr(ip_address)
    return reverse_dns


def get_whois(ip_address):
    ipwhois = IPWhois(ip_address)
    whois = ipwhois.lookup_rdap()
    return whois


def analyse_redirections(url, depth=0, max_depth=100):
    r = requests.head(url)

    if r.status_code != requests.codes.ok:
        print(f"Erreur HTTP {r.status_code} à la profondeur {depth}: {url}")
        return

    redirect_url = r.headers.get("location")

    if redirect_url:
        try:
            r = requests.head(redirect_url)
        except requests.exceptions.MissingSchema:
            print(f"Erreur: URL de redirection non valide à la profondeur {depth}: {redirect_url}")
            return

        if depth >= max_depth:
            print(f"Erreur: Trop de redirections à la profondeur {depth}: {redirect_url}")
            return

        print(f"Redirection trouvée à la profondeur {depth}: {redirect_url}")
        analyse_redirections(redirect_url, depth=depth + 1, max_depth=max_depth)
    else:
        print("Aucune redirection trouvée")
