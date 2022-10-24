import json
import hashlib
import requests
import codecs
message = {"method":"getRouteArrivalToStop", "KS_ID":9,"KR_ID":1}
hash_object = hashlib.sha1(bytes(json.dumps(message) 
+ "just_f0r_tests", encoding="utf-8")).hexdigest()

data = {"message":json.dumps(message),
        "os": "web",
        "clientId":"test",
        "authKey": hash_object }
b = requests.post("http://tosamara.ru/api/v2/json", data=data)
print(b.content.decode("utf-8"))

with open("prediction.json", "wb") as f:
            f.write(b.content) 

#clientId=test secret_key=just_f0r_tests