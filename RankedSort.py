import apiKey
from riotwatcher import RiotWatcher


watcher = RiotWatcher(apiKey.key)
region = "EUW1"
file = open("MatchData.txt", "r")
MatchData = eval(file.read())
rankedMatches = []


for key, totalRecentMatches in MatchData.items():
    for match in totalRecentMatches["matches"]:
        if match["queue"] == 420:
            rankedMatches.append(match)

print("Total Ranked Matches: " + str(len(rankedMatches)))

for game in rankedMatches:
    timeline = watcher.match.timeline_by_match(region=region, match_id=game["gameId"])
    print(timeline)

ffgames = []
n = 0
m = 0
for match in rankedMatches:
    gameLength = watcher.match.by_id(region=region, match_id=match["gameId"])["gameDuration"]
    if 900 <= gameLength <= 1200:
        n += 1
        seconds = gameLength%60
        if seconds < 10:
            secondsstring = "0" + str(seconds)
        else:
            secondsstring = str(seconds)
        ffgames.append(match["gameId"])
        print("Game " + str(match["gameId"]) + " was surrendered at " + str(int((gameLength/60)))+ ":" + secondsstring)
    else:
        n +=1
    print("Done " + str(n) + "/" + str(len(rankedMatches)))

print(ffgames)




