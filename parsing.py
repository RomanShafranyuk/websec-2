import requests
a = requests.get("https://tosamara.ru/api/v2/classifiers/stopsFullDB.xml")
with open("data.xml", "wb") as f:
    f.write(a.content)    
import xml.etree.ElementTree as ET
tree = ET.parse('data.xml')
root = tree.getroot()
print(root[0][1].text)