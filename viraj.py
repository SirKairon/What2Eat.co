"""import requests
from operator import itemgetter

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("hacked-2023-ad41e-firebase-adminsdk-lc0yj-acfa8af233.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://hacked-2023-ad41e-default-rtdb.firebaseio.com"
})
"""

import requests
from flask import Flask, request, render_template, jsonify
from operator import itemgetter

BASE_URL = "https://api.edamam.com/api/recipes/v2"
aid = "fddb9486"
akey = "f8f8204240d43464a98e520c2a40be62"



def getMatchingMeals(igdt: str) -> dict:
    link = BASE_URL + "?type=public"
    fields = ["uri", "label", "url", "ingredientLines", "calories"]
    q = {"q" : igdt, "app_id" : aid, "app_key" : akey, "field" : fields}
    actual = requests.get(link, params = q)

    if actual.status_code != 200:
        return None
    else:
        return actual.json()

def sortResults(results: dict) -> list:
    meals = []
    for i in range(len(results)):
        meals.append([])
        meals[i] = results[i]["recipe"]
        meals[i]["countIngds"] = len(meals[i]["ingredientLines"])
    meals = sorted(meals, key = itemgetter("countIngds"))
    return meals

def displayMeals(meals: list) -> None:
    string=""
    big=[]
    for meal in meals:
        #print(f"{n}. {meal['label']} | No. of Ingredients: {meal['countIngds']}")
        # string += f"{meal['label']} | No. of Ingredients: {meal['countIngds']}"
        big.append(meal)
    return big

    # return string

def getMeal(mealURI: str) -> dict:
    link = BASE_URL + "/" + mealURI + "?type=public"
    q = {"type" : "public", "app_id" : aid, "app_key" : akey}
    actual = requests.get(link, params = q)

    if actual.status_code != 200:
        return None
    else:
        return actual.json()

def formatMeal(meal: dict) -> None:
    mealName = meal['label']
    mealCat = meal['cuisineType'][0].capitalize()
    mealIngd = meal['ingredientLines']
    print("Name:", mealName)
    print("Category:", mealCat)
    print("Ingredients:\n" + formatIngd(mealIngd))

def formatIngd(inst: list) -> str:
    n = 1
    actInst = ""
    for line in inst:
        actInst += "%s. %s %s" % (n, line, "\n")
        n += 1
    return actInst

def main():
    ingredient = input("Provide ingredient(s): ")
    print()
    results = getMatchingMeals(ingredient)["hits"]
    if not results:
        print("No results loaded!")
    else:
        results = sortResults(results)
        print("Here are the results:")
        displayMeals(results)
        print()

        ch = int(input("Select a recipe: "))
        print() 

        uri = results[ch-1]["uri"]
        pos = uri.find("_")
        uri = uri[pos+1:]
        meal = getMeal(uri)["recipe"]
        formatMeal(meal)

# Flask app

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/submit', methods=['GET'])
def handle_form_submission():
    # Get the form data from the request
    ingredients = request.values.get("ingredients") 

    # Process the form data here
    results = getMatchingMeals(ingredients)["hits"]
    if not results:
        return "No results loaded!"
    else:
        results = sortResults(results)
        return jsonify(displayMeals(results))

if __name__ == '__main__':
    app.run()
    # app.run(host='2620:101:c040:85c:5db1:7e0b:dcb3:f4f')
    # app.run(host='0.0.0.0')
