import requests
import xmltodict
import json


def getCollection(username):
    print("Getting User's Collection...")
    collection = {}
    rawCollection = requests.get("https://boardgamegeek.com/xmlapi2/collection?username=" + username + "&version=0&own=1&excludesubtype=boardgameexpansion")
    collectionDict = xmltodict.parse(rawCollection.text)
    #print(collectionDict)
    for game in collectionDict["items"]["item"]:
        gameDict = {}
        gameDict["id"] = game['@objectid']
        gameDict["image"] = game["image"]
        gameDict["name"] = game["name"]["#text"]
        gameDict["recScore"] = 0
        collection[game['@objectid']] = gameDict
    return collection

def getRelatedGames(game):
    gameID = game["id"]
    rawRecs = requests.get("https://api.geekdo.com/api/geekitem/recs?ajax=1&objecttype=thing&objectid=" + str(gameID))
    recs = json.loads(rawRecs.text)
    items = []
    for rec in recs["recs"]:
        item = {}
        item["name"] = rec["item"]["name"]
        item["id"] = rec["item"]["id"]
        items.append(item)
    return items



userCollection = getCollection("snaxib")

for game in userCollection:
    #print("Getting Related Games for " + userCollection[game]["name"] + "...")
    recs = getRelatedGames(userCollection[game])
    userCollection[game]["related"] = (recs)
    for rec in userCollection[game]["related"]:
        if rec["id"] in userCollection:
            userCollection[rec["id"]]["recScore"] += 1

for game in userCollection:
    print(userCollection[game]["name"] + "," + str(userCollection[game]["recScore"]))
