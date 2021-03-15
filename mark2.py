import requests
while True:
    try:
        r=requests.get("https://profile-counter.glitch.me/0x0is1/count.svg")
        print(r.status_code)
    except:
         print("error")
         continue
