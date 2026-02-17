'''
    Hi, I am not familiar with OOP yet, therefore you'll have to stick with this shitty code, sorry!

    Farmbot version: 1.0.4
    Made by: Aidanman14/RiceEaten

    Thank you for using this farmbot!
'''

### Imports
import requests
import json
import time
import os

### Variables
farmBotVersion = "1.0.4"
gameBuild = "1.0.4"

scriptDir = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(scriptDir, "tokens.txt")

if not os.path.exists(path):
    with open(path, "w") as f:
        f.write("{}")

with open(path, "r+") as tokensFile:
    content = tokensFile.read().strip()
    if content:
        tokens = json.loads(content)
    else:
        quit()

def getGameInfo():
    specialHeaders = {
        'Host': 'tino.detailgames.ai',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
        'Accept-Language': 'en-GB,en;q=0.9',
        'X-Unity-Version': '2022.3.62f2',
    }

    response = requests.get('https://tino.detailgames.ai/games/1/status', headers=specialHeaders)
    responseJson = json.loads(response.text) 
    return (responseJson["status"], responseJson["version"])

# Refreshes & gets new tokens from the game's server
def getNewPlayerTokens():
    specialHeaders = {
        'Host': 'tino.detailgames.ai',
        'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
        'x-client-build': gameBuild,
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.9',
        'Authorization': 'Bearer ',
        'X-Unity-Version': '2022.3.62f2',
        'Content-Type': 'application/json',
    }

    json_data = {
        'refreshToken': tokens["refreshToken"],
    }

    response = requests.post('https://tino.detailgames.ai/auth/refresh', headers=specialHeaders, json=json_data)
    return json.loads(response.text)

# Test if the player's tokens are valid
def testPlayerTokens():
    response = requests.get('https://tino.detailgames.ai/users/me', headers=headersGet)
    if response.status_code == 400:
        return False
    return True

# Get the player's details: username, level & current stage they're on
def getPlayerDetails():
    playerData1 = json.loads(requests.get('https://tino.detailgames.ai/users/me', headers=headersGet).text)
    playerData2 = json.loads(requests.get('https://tino.detailgames.ai/tged/account', headers=headersGet).text)

    return (playerData1["nickname"], playerData2["level"], playerData2["stageSummary"]["maxStage"])

# Very bad auto farming subprogram, VERY VERY scuffed.
def farmStages(stages):
    global maxCurrentStage
    if (stages == 0):
        stages = 99999999999999 # lol
    for stage in range(maxCurrentStage, maxCurrentStage + stages):
        try:
            waves = 20

            if stage % 5 == 0:
                waves = 30

            # Start stage
            json_data = {
                'stage': stage,
                'deployedCharacters': [
                    4007,
                    4010,
                    4001,
                    4006,
                ],
            }
            response = requests.post('https://tino.detailgames.ai/tged/stages/start', headers=headersPostJson, json=json_data)

            #print(response.text)

            # Gets the session ID of the stage
            responseJson = json.loads(response.text)
            sessionId = ""
            if (not responseJson["sessionId"]):
                print("Session Id not found - You might be out of energy!")
                input("Press enter to continue.")
                return
                #quit()

            sessionId = responseJson["sessionId"]

            print(f"Started stage session ({sessionId}) for stage {stage}")

            json_data = {
                'stage': stage,
                'wave': waves,
                'clearTime': 41207,
            }

            response = requests.post(
                'https://tino.detailgames.ai/tged/leaderboard/stages/realtime-rank',
                headers=headersPostJson,
                json=json_data,
            )
            #print(response.text)

            json_data = {
                'sessionId': sessionId,
                'stage': stage,
                'wave': waves,
                'clearTime': 358886,
                'missionId': 0,
                'characterDamages': [
                    {
                        'characterId': '4010',
                        'totalDamage': '18893266',
                    },
                    {
                        'characterId': '4001',
                        'totalDamage': '22642928',
                    },
                    {
                        'characterId': '4007',
                        'totalDamage': '30343078',
                    },
                    {
                        'characterId': '4006',
                        'totalDamage': '32664713',
                    },
                ],
            }

            response = requests.post('https://tino.detailgames.ai/tged/stages/end', headers=headersPostJson, json=json_data)

            #print(response.text)

            responseJson = json.loads(response.text)

            if (not responseJson["stageSummary"]):
                print("An error occured")
                input("Press enter to continue.")
                return
                #quit()
            
            print(f"Stage {stage} completed.")
            maxCurrentStage += 1

            time.sleep(.5)
        except KeyboardInterrupt:
            print("Interrupted.")
            return
        except:
            print("Energy depleted OR unknown error.")
            return

