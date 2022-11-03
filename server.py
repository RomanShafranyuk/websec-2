from flask import Flask, render_template, request
import xml.etree.ElementTree as ET
import requests
import hashlib
app = Flask(__name__)
@app.route("/route")
def route():
    HULLNO = request.args.getlist("transportId")
    first = ET.Element('request')
    method = ET.SubElement(first, 'method')
    parameters = ET.SubElement(first, 'parameters')
    hullno = ET.SubElement(parameters, 'HULLNO')
    method.text = 'getTransportPosition'
    hullno.text = HULLNO[0]
    hash_object = hashlib.sha1(ET.tostring(
        first, encoding="utf-8") + bytes("just_f0r_tests", encoding="utf-8")).hexdigest()
    data = {"message": ET.tostring(first, encoding="utf-8"),
            "os": "web",
            "clientId": "test",
            "authKey": hash_object

            }
    route = requests.post("http://tosamara.ru/api/v2/xml", data=data)
    content = route.content.decode()
    root_route = ET.fromstring(content)
    route_list = []
    route_id = root_route[0].text
    r = requests.get("http://tosamara.ru/api/v2/classifiers/routes.xml")
    with open("routes.xml", "wb") as f:
        f.write(r.content)
    tree = ET.parse('routes.xml')
    root_r = tree.getroot()
    for i in root_r:
        if route_id == i[0].text:
            route_id = i[1].text + "  " +  i[6].text
    
    
    for i in root_route:
        for j in i:
            result= {"stop_id":j[0].text, "time":str(round(float(j[1].text)/60))}
            route_list.append(result)
    tree = ET.parse('data.xml')
    root_stops = tree.getroot()
    for i in route_list:
        for j in root_stops:
            if i["stop_id"] == j[0].text:
                i["stop_id"] = j[1].text
    print(route_list)    

    return render_template("route.html", route_id=route_id, route_list=route_list)
    

@app.route("/prediction")
def prediction():
    KS_ID = request.args.getlist("stopId")
    print(KS_ID[0])
    COUNT = 20
    first = ET.Element('request')
    method = ET.SubElement(first, 'method')
    parameters = ET.SubElement(first, 'parameters')
    stop_id = ET.SubElement(parameters, 'KS_ID')
    count = ET.SubElement(parameters, 'COUNT')
    method.text = 'getFirstArrivalToStop'
    stop_id.text = KS_ID[0]
    count.text = str(COUNT)
    hash_object = hashlib.sha1(ET.tostring(
        first, encoding="utf-8") + bytes("just_f0r_tests", encoding="utf-8")).hexdigest()
    data = {"message": ET.tostring(first, encoding="utf-8"),
            "os": "web",
            "clientId": "test",
            "authKey": hash_object
            }
    prediction = requests.post("http://tosamara.ru/api/v2/xml", data=data)
    content = prediction.content.decode()
    root = ET.fromstring(content)
    predictions = []
    for i in root:
        result = {"id_transport": i[9].text, "time": i[12].text,
                  "type": i[15].text, "number": i[6].text, "distance": i[16].text,
                  "stop": i[1].text}
        predictions.append(result)
    print(predictions)
    a = requests.get(
            "https://tosamara.ru/api/v2/classifiers/stopsFullDB.xml")
    with open("data.xml", "wb") as f:
        f.write(a.content)
    stops = ET.parse("data.xml")
    stops_root = stops.getroot()
    stop = ""
    for i in stops_root:
        if KS_ID[0] == i[0].text:
            stop = i[1].text + "\n" + i[2].text + "  " + i[3].text
    print(stop)
    return render_template("prediction.html", predictions=predictions, stop=stop)


@app.route("/")
def main():
    stops_info = []
    search_text = request.args.getlist("busStop")
    if len(search_text) == 0:
        return render_template("index.html")
    else:
        search_text[0] = search_text[0].capitalize()
        a = requests.get(
            "https://tosamara.ru/api/v2/classifiers/stopsFullDB.xml")
        with open("data.xml", "wb") as f:
            f.write(a.content)
        tree = ET.parse('data.xml')
        root = tree.getroot()
        for i in root:
            if i[1].text.find(search_text[0]) >= 0:
                tmp = {"stop_id": i[0].text, "title": i[1].text,
                       "location": i[2].text, "side": i[3].text}
                stops_info.append(tmp)
        print(stops_info)
        return render_template("stops.html", stops=stops_info)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
