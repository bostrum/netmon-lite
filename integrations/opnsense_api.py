import requests
import json

def get(ipv4, api, secret):
    url = "https://{0}/api/diagnostics/interface/getArp".format(ipv4)
    r = requests.get(
        url, verify = False,
        auth = (api,secret),
        timeout=10
    )
    return json.loads(r.text)