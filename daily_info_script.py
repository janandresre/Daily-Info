import os
import requests
import urllib.request

# os.getenv sucht im System nach einer Variable mit dem Namen 'MY_API_KEY'
WEBHOOK_URL = os.getenv('MY_DISCORD')

if WEBHOOK_URL is None:
    print("Fehler: API_KEY wurde nicht gefunden!")
else:
    print("Key erfolgreich geladen.")

lines = []
lines.append("Das ist ein Test")
lines.append("asdf")
lines.append("asdf")
message = "\n".join(lines)


payload = {
    "content": message
}

response = requests.post(WEBHOOK_URL, json=payload)

if response.status_code == 204:
    print("Nachricht erfolgreich gesendet!")
else:
    print(f"Fehler: {response.status_code} - {response.text}")
