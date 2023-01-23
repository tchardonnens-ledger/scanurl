import socket
from ipwhois import IPWhois
import requests
import urllib
import tldextract
from utils import analyse_redirections


async def osint(url: str):
    # Demande à l'utilisateur de saisir une URL
    url = url
    # Récupère l'adresse IP de l'URL en utilisant le module "socket"
    extracted_domain = tldextract.extract(url)

    # Concatenate the subdomain and domain parts
    domain = extracted_domain.subdomain + '.' + extracted_domain.domain + '.' + extracted_domain.suffix
    print(domain)
    ip_address = socket.gethostbyname(domain)

    # Réalise un reverse DNS en utilisant le module "socket"
    reverse_dns = socket.gethostbyaddr(ip_address)

    # Réalise un whois en utilisant le module "ipwhois"
    ipwhois = IPWhois(ip_address)
    whois = ipwhois.lookup_rdap()

    redirections = analyse_redirections(url)

    return url, reverse_dns, whois, redirections
