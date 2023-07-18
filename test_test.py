import requests
import pandas as pd
import json

base_url = 'http://localhost:5000'
fetchCelebUrl = f"{base_url}/fetchAllArtists"

res = requests.get(fetchCelebUrl)
celeb_data = res.json()

print(celeb_data)

updateCelebUrl = f"{base_url}/updateCelebrity/1/50"
response = requests.put(updateCelebUrl)
print(response.text)
