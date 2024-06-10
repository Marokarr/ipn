import requests

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        return response.json()['ip']
    except requests.RequestException:
        return "Could not retrieve public IP"
