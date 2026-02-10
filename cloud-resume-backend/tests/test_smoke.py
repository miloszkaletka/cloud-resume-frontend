import os
import requests

FRONTDOOR_URL = "https://cloud-resume-a8c3h4c4esacbmec.z01.azurefd.net"
API_URL = "https://fn-cloud-resume-counter-cacwd0eaf8hrfvcr.westeurope-01.azurewebsites.net/api/counter"

def test_frontend_is_up():
    r = requests.get(FRONTDOOR_URL, timeout=15)
    assert r.status_code == 200
    # prosta kontrola, że to Twoja strona (dopasuj tekst, który masz w HTML)
    assert "Visitor count" in r.text


def test_api_counter_returns_json():
    r = requests.get(API_URL, timeout=15)
    assert r.status_code == 200
    data = r.json()
    assert "count" in data
    assert isinstance(data["count"], int)
