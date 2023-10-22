from flask import Flask, request
import requests, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def main():

    # check if lat and long are in request
    if request.args.get("city"):
        city = request.args.get("city")
    else:
        return "Error: Please provide lat and long"
    
    latlonstuff = requests.get(f"https://geocode.maps.co/search?q={city}")
    
    lat = latlonstuff.json()[0]["lat"]
    lon = latlonstuff.json()[0]["lon"]
    
    dataToReturn = []

    req = requests.get(f"https://www.google.com/maps/search/Restaurants/@{lat},{lon},10z/data=!3m1!4b1!4m4!2m3!5m1!4e1!6e5/?entry=ttu&ech=3")
    
    splittedThang = req.text.split("window.APP_INITIALIZATION_STATE=")[1].split(";window.APP_FLAGS")[0];
    
    parsed = json.loads(splittedThang)
    
    rawRestData = parsed[3][2]
    
    parsed1moretimeomg = json.loads(rawRestData.replace(")]}'",""))[0][1]
        
    for element in parsed1moretimeomg:
        if parsed1moretimeomg.index(element) == 0:
            continue
        
        address = element[14][2][0] + " " + element[14][2][1]
        stars = element[14][4][7]
        money = element[14][4][2]
        name = element[14][11]
        tags = element[14][13]
        numReviews = element[14][4][8]
        
        dataToReturn.append({"name": name, "address": address, "stars": stars, "money": money, "tags": tags, "numReviews": numReviews})
        
    

    return dataToReturn;
    

app.run()
