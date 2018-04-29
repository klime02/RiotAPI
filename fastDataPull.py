import multiprocessing as mp
import apiKey
from riotwatcher import RiotWatcher
import logging

watcher = RiotWatcher(apiKey.key)
logging.basicConfig(filename='myapp.log', level=logging.INFO)


def getLeaguePlayerIds(name, region):
    playerList = []
    leagueId = watcher.league.positions_by_summoner(region=region, summoner_id=watcher.summoner.by_name(region, name)["id"])[0]["leagueId"]
    for player in watcher.league.by_id(region, leagueId)["entries"]:
        playerList.append(player["playerOrTeamName"])
    print("Got Player List")
    return playerList


def splitList(playerlist):
    bunchnumber = int(len(playerlist)/4)
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    count = 0
    for player in playerlist:
        count +=1
        if 1 <= count <= bunchnumber:
            list1.append(player)
        elif bunchnumber < count <= (2*bunchnumber):
            list2.append(player)
        elif (2*bunchnumber) < count <= (3*bunchnumber):
            list3.append(player)
        else:
            list4.append(player)
    seperatedPlayers = {}
    listofLists = [list1, list2, list3, list4]
    lcount = 0
    for x in listofLists:
        lcount += 1
        seperatedPlayers[lcount] = x
    return seperatedPlayers


def getRecentMatches(playerlist, region):
    recentmatches = {}
    for name in playerlist:
        print("Done " + name)
        accId = watcher.summoner.by_name(region=region, summoner_name=name)["accountId"]
        matchlist = watcher.match.matchlist_by_account_recent(region=region, account_id=accId)
        recentmatches[accId] = matchlist
    return recentmatches


if __name__ == '__main__':
    seedName = input("Seed Name: ")
    region = input("Region: ")
    playerlist = getLeaguePlayerIds(seedName, region)
    seperatedPlayers = splitList(playerlist)
    pool = mp.Pool(processes=4)
    results = [pool.apply_async(getRecentMatches, args=(seplist, region)) for keys, seplist in seperatedPlayers.items()]
    output = [p.get() for p in results]
    finalCombinedData = {}
    data = open(("Matches" + seedName + region + ".txt"), "w")
    for subpart in output:
        for key, value in subpart.items():
            finalCombinedData[key] = value
    data.write(str(finalCombinedData))
    data.close()



