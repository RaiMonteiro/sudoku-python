# This current file is responsible for managing the data of the game,
# such as the score table, and the functions to add and arrange the scores.
import json
import os

class Statistics:
    def __init__(self):
        self.cwd = os.getcwd()
        try:
            with open(os.path.join(self.cwd, "data.json"), mode="r", encoding="utf-8") as file: self.stats = json.load(file)
        except:
            with open(os.path.join(self.cwd, "data.json"), mode="w", encoding="utf-8") as file: json.dump({"scoreTable": []}, file, indent=4, ensure_ascii=False)
            with open(os.path.join(self.cwd, "data.json"), mode="r", encoding="utf-8") as file: self.stats = json.load(file)

    def add(self, arr: list):
        self.stats["scoreTable"].append({
            "name": arr[0],
            "difficulty": arr[1],
            "time": arr[2],
            "errors": arr[3],
            "points": arr[4]
        })

        self.arrange()

        # Write the updated stats back to the JSON file
        with open(os.path.join(self.cwd, "data.json"), mode="w", encoding="utf-8") as file:
            json.dump(self.stats, file, indent=4, ensure_ascii=False)

    def arrange(self):
        # Sort the stats by score
        self.stats["scoreTable"].sort(key=lambda x: x["points"], reverse=True)

        # Keep only top 10 scores
        if len(self.stats["scoreTable"]) > 10:
            self.stats["scoreTable"] = self.stats["scoreTable"][:10]

    def unBoxData(self):
        _data = []
        for d in self.stats["scoreTable"]:
            _data.append([
                d["name"],
                d["difficulty"],
                d["time"],
                d["errors"],
                d["points"]
            ])
        return _data