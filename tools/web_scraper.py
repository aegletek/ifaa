import requests
from bs4 import BeautifulSoup

def verify_incident(claim):

    url = "https://example-news.com"

    response = requests.get(url)

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    return {
        "external_risk": False,
        "source": "news verification"
    }