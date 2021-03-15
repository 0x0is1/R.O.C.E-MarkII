import requests
while True:
    try:
        requests.get("https://profile-counter.glitch.me/0x0is1/count.svg")
    except:
         print("error")
         continue
