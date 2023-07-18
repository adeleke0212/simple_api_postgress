import pandas as pd
import requests


base_url = 'http://localhost:5000'
fetch_home_URL = f"{base_url}/fetchHome"

response = requests.get(fetch_home_URL)
artists_data = response.json()

print(artists_data)


fetch_home_select = f"{base_url}/fetchHome/select"

response = requests.get(fetch_home_select)
print(response.status_code)
fetch_select_data = response.json()
print(fetch_select_data)

load_json_url = f"{base_url}/loadJsonFile"
response = requests.get(load_json_url)
celeb_data = response.json()
print(celeb_data)


fetch_home_id_url = f"{base_url}/fetchHome/20"
response = requests.get(fetch_home_id_url)
id_data = response.json()
# print(id_data)

post_celeb_url = f"{base_url}/postCelebrity"
resp = requests.post(post_celeb_url)
data = resp.text
print(data)

updateCelebUrl = f"{base_url}/updateCelebrity/1/50"
response = requests.put(updateCelebUrl)
print(response.text)
