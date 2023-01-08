import requests
from operator import itemgetter
BASE_URL = "https://api.edamam.com/api/recipes/v2"
aid = "62bf7e15"
akey = "78e58e130038ec1044ca0a63accb938a"

def getMatchingMeals(igdt: str) -> dict:
    link = BASE_URL + "?type=public"
    fields = ["uri", "label", "image", "ingredientLines", "calories"]
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
    n = 1
    for meal in meals:
        print(f"{n}. {meal['label']} | No. of Ingredients: {meal['countIngds']} | Calories: {int(meal['calories'])}")
        n += 1

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

if __name__ == '__main__':
    main()