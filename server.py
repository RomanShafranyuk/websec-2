from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import requests
correct_values = [0,1,2,3, 11,12,13,14,15,16,17,18,19]
app = Flask(__name__)
@app.route("/prediction")
def prediction():
    return render_template("prediction.html")
@app.route("/")
def main():
    stops_info = []
    search_text = request.args.getlist("busStop")
    if len(search_text) == 0:
        return render_template("index.html")
    else:
        a = requests.get("https://tosamara.ru/api/v2/classifiers/stopsFullDB.xml")
        with open("data.xml", "wb") as f:
            f.write(a.content)    
        tree = ET.parse('data.xml')
        root = tree.getroot()
        for i in root:
            if i[1].text.find(search_text[0]) >= 0:
                tmp = ""
                for j in range(0,19):
                    if j in correct_values and i[j].text != None and j>=1 and j <=3:
                        tmp += " " + i[j].text 
                stops_info.append(tmp)
                        #print(f"{i[j].tag}: {i[j].text}")
        print(stops_info)
        #return render_template("index.html")
        return render_template("stops.html", stops=stops_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
