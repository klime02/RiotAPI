import apiKey
from riotwatcher import RiotWatcher

watcher = RiotWatcher(apiKey.key)

initialPlayerName = "Klime"
euw = "EUW1"

fullPlayerList = []
fullMatchId = {}
for player in watcher.league.by_id(euw, watcher.league.positions_by_summoner(euw, summoner_id=watcher.summoner.by_name(euw, initialPlayerName)["id"])[0]["leagueId"])["entries"]:
    fullPlayerList.append(player["playerOrTeamName"])

n = 0

print("Total players in League: " + str(len(fullPlayerList)))

for player in fullPlayerList:
    tempId = watcher.summoner.by_name(euw, player)["accountId"]
    tempList = watcher.match.matchlist_by_account_recent(euw, account_id=tempId)
    fullMatchId[tempId] = tempList
    n +=1
    print("Done player " + str(n))
print(fullMatchId)