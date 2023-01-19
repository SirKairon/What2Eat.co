# Author: Dhruv Kairon

# Imports
import requests
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template
from operator import itemgetter

# Load environment variables
load_dotenv("/Users/dhruvkairon/apidata.env")

BASE_URL = "https://api.edamam.com/api/recipes/v2"
aid = os.environ.get("apiID")
akey = os.environ.get("apiKey")


def getMatchingMeals(igdt: str) -> dict:
    link = BASE_URL + "?type=public"
    fields = ["uri", "label", "image", "url", "ingredientLines", "calories", "cuisineType", "dishType", "mealType", "healthLabels", "cautions"]
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
    n = 1
    for meal in meals:
        string += f"{n}. {meal['label']} | No. of Ingredients: {meal['countIngds']} | Link to the Website: {meal['url']} | Calories: {meal['calories']} | Cuisine Type: {meal['cuisineType']} | Dish Type: {meal['dishType']} | Meal Type: {meal['mealType']} | Cautions: {meal['cautions']}"
        n += 1
    return string


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

def terminal():
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

@app.route('/results.html', methods=['GET'])
def handle_form_submission():
    # Get the form data from the request
    ingredients = request.values.get("ingredients")

    # Process the form data here
    results = getMatchingMeals(ingredients)["hits"]
    if not results:
        return "No results loaded!"
    else:
        results = sortResults(results)
        return render_template("results.html", image1 = results[0]["image"], image2 = results[1]["image"], image3 = results[2]["image"], image4 = results[3]["image"], image5 = results[4]["image"], image6 = results[5]["image"], image7 = results[6]["image"], image8 = results[7]["image"], label1 = results[0]["label"], label2 = results[1]["label"], label3 = results[2]["label"], label4 = results[3]["label"], label5 = results[4]["label"], label6 = results[5]["label"], label7 = results[6]["label"], label8 = results[7]["label"], ingdlist1 = formatIngd(results[0]["ingredientLines"]).split("\n"), ingdlist2 = formatIngd(results[1]["ingredientLines"]).split("\n"), ingdlist3 = formatIngd(results[2]["ingredientLines"]).split("\n"), ingdlist4 = formatIngd(results[3]["ingredientLines"]).split("\n"), ingdlist5 = formatIngd(results[4]["ingredientLines"]).split("\n"), ingdlist6 = formatIngd(results[5]["ingredientLines"]).split("\n"), ingdlist7 = formatIngd(results[6]["ingredientLines"]).split("\n"), ingdlist8 = formatIngd(results[7]["ingredientLines"]).split("\n"), url1 = results[0]["url"], url2 = results[1]["url"], url3 = results[2]["url"], url4 = results[3]["url"], url5 = results[4]["url"], url6 = results[5]["url"], url7 = results[6]["url"], url8 = results[7]["url"])

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)