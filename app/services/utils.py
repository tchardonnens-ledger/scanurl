import socket
from ipwhois import IPWhois
import requests
import tldextract
import tld


def _is_url(input_string):
    try:
        tld.get_tld(input_string, as_object=True)
        return True
    except tld.exceptions.TldBadUrl:
        return False


def _get_domain(url):
    first_level_domain = tld.get_fld(url)
    print(url, first_level_domain)
    return first_level_domain


def _get_url_from_domain(domain):
    return "https://"+domain


def get_ip(input):
    if _is_url(input):
        ip_address = socket.gethostbyname(_get_domain(input))
    else:
        ip_address = socket.gethostbyname(input)
    return ip_address


def get_reverse_dns(ip_address):
    reverse_dns = socket.gethostbyaddr(ip_address)
    return reverse_dns


def get_whois(ip_address):
    ipwhois = IPWhois(ip_address)
    whois = ipwhois.lookup_rdap()
    return whois


def analyse_redirections(input, depth=0, max_depth=100):
    url = ""
    if _is_url(input):
        url = input
    else:
        domain = input
        url = _get_url_from_domain(domain)
    r = requests.head(url)

    if r.status_code != requests.codes.ok:
        return f"HTTP error {r.status_code} at depth {depth} for {url}"

    redirect_url = r.headers.get("location")

    if redirect_url:
        try:
            if depth >= max_depth:
                return f"Too many redirections {depth}: {redirect_url}"

        except requests.exceptions.MissingSchema:
            return f"Redirection for URL {redirect_url} not valid at depth {depth}"

        analyse_redirections(redirect_url, depth=depth + 1, max_depth=max_depth)
        return f"URL Redirection {redirect_url} found at depth {depth}"
    else:
        return f"No redirection found from {redirect_url}"
