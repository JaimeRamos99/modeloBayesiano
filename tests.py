import requests
import random
r = requests.get("https://api-rest-botic.herokuapp.com/api/messages")
print(r.json())
hola = [0]
for i in r.json():
    if i["_id"] == "5db7bf2906fd9800178f7230":
        print(i)
print(random.randint(0, len(hola) - 1))
