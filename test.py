from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import requests
import hashlib
import os.path

if (os.path.exists("data.xml")):
    print("Да")
else:
    print("Нет")
a = requests.get("https://tosamara.ru/api/v2/classifiers")
with open("update.xml", "wb") as f:
    f.write(a.content)
tree = ET.parse('update.xml')
root = tree.getroot()
print(root[6][0].text)