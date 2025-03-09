# This current file is responsible for managing the data of the game,
# such as the version, the score table, and the functions to add and arrange the scores.
import json

def getVersion():
    with open("assets/data/data.json", mode="r", encoding="utf-8") as file:
        stats = json.load(file)
    return stats["version"]

def unboxData():
    with open("assets/data/data.json", mode="r", encoding="utf-8") as file: stats = json.load(file)
    return [list(stats["scoreTable"][i].values()) for i in range(len(stats["scoreTable"]))]

def add(arr):
    with open("assets/data/data.json", mode="r", encoding="utf-8") as file:
        stats = json.load(file)

    stats["scoreTable"].append({
        "name": arr[0],
        "difficulty": arr[1],
        "time": arr[2],
        "errors": arr[3],
        "points": arr[4]
    })

    with open("assets/data/data.json", mode="w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4, ensure_ascii=False)

def arrange():
    _stats = unboxData()

    # Sort the stats by score
    _stats.sort(key=lambda x: x[4], reverse=True)

    with open("assets/data/data.json", mode="r", encoding="utf-8") as file: stats = json.load(file)
    # Update the original stats with the sorted data
    for i, entry in enumerate(_stats):
        if i < 10:
            stats["scoreTable"][i] = {
                "name": entry[0],
                "difficulty": entry[1],
                "time": entry[2],
                "errors": entry[3],
                "points": entry[4]
            }
        else:
            stats["scoreTable"].pop()

    # Write the updated stats back to the JSON file
    with open("assets/data/data.json", mode="w", encoding="utf-8") as file:
        json.dump(stats, file, indent=4, ensure_ascii=False)