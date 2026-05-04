import requests

url = "https://parseapi.back4app.com/classes/YourClass"
headers = {
    "X-Parse-Application-Id": "YOUR_APP_ID",
    "X-Parse-REST-API-Key": "YOUR_API_KEY"
}

response = requests.get(url, headers=headers)
print(response.json())