# Very bad auto summoning subprogram
def autoSummon(times, exclusive):
    if (times == 0):
        times = 9999999999
    for i in range(1, times+1):
        try:
            json_data = {
                'count': 10,
                'isExclusive': exclusive,
            }
            response = requests.post('https://tino.detailgames.ai/tged/gacha/56000/draw', headers=headersPostJson, json=json_data)

            #print(response.text)

            if "success" in response.text:
                print(f"Summon success ({i})")
            else:
                print("Tickets depleted OR unknown error.")
                return

            time.sleep(.5)
        except KeyboardInterrupt:
            print("Interrupted.")
            return
        except:
            print("Tickets depleted OR unknown error.")
            return



# Generate a simple option choosing interface, then return the user's choice
def startOptions(options):
    if (len(options) == 0):
        return 
    for i in range(0, len(options)):
        print(f"[{i+1}] {options[i]}")
    validInput = False
    userInput = ""
    while (not validInput):
        userInput = input(">> ")
        try:
            userInput = options[int(userInput)-1]
            validInput = True
        except:
            print("Invalid option.")
    return userInput

def clear():
  os.system('cls' if os.name == 'nt' else 'clear')
  time.sleep(1)

def farmStagesMenu():
    a = True
    while (a):
        print(f"Current stage: {maxCurrentStage}")
        option = startOptions(["Farm X number of stages", "Farm until energy depletion", "Back"])
        if (option == "Farm X number of stages"):
            X = int(input("Amount of stages to farm: "))
            farmStages(X)
            continue
        elif (option == "Farm until energy depletion"):
            farmStages(0)
            continue
        elif (option == "Back"):
            a = False

def summonMenu():
    a = True
    while (a):
        print(f"Current stage: {maxCurrentStage}")
        option = startOptions(["Summon normal X amount of times", "Summon normal until ticket depletion", "Summon exclusive X amount of times", "Summon exclusive until ticket depletion", "Back"])
        if (option == "Summon normal X amount of times"):
            X = int(input("Amount to summon: "))
            autoSummon(X, True)
            continue
        elif (option == "Summon exclusive X amount of times"):
            X = int(input("Amount to summon: "))
            autoSummon(X, False)
            continue
        elif (option == "Summon normal until ticket depletion"):
            autoSummon(0, True)
            continue
        elif (option == "Summon exclusive until ticket depletion"):
            autoSummon(0, False)
            continue
        elif (option == "Back"):
            a = False

# There isn't actually an api for "logging out"
def logout():
    print("Bye bye!")
    quit()

# def login():
#     pass

# Main menu subprogram
def mainMenu():
    a = True
    while (a):
        print(f"Username: {nickname}")
        print(f"Level: {level}")
        print(f"Current stage: {maxCurrentStage}")
        option = startOptions(["Farm stages", "Summon", "Logout"])
        if (option == "Farm stages"):
            farmStagesMenu()
            continue
        elif (option == "Summon"):
            summonMenu()
            continue 
        elif (option == "Logout"):
            a = False
            logout()
        clear()

# def startUpMenu():
#     pass

# Using try: except: to ignore annoying errors (i cannot be asked to fix em)
try:
    # Gets the game's status, with the game's build
    gameStatus, gameBuild = getGameInfo()

    # Game's build version will always be == farmbot version
    if (not gameBuild == farmBotVersion):
        print("Farmbot is currently outdated, please wait for an update!")
        print(f"Game version: {gameBuild}\nFarmbot version: {farmBotVersion}")

    # Generate new tokens for the player & saves them to a text file
    tokens = getNewPlayerTokens()

    with open(path, "w") as tokensFile:
        tokensFile.write(json.dumps(tokens))
        tokensFile.close()

    # Set the headers
    headersGet = {
            'Host': 'tino.detailgames.ai',
            'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
            'Connection': 'keep-alive',
            'x-client-build': gameBuild,
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Authorization': 'Bearer ' + tokens['accessToken'],
            'X-Unity-Version': '2022.3.62f2',
        }
    headersPostJson = {
            'Host': 'tino.detailgames.ai',
            'User-Agent': 'Greatest%20Estate%20Dev%3A%20Squad%20TD/30 CFNetwork/3860.300.31 Darwin/25.2.0',
            'x-client-build': gameBuild,
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Authorization': 'Bearer ' + tokens['accessToken'],
            'X-Unity-Version': '2022.3.62f2',
            'Content-Type': 'application/json',
        }
    
    validTokens = testPlayerTokens()
    tokenRefreshTries = 0

    print("Tokens are valid, starting farmbot.")
    time.sleep(1.5)

    global nickname, level, maxCurrentStage
    nickname, level, maxCurrentStage = getPlayerDetails()
    mainMenu()
except KeyboardInterrupt:
    print("Interrupted.")
except Exception as error:
    print(f"An error occured: {error}")
