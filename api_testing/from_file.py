import requests

url = "http://127.0.0.1:5000/import-transactions"

with open('data.csv', 'rb') as file:
    response = requests.post(url, files={'file': file})

print("Response:", response.text)