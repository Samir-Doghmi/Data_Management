import requests
import json

dataset = {}

with open('dataAnimeUnity.json', 'r') as infile:
    dataset = json.load(infile)

result = []
for i in range(0,3833, 30):
    url = 'https://www.animeunity.tv/archivio/get-animes'
    headers = {
        "authority": "www.animeunity.tv",
        "Connection": "keep-alive",
        "Content-Length": "129",
        "Origin": "https://www.animeunity.tv",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        "Content-Type": "application/json",
        "Accept": "*/*",
        "x-csrf-token": "6USoRVqvLgl9qRqkxr2rmlvzuMvRiCXZZF9G7Ocp",
        "Referer": "https://www.animeunity.tv/archivio",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "fr-FR,fr;q=0.8,en-US;q=0.6,en;q=0.4",
        "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.3",
        "Cookie": "__cf_bm=mbyEidn5X0K58OXDgomxtGNGxGVmzHRz.7QBHtfznDg-1670620626-0-AWV77OItQ7E6NInXM7V457f9TBk/O5Ik37IJnGryZheRC4OdDV8HT+hYQBuZH3kdqAXyZMHEsEBp6AePW/eVp9o7Pu6M0EMWtOYOedJJBCQZvqDVffpfHYutfpUDutis7IJy0kfJFNvgGhYMgbSMQWk=; visuals=[45660]; XSRF-TOKEN=eyJpdiI6IjJZREtqZlg1UWJcL1J2cTVtWkw4bFhRPT0iLCJ2YWx1ZSI6Im9rZUhadG9QOGZxdUc5STdaMThwb0N2WWNJeGtRSDJveDdCVUpYYll3eVpZMFhMbDlQQWFhOElmV0U1bEpxUkciLCJtYWMiOiIxNDIzNzMwMDc3YzA0ZDdjZDIyY2FjYzA5ZDUzYTk5OWZkNjYxYTFlYWYwYWQyNzhlY2JmMWZkNjJlMjU4ZjFiIn0%3D; animeunity_session=eyJpdiI6IlNvYzMwT2RkSHRoYzB6WHNYNEJ3OUE9PSIsInZhbHVlIjoiK1wvWkRYWkVaTExlZVRBY2JZSlNUZ0xPWTVSYW5tKzd1YTBCM1EzRUJ3RndWK2tLMkI5V1p5XC9waUpFYXhObUVSIiwibWFjIjoiMjRiNWJhZWExMzYxZDgxYTI3NDY4NDU1Yjc0MDNhNTkyMmRiMzRlMDAxMGI2ZWU5M2Y0YzY4ZDViMWQxODRjNiJ9"
    }
    payload = {
    "offset": str(i)
    }
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    
    resp_Json = r.json()

    result.extend(resp_Json["records"])
    print(resp_Json["records"])

    
    
dataset["records"] = result

jsonFile = open("dataAnimeUnity.json", "w")
jsonFile.write(json.dumps(dataset))
jsonFile.close()


    

