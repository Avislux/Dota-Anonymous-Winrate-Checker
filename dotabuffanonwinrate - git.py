
import json
import requests
import pprint
key = 'redacted' #steam webapi key.
accountIDurl = 0 #Dota account ID if desired. datatype: int
numberOfGames = 10
gameHistoryURL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?account_id=' + str(accountIDurl) + '&matches_requested=' + str(numberOfGames) + '&key=' + str(key)
gameHistory = requests.get(gameHistoryURL)

with open("hero id.txt") as  data_file:
    heroIDdata = json.load(data_file)
gameHistoryData = json.loads(gameHistory.text)
trueCount = 0
falseCount = 0
evenCount = 0
for x in range(0,numberOfGames):
    print("Match ID:" + str(gameHistoryData["result"]["matches"][x]["match_id"]))
    matchdetailsURL = 'https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?account_id='+ str(accountIDurl) +'&match_id=' + str(gameHistoryData["result"]["matches"][x]["match_id"]) +'&key=' + str(key)
    matchpage = requests.get(matchdetailsURL)
    matchDetails = json.loads(matchpage.text)
    radiantNotAnon = 0
    direNotAnon = 0
    numberOfPlayers = len(matchDetails["result"]["players"])
    for y in range(0,numberOfPlayers): #number of players
        '''
        if y == 0:
            print("Radiant:")
        if y == 5:
            print ("Dire:")
            '''
        if y < 5:
            try:
                print (matchDetails["result"]["players"][y]["account_id"])
                accountID = matchDetails["result"]["players"][y]["account_id"]
            except KeyError:
                print("None")
            
            if accountID != 4294967295:
                radiantNotAnon = radiantNotAnon + 1
        else:
            try:
                print (matchDetails["result"]["players"][y]["account_id"])
                accountID = matchDetails["result"]["players"][y]["account_id"]
            except KeyError:
                print("None")
            if accountID != 4294967295:
                direNotAnon = direNotAnon + 1
        if accountID == accountIDurl: 
            for z in range( 0, 111):
                if heroIDdata["heroes"][z]["id"] == matchDetails["result"]["players"][y]["hero_id"] :
                    print( "\t\t\t", heroIDdata["heroes"][z]["localized_name"])
    if (str(matchDetails["result"]["radiant_win"] == True)):
        print ("Radiant Victory" + " \tNonAnons on Radiant: " + str(radiantNotAnon) + " NonAnons on Dire: " + str(direNotAnon))
    else:
        print ("Dire Victory" + " \tNonAnons on Radiant: " + str(radiantNotAnon) + " NonAnons on Dire: " + str(direNotAnon))
    if matchDetails["result"]["human_players"] != 10:
        print("Not counted")
    elif (matchDetails["result"]["radiant_win"] == True) and (radiantNotAnon > direNotAnon): #If radiant won and there are fewer anons on that team
        trueCount = trueCount + 1
    elif (matchDetails["result"]["radiant_win"] == False) and (radiantNotAnon < direNotAnon): #If dire won and there are fewer anons on that team
        trueCount = trueCount + 1
    elif radiantNotAnon == direNotAnon:
        evenCount = evenCount + 1
    else:
        falseCount = falseCount + 1
print("\nAre teams with fewer 'stats hidden' players more likely to win?")
print('Yes: ', str(trueCount), 'No: ', str(falseCount), 'Even: ', str(evenCount))

print("done")

